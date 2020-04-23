import json
import numpy as np
import os
from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN 


'''
Removes duplicates from a list

:param original_list: the list containing duplicates
:type original_list: JSON file

:return: a JSON list containing unique elements
:rtype: JSON file
'''
def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list

def load_tweets(file=''):
    tweets = []
    
    with open(file, "r") as file:
        tweets = json.load(file)

    return make_unique(tweets)

def rename_emotions(tweet):
    renamed_emotions = {}
    emotions = tweet['emotions']
    
    for emotion in emotions:
        if emotion == 'Excited':
            renamed_emotions['Excitement'] = emotions['Excited']
        if emotion == 'Angry':
            renamed_emotions['Anger'] = emotions['Angry']
        if emotion == 'Sad':
            renamed_emotions['Sadness'] = emotions['Sad']
        if emotion == 'Happy':
            renamed_emotions['Happiness'] = emotions['Happy']
        if emotion == 'Fear':
            renamed_emotions['Fear'] = emotions['Fear']

    tweet['emotions'] = renamed_emotions

    return tweet

'''
Creates NP arrays for the the set of the emotions of a tweet

:param tweets: the list of tweets with their associated emotions
:type tweets: list of dictionaries

:return: the np vectors of emotions for all the tweets
:rtype: np vector
'''
def create_np_emotions_array(tweets):
    vectors = np.empty((0, 5))

    # Add all the vectors to our matrix
    for tweet in tweets:
        emotions = rename_emotions(tweet)['emotions']
        vector = np.array([[emotions['Excitement'],
                            emotions['Anger'],
                            emotions['Sadness'],
                            emotions['Happiness'],
                            emotions['Fear']]])
        
        vectors = np.append(vectors, vector, axis=0)

    return vectors

'''
Adds the cluster number for each tweet

:param tweets: the list of tweets with their associated emotions
:type tweets: list of dictionaries

:param clusters: the clusters given by the clustering algorithm
:type clusters: clusters object given by the clustering algorithm

:return: the tweets alongside with their cluster number
:rtype: list of dictionaries
'''
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

'''
Computes the divisive hierarhical clustering technique on the given dataset. 

:param tweets: the list of tweets with their associated emotions
:type tweets: list of dictionaries

:param nr_of_clusters: the number of clusters to be computed by the algoritm
:type nr_of_clusters: integer

:return: clusters object given by the clustering algorithm
:rtype: clusters object given by the clustering algorithm
'''
def divisive_hierarhical_clustering(tweets, nr_of_clusters=10):
    vectors = create_np_emotions_array(tweets)

    # Cluster the vectors using Agglomerative clustering
    divisive_hierarhical_clusters = AgglomerativeClustering(n_clusters=nr_of_clusters).fit_predict(vectors)

    return divisive_hierarhical_clusters


'''
Computes the divisive hierarhical clustering technique on the given dataset. 

:param tweets: the list of tweets with their associated emotions
:type tweets: list of dictionaries

:param nr_of_clusters: the number of clusters to be computed by the algoritm
:type nr_of_clusters: integer

:return: clusters object given by the clustering algorithm
:rtype: clusters object given by the clustering algorithm
'''
def kmeans_clustering(tweets, nr_of_clusters=10):
    vectors = create_np_emotions_array(tweets)

    # Cluster using Kmeans
    kmeans_clusters = KMeans(n_clusters=nr_of_clusters, random_state=0).fit_predict(vectors)

    return kmeans_clusters

'''
Computes the emotions for the central value in a cluster

:param tweets: the list of tweets with their associated emotions
:type tweets: list of dictionaries

:return: a dictionary containing the clusters mapped to the central point's emotions
:rtype: dictionary
'''
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
    tweets = load_tweets("./resources/emotions_collected/emotions_brexit.json")

    divisive_hierarhical_clusters = divisive_hierarhical_clustering(tweets)
    divisive_hierarhical_clustered_tweets = create_clustering_result_vector(tweets, divisive_hierarhical_clusters)
    clustered_file_creation(divisive_hierarhical_clustered_tweets, "./FlaskApp/perspectives_app/static/json/brexit/clustered_tweets.json")

    divisive_hierarhical_centroids = create_centroids(divisive_hierarhical_clustered_tweets)
    clustered_file_creation(divisive_hierarhical_centroids, "./FlaskApp/perspectives_app/static/json/brexit/centroids_of_tweets.json")

    # kmeans_clusters = kmeans_clustering(tweets)
    # kmeans_clustered_tweets = create_clustering_result_vector(tweets, kmeans_clusters)
    # clustered_file_creation(kmeans_clustered_tweets, "./FlaskApp/perspectives_app/static/json/brexit/kmeans_clustered_tweets.json")

    

    
    
