import json
import numpy as np
import os
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans

def load_tweets(file=''):
    tweets = []
    # with open(file, 'r') as f:
    with open(file, "r") as file:
        tweets = json.load(file)

    return tweets

def create_np_emotions_array(tweets):
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

    return vectors

def create_clustering_result_vector(tweets, clusters):
    # Annotate each tweet with the cluster id
    result = []
    for i in range(len(tweets)):
        clustered_tweet = tweets[i]
        clustered_tweet['cluster'] = int(clusters[i])

        result.append(clustered_tweet)

    # Sort by cluster id
    result = sorted(result, key=lambda tweet: tweet['cluster'])

    return result

def divisive_hierarhical_clustering(tweets, nr_of_clusters=5):
    vectors = create_np_emotions_array(tweets)

    # Cluster the vectors using Agglomerative clustering
    divisive_hierarhical_clusters = AgglomerativeClustering(n_clusters=nr_of_clusters).fit_predict(vectors)

    return divisive_hierarhical_clusters

def kmeans_clustering(tweets, nr_of_clusters=5):
    vectors = create_np_emotions_array(tweets)

    # Cluster using Kmeans
    kmeans_clusters = KMeans(n_clusters=nr_of_clusters, random_state=0).fit_predict(vectors)

    return kmeans_clusters

def create_centroids(tweets):
    centroids_dict = {}
    cluster_memeber_count = {}

    # Create dictionary of dictionary of the summed emotions for a cluster
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
    # Dump to a file
    # with open(file,"w") as file:
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    tweets = load_tweets("./resources/emotions_brexit.json")

    divisive_hierarhical_clusters = divisive_hierarhical_clustering(tweets)
    divisive_hierarhical_clustered_tweets = create_clustering_result_vector(tweets, divisive_hierarhical_clusters)
    clustered_file_creation(divisive_hierarhical_clustered_tweets, "./FlaskApp/perspectives_app/static/json/brexit/clustered_tweets.json")

    divisive_hierarhical_centroids = create_centroids(divisive_hierarhical_clustered_tweets)
    clustered_file_creation(divisive_hierarhical_centroids, "./FlaskApp/perspectives_app/static/json/brexit/centroids_of_tweets.json")

    # kmeans_clusters = kmeans_clustering(tweets)
    # kmeans_clustered_tweets = create_clustering_result_vector(tweets, kmeans_clusters)
    # clustered_file_creation(kmeans_clustered_tweets, "./FlaskApp/perspectives_app/static/json/brexit/kmeans_clustered_tweets.json")


    
    
