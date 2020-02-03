import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def load_tweets(file=''):
    tweets = []
    # with open(file, 'r') as f:
    with open(os.path.join('./resources/',file), "r") as file:
        tweets = json.load(file)

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

def create_centroids(tweets):
    centroids_dict = {}
    cluster_memeber_count = {}

    #Create dictionary of dictionary of the summed emotions for a cluster
    for tweet in tweets:
        emotions_dict = tweet['emotions']
        current_centroid = centroids_dict.get(tweet['cluster'], {})

        for emotion, value in tweet['emotions'].items():
            emotion_count = current_centroid.get(emotion, 0)
            current_centroid[emotion] = emotion_count + value
        
        centroids_dict[tweet['cluster']] = current_centroid

        # Create dictionary with the number of elements in a cluster
        if not tweet['cluster'] in cluster_memeber_count:
            cluster_memeber_count[tweet['cluster']] = 0
        
        cluster_memeber_count[tweet['cluster']] += 1
    
    # Create centroids
    for key, emotion in centroids_dict.items():
        for em, value in emotion.items():
            value = value/cluster_memeber_count[key]
    
    return centroids_dict

def clustered_file_creation(tweets, file=''):
    # Dump to a filec
    # with open(file,"w") as file:
    with open(os.path.join('./resources/',file), "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    tweets = load_tweets("emotions.json")
    clustered_tweets = divisive_hierarhical_clustering(tweets)
    centroids = create_centroids(clustered_tweets)
    clustered_file_creation(clustered_tweets, "clustered_tweets.json")
    clustered_file_creation(centroids, "centroids_of_tweets.json")
