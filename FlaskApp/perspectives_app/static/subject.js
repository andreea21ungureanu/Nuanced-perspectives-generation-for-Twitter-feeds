const clusterToHigherEmotion = new Map();
const clusterToRawEmotions = new Map();
const clusterToTweets = new Map();
let tweetHtml;

function allDataLoaded() {
    return clusterToHigherEmotion.size > 0 && clusterToRawEmotions.size > 0 && clusterToTweets.size > 0 && tweetHtml != null;
}

function addPerspectivesHTML() {
    fetch("static/perspective.html").then((response) => response.text())
        .then((text) => {

            // Find the perspective div by id
            const perspective_html = text;
            const persp_container = document.getElementById("perspectives");
                
            // Iterate over the clusters (keys in one of the maps)
            for (clusterIdx of clusterToHigherEmotion.keys()) {
                console.log(clusterIdx);
                
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
                clusterImg.src = "static/plot_" + clusterIdx + ".png";

                // Find the p element and set it to the tweets text
                const tweet_list = clusterHtml.getElementsByClassName("tweet-list")[0];
                for (const tweet of clusterToTweets.get(clusterIdx)) {
                    const tweetContainer = document.createElement("div");
                    tweet_list.appendChild(tweetContainer);
                    tweetContainer.innerHTML += tweetHtml;
                    tweetObject = tweetContainer.getElementsByClassName("tweeto")[0];
                    tweetObject.innerText = tweet.tweet
                }
                
            }
        });
}


fetch("static/tweets.html").then((resp) => resp.text())
.then((text) => {
    tweetHtml = text;
});

fetch("static/higher_emotions.json").then((response) => response.json())
    .then((json) => {

        for ([clusterIdx, dominantEmotion] of Object.entries(json)) {    
            clusterToHigherEmotion.set(clusterIdx, dominantEmotion);
        }

        if (allDataLoaded()) {
            addPerspectivesHTML();
        }
    });

fetch("static/centroids_of_tweets.json").then((response) => response.json())
    .then((json) => {

        for ([clusterIdx, emotionScores] of Object.entries(json)) {     
            clusterToRawEmotions.set(clusterIdx, Object.entries(emotionScores).sort((entry1, entry2) => entry2[1] - entry1[1]));
        }
        
        if (allDataLoaded()) {
            addPerspectivesHTML();
        } 
    });

fetch("static/clustered_tweets.json").then((response) => response.json())
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
  