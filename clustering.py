import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering

tweets = []
with open('emotions.json', 'r') as f:
    tweets = json.load(f)

# Initialize to correct dimensions
vectors = np.empty((0, 6))

# Add all the vectors to our matrix
for tweet in tweets:
    emotions = tweet['emotions']
    vector = np.array([[emotions['Excited'],
                        emotions['Angry'],
                        emotions['Sad'],
                        emotions['Happy'],
                        emotions['Bored'],
                        emotions['Fear']]])
    
    vectors = np.append(vectors, vector, axis=0)

# Cluster the vectors
clusters = AgglomerativeClustering(n_clusters=5).fit_predict(vectors)

# Annotate each tweet with the cluster id
result = []
for i in range(len(tweets)):
    clustered_tweet = tweets[i]
    clustered_tweet['cluster'] = int(clusters[i])

    result.append(clustered_tweet)

# Sort by cluster id
result = sorted(result, key=lambda tweet: tweet['cluster'])

# Dump to a file
with open("clustered_tweets.json","w") as file:
    file.write(json.dumps(result))