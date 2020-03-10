const clusterToHigherEmotion = new Map();
const clusterToRawEmotions = new Map();
const clusterToTweets = new Map();
const clusterToPerspective = new Map();
const clusterToExtraPerspective = new Map();

let tweetHtml;
let jsonDirectory = "";
let imagesDirectory = "";


const urlRegex =/(\b(https?|ftp|file):\/\/t.co[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;

function allDataLoaded() {
    return clusterToHigherEmotion.size > 0 && 
        clusterToRawEmotions.size > 0 && 
        clusterToTweets.size > 0 && 
        tweetHtml != null &&
        clusterToPerspective.size > 0 &&
        clusterToExtraPerspective.size > 0;
}

// Parse the URL parameter replated to the topic
function getParameterByName(name, url) {
    // Retrieve the URL
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");

    // Retrieve just the query string and remove additional information
    var regex = new RegExp(name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    results[2] = results[2].replace("?", "");

    // Return the query string or null
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

// Choose information that should be displayed on the page given the query string of the URL
function chooseSubject() {
    let topic = getParameterByName("topic");
    const subject_header = document.getElementsByClassName("subject-header")[0];

    if (topic == "US Democratic debate")
        topic = "demdebate";
    else if (topic == "Corona Virus")
        topic = "coronavirus";

    subject_header.innerText = "#" + topic;
    jsonDirectory = "/static/json/" + topic;
    imagesDirectory = "/static/images/" + topic + "/plot_";

    clustered_tweets_file = jsonDirectory + "/clustered_tweets.json";
    centroids_of_tweets_file = jsonDirectory + "/centroids_of_tweets.json";
    higher_emotions_file = jsonDirectory + "/higher_emotions.json";
    initial_perpective_file = jsonDirectory + "/initial_perspective.json";
    extra_perpective_file = jsonDirectory + "/extra_perspective.json";
}

function setContainerHeight() {
    const subjectContainer = document.getElementsByClassName("subject-container")[0];
    subjectContainer.style.height = window.innerHeight + "px";
}

function imagify(text) {
    return text.replace(urlRegex, (url) => {
        return '<meta name="twitter:url" content="' + url + '">';
    });
}

function addPerspectivesHTML() {
    fetch("/static/html/perspective.html").then((response) => response.text())
        .then((text) => {
            // Change the subject name depending on the chosen subject on the home page

            // Find the perspective div by id
            const perspective_html = text;
            const persp_container = document.getElementById("perspectives");
                
            // Iterate over the clusters (keys in one of the maps)
            for (clusterIdx of clusterToHigherEmotion.keys()) {
    
                // Creating an element and adding the html string to it to parse into a html
                // object. This lets us query to find the specific elements such as the header.
                const clusterHtml = document.createElement("div");
                persp_container.appendChild(clusterHtml);
                clusterHtml.innerHTML += perspective_html;

                // Find the header element and set it to the clusters higher emotion
                const clusterHeader = clusterHtml.getElementsByClassName("persp-header")[0];
                clusterHeader.innerText = clusterToHigherEmotion.get(clusterIdx);

                // Find the sub header element and set it to the clusters top raw emotions
                const clusterSubHeader = clusterHtml.getElementsByClassName("persp-sub-header")[0];
                clusterSubHeader.innerText = clusterToRawEmotions.get(clusterIdx)
                    .slice(0, 2)
                    .map((entry) => entry[0])
                    .join(" | ");

                // Find the img element and set it to the radar chart
                const clusterImg = clusterHtml.getElementsByClassName("radar-chart")[0];
                clusterImg.src = imagesDirectory + clusterIdx + ".png";

                // Find the p element and fill in the initial perspective text
                const clusterIntialPerspective = clusterHtml.getElementsByClassName("persp-initial")[0];
                clusterIntialPerspective.innerText = clusterToPerspective.get(clusterIdx);

                // Find the p element and fill in the extra perspective text
                const clusterExtraPerspective = clusterHtml.getElementsByClassName("persp-extra")[0];
                clusterExtraPerspective.innerText = clusterToExtraPerspective.get(clusterIdx);

                // Find the p element and set it to the tweets text
                const tweet_list = clusterHtml.getElementsByClassName("tweet-list")[0];
                for (const tweet of clusterToTweets.get(clusterIdx)) {
                    const tweetContainer = document.createElement("li");
                    tweet_list.appendChild(tweetContainer);
                    tweetContainer.innerHTML += tweetHtml;
                    tweetText = tweetContainer.getElementsByClassName("tweet-text")[0];
                    tweetText.innerText = tweet.tweet;
                    //.replace(urlRegex, "");
                }                
            }
        });

}

function loadJsonResources() {
    chooseSubject();

    fetch("/static/html/tweets.html").then((response) => response.text())
    .then((text) => {
        tweetHtml = text;
    });

    fetch(higher_emotions_file).then((response) => response.json())
        .then((json) => {

            for ([clusterIdx, dominantEmotion] of Object.entries(json)) {    
                clusterToHigherEmotion.set(clusterIdx, dominantEmotion);
            }

            if (allDataLoaded()) {
                addPerspectivesHTML();
            }
        });

    fetch(centroids_of_tweets_file).then((response) => response.json())
        .then((json) => {

            for ([clusterIdx, emotionScores] of Object.entries(json)) {     
                clusterToRawEmotions.set(clusterIdx, Object.entries(emotionScores).sort((entry1, entry2) => entry2[1] - entry1[1]));
            }
            
            if (allDataLoaded()) {
                addPerspectivesHTML();
            } 
        });

    fetch(clustered_tweets_file).then((response) => response.json())
        .then((json) => {

            for (tweet of json) {     
                const tweetCluster = "" + tweet.cluster;
                if (!clusterToTweets.has(tweetCluster)) {
                    clusterToTweets.set(tweetCluster, []);
                }
                clusterToTweets.get(tweetCluster).push(tweet);
            }
            
            if (allDataLoaded()) {
                addPerspectivesHTML();
            }
        });

    fetch(initial_perpective_file).then((response) => response.json())
    .then((json) => {

        for ([clusterIdx, perspective] of Object.entries(json)) {    
            clusterToPerspective.set(clusterIdx, perspective);
        }

        if (allDataLoaded()) {
            addPerspectivesHTML();
        }
    });

    fetch(extra_perpective_file).then((response) => response.json())
    .then((json) => {

        for ([clusterIdx, perspective] of Object.entries(json)) {    
            clusterToExtraPerspective.set(clusterIdx, perspective);
        }

        if (allDataLoaded()) {
            addPerspectivesHTML();
        }
    });
}


window.addEventListener("resize", setContainerHeight);
document.addEventListener("DOMContentLoaded", setContainerHeight);
window.addEventListener('DOMContentLoaded', loadJsonResources);