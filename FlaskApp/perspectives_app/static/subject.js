async function getPerspectiveElement(perspectiveHtmlPromise) {
    const perspectiveElement = document.createElement("div");    
    perspectiveElement.innerHTML += await perspectiveHtmlPromise;    
    return perspectiveElement;
}

async function setPerspectiveHeader(perspectiveElement, higherEmotionsPromise, clusterIdx) {                         
    const perspectiveHeader = perspectiveElement.getElementsByClassName("persp-header")[0];
    perspectiveHeader.innerText = (await higherEmotionsPromise)[clusterIdx];
}

async function setPerspectiveSubHeader(perspectiveElement, clusterCentroidsPromise, clusterIdx) {                         
    const perspectiveSubHeader = perspectiveElement.getElementsByClassName("persp-sub-header")[0];
    const emotionScores = (await clusterCentroidsPromise)[clusterIdx];
    const sortedEmotions = Object.keys(emotionScores).sort(
        (emotionA, emotionB) => emotionScores[emotionB] - emotionScores[emotionA]);
    perspectiveSubHeader.innerText = sortedEmotions.slice(0, 2).join(" | ");
}

async function setPerspectiveImage(perspectiveElement, topic, clusterIdx) {
    const clusterImg = perspectiveElement.getElementsByClassName("radar-chart")[0];
    const clusterEmoji = perspectiveElement.getElementsByClassName("emoji-cloud")[0];
    clusterImg.src = `/static/images/${topic}/radarChart/plot_${clusterIdx}.png`;
    clusterEmoji.src = `/static/images/${topic}/emojiCloud/cluster_${clusterIdx}.svg`;
}

async function setPerspectivePrimaryDescription(perspectiveElement, initialPerspectivePromise, clusterIdx) {                         
    const perspectivePrimaryDescription = perspectiveElement.getElementsByClassName("persp-initial")[0];
    perspectivePrimaryDescription.innerText = (await initialPerspectivePromise)[clusterIdx];
}

async function setPerspectiveSecondaryDescription(perspectiveElement, extraPerspectivePromise, clusterIdx) {                         
    const perspectiveSecondaryDescription = perspectiveElement.getElementsByClassName("persp-extra")[0];
    perspectiveSecondaryDescription.innerText = (await extraPerspectivePromise)[clusterIdx];
}

async function setPerspectiveTweetList(perspectiveElement, clusteredTweetsPromise, tweetHtmlPromise, clusterIdx) {                         
    const perspectiveTweetList = perspectiveElement.getElementsByClassName("tweet-list")[0];
    for (const tweet of (await clusteredTweetsPromise).get(clusterIdx)) {
        
        const tweetContainer = document.createElement("li");
        perspectiveTweetList.appendChild(tweetContainer);

        tweetContainer.innerHTML += await tweetHtmlPromise;
        tweetText = tweetContainer.getElementsByClassName("tweet-text")[0];

        // If tweet text contains a link, extract it
        const urlRegex =/(\b(https?|ftp|file):\/\/t.co[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
        let urlContent = tweet.tweet.match(urlRegex);
        if (urlContent != null) {
            const breakElement = document.createElement("br");
            for (const url of urlContent) {
                tweet.tweet = tweet.tweet.replace(url, "");
                const linkElement = document.createElement("a");
                linkElement.href = url;
                linkElement.innerText = url;
                tweetContainer.appendChild(breakElement);
                tweetContainer.appendChild(linkElement);
            }                    
        }
        tweetText.innerText = tweet.tweet;   
    }
}

function setContainerHeight() {
    const subjectContainer = document.getElementsByClassName("subject-container")[0];
    subjectContainer.style.height = window.innerHeight + "px";
}

// Parse the URL parameter replated to the topic
function getParameterByName(name, url) {
    // Retrieve the URL
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");

    // Retrieve just the query string and remove additional information
    var regex = new RegExp(name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
        
    // Return the query string or null
    if (!results) return null;
    if (!results[2]) return '';
    results[2] = results[2].replace("?", "");
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function getTopic() {
    let topic = getParameterByName("topic");
 
    if (topic == "US Democratic debate")
        topic = "demdebate";
    else if (topic == "Corona Virus")
        topic = "coronavirus";
    else if (topic == "UK Lockdown")
        topic = "uklockdown";
    else if (topic == "Brexit")
        topic = "brexit";

    document.getElementById("sub-header").innerText = `#${topic}`;
    return topic;
}

function splitTweetsIntoClusters(tweet_list) {
    
    const clusterToTweets = new Map();
    
    for (const tweet of tweet_list) {
        if (!clusterToTweets.has(tweet.cluster)) {
            clusterToTweets.set(tweet.cluster, []);
        }
        clusterToTweets.get(tweet.cluster).push(tweet);
    }

    return clusterToTweets;
}

async function addPerspectivesHTML(topic) {

    // Load resources for the given topic
    const perspectiveHtmlPromise = fetch("/static/html/perspective.html").then((r) => r.text())
    const tweetHtmlPromise = fetch(`/static/html/tweets.html`).then((r) => r.text());
    const clustersPromise = fetch(`/static/json/${topic}/clusters.json`).then((r) => r.json());
    const clusteredTweetsPromise = fetch(`/static/json/${topic}/relabelled_clustered_tweets.json`).then((r) => r.json()).then(splitTweetsIntoClusters);
    const higherEmotionsPromise = fetch(`/static/json/${topic}/higher_emotions.json`).then((r) => r.json());
    const clusterCentroidsPromise = fetch(`/static/json/${topic}/centroids_of_tweets.json`).then((r) => r.json());
    const initialPerspectivePromise = fetch(`/static/json/${topic}/initial_perspective.json`).then((r) => r.json());
    const extraPerspectivePromise = fetch(`/static/json/${topic}/extra_perspective.json`).then((r) => r.json());

    // Find the perspective div by id
    const perspContainer = document.getElementById("perspectives");

    for (const clusterIdx of (await clustersPromise).clusters) {
        
        const perspectiveElement = await getPerspectiveElement(perspectiveHtmlPromise);
        perspContainer.appendChild(perspectiveElement);

        setPerspectiveHeader(perspectiveElement, higherEmotionsPromise, clusterIdx);
        setPerspectiveSubHeader(perspectiveElement, clusterCentroidsPromise, clusterIdx);
        setPerspectiveImage(perspectiveElement, topic, clusterIdx);
        setPerspectivePrimaryDescription(perspectiveElement, initialPerspectivePromise, clusterIdx);
        setPerspectiveSecondaryDescription(perspectiveElement, extraPerspectivePromise, clusterIdx);
        setPerspectiveTweetList(perspectiveElement, clusteredTweetsPromise, tweetHtmlPromise, clusterIdx);

        const button = perspectiveElement.getElementsByClassName("showhide")[0];
        button.addEventListener('click', () => {
            const radarChart = perspectiveElement.getElementsByClassName('radar-chart')[0];
            const emojiCloud = perspectiveElement.getElementsByClassName('emoji-cloud')[0];

            radarChart.style.display = radarChart.style.display == '' ? 'none' : '';
            emojiCloud.style.display = emojiCloud.style.display == '' ? 'none' : '';
            button.innerText = button.innerText == 'Display Emoji Cloud' ? 'Display Radar Chart' : 'Display Emoji Cloud';
        })

    }
}

function onWindowLoaded() {
    const topic = getTopic();
    addPerspectivesHTML(topic);
}

window.addEventListener("resize", setContainerHeight);
document.addEventListener("DOMContentLoaded", setContainerHeight);
window.addEventListener('DOMContentLoaded', onWindowLoaded);

