// Loading the JSON file
fetch("static/higher_emotions.json")
    // A promise to return the JSON once it's loaded
    .then((response) => { 
        return response.json();
    })
    .then((json) => {

        for ([clusterIdx, dominantEmotion] of Object.entries(json)) {            
            
            const perspective = document.getElementById("persp-" + clusterIdx);
            if (perspective == null) {
                return;
            }

            const perspectiveHeader = perspective.getElementsByClassName("persp-header")[0];
    
            perspectiveHeader.innerText = dominantEmotion;            
        }
    });

fetch("static/centroids_of_tweets.json")
    // A promise to return the JSON once it's loaded
    .then((response) => { 
        return response.json();
    })
    .then((json) => {

        for ([clusterIdx, emotionScores] of Object.entries(json)) {            
            
            const perspective = document.getElementById("persp-" + clusterIdx);
            if (perspective == null) {
                return;
            }

            const sortedEmotions = Object.entries(emotionScores).sort((entry1, entry2) => entry2[1] - entry1[1]);
            
            const perspectiveSubHeader = perspective.getElementsByClassName("persp-sub-header")[0];
            perspectiveSubHeader.innerText = sortedEmotions.slice(0, 2).map((entry) => entry[0]).join(" | ");   
            
            
        }
    });