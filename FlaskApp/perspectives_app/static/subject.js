const clusterToHigherEmotion = new Map();
const clusterToRawEmotions = new Map();
const clusterToTweets = new Map();
let tweetHtml;
let jsonDirectory;
let imagesDirectory;


const urlRegex =/(\b(https?|ftp|file):\/\/t.co[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;

function allDataLoaded() {
    return clusterToHigherEmotion.size > 0 && clusterToRawEmotions.size > 0 && clusterToTweets.size > 0 && tweetHtml != null;
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

    subject_header.innerText = "#" + topic;
    jsonDirectory = "/static/json/" + topic;
    imagesDirectory = "/static/images/" + topic + "/plot_";
}

function setContainerHeight() {
    const subjectContainer = document.getElementsByClassName("subject-container")[0];
    subjectContainer.style.height = window.innerHeight + "px";
}

function imagify(text) {
    return text.replace(urlRegex, (url) => {
        return '<img src="' + url + '"></img>';
    });
}

function addPerspectivesHTML() {
    fetch("/static/html/perspective.html").then((response) => response.text())
        .then((text) => {
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
                clusterImg.src = "/static/images/plot_" + clusterIdx + ".png";

                // Find the p element and set it to the tweets text
                const tweet_list = clusterHtml.getElementsByClassName("tweet-list")[0];
                for (const tweet of clusterToTweets.get(clusterIdx)) {
                    const tweetContainer = document.createElement("li");
                    tweet_list.appendChild(tweetContainer);
                    tweetContainer.innerHTML += tweetHtml;
                    tweetText = tweetContainer.getElementsByClassName("tweet-text")[0];
                    tweetText.innerText = tweet.tweet.replace(urlRegex, "");
                }                
            }
            // Change the subject name depending on the chosen subject on the home page
            chooseSubject();
        });

}

window.addEventListener("resize", setContainerHeight);
document.addEventListener("DOMContentLoaded", setContainerHeight);

fetch("/static/html/tweets.html").then((response) => response.text())
.then((text) => {
    tweetHtml = text;
});

fetch("/static/json/higher_emotions.json").then((response) => response.json())
    .then((json) => {

        for ([clusterIdx, dominantEmotion] of Object.entries(json)) {    
            clusterToHigherEmotion.set(clusterIdx, dominantEmotion);
        }

        if (allDataLoaded()) {
            addPerspectivesHTML();
        }
    });

fetch("/static/json/centroids_of_tweets.json").then((response) => response.json())
    .then((json) => {

        for ([clusterIdx, emotionScores] of Object.entries(json)) {     
            clusterToRawEmotions.set(clusterIdx, Object.entries(emotionScores).sort((entry1, entry2) => entry2[1] - entry1[1]));
        }
        
        if (allDataLoaded()) {
            addPerspectivesHTML();
        } 
    });

fetch("/static/json/clustered_tweets.json").then((response) => response.json())
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
  
