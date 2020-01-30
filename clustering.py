import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def load_tweets(file=''):
    tweets = []
    with open(file, 'r') as f:
        tweets = json.load(f)

    return tweets

def divisive_hierarhical_clustering(tweets, nr_of_clusters=3):
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
    clusters = AgglomerativeClustering(n_clusters=nr_of_clusters).fit_predict(vectors)

    # Annotate each tweet with the cluster id
    result = []
    for i in range(len(tweets)):
        clustered_tweet = tweets[i]
        clustered_tweet['cluster'] = int(clusters[i])

        result.append(clustered_tweet)

    # Sort by cluster id
    result = sorted(result, key=lambda tweet: tweet['cluster'])

    return result

def clustered_file_creation(tweets, file=''):
    # Dump to a file
    with open(file,"w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    tweets = load_tweets("emotions.json")
    clustered_tweets = divisive_hierarhical_clustering(tweets)
    clustered_file_creation(clustered_tweets, "clustered_tweets.json")
