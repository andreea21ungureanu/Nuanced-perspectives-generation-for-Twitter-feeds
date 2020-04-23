import json
from sklearn import metrics
import os
import sys
from sklearn.cluster import DBSCAN, OPTICS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.clustering import *

def load_tweets(file=''):
    tweets = []
    # with open(file, 'r') as f:
    with open(file, "r") as file:
        tweets = json.load(file)

    return tweets

def create_np_emotions_array_copy(tweets):
    vectors = np.empty((0, 5))

    # Add all the vectors to our matrix
    for tweet in tweets:
        emotions = tweet['emotions']
        vector = np.array([[emotions['Excitement'],
                            emotions['Anger'],
                            emotions['Sadness'],
                            emotions['Happiness'],
                            emotions['Fear']]])
        
        vectors = np.append(vectors, vector, axis=0)

    return vectors

def create_np_old_emotions_array(tweets):
    vectors = np.empty((0, 5))

    # Add all the vectors to our matrix
    for tweet in tweets:
        emotions = tweet['emotions']
        vector = np.array([[emotions['Excited'],
                            emotions['Angry'],
                            emotions['Sad'],
                            emotions['Happy'],
                            emotions['Fear']]])
        
        vectors = np.append(vectors, vector, axis=0)

    return vectors

def dbscan_clustering(tweets):
    vectors = create_np_emotions_array(tweets)

    # Cluster using DBSCAN
    dbscan_clusters = DBSCAN(eps=0.07).fit_predict(vectors)

    return dbscan_clusters

def optics_clustering(tweets):
    vectors = create_np_emotions_array(tweets)

    # Cluster using DBSCAN
    optics_clusters = OPTICS().fit_predict(vectors)

    return optics_clusters
   
def recompute_clusters_from_divisive(tweets):
    tweets_in_clusters = []
    for tweet in tweets:
        cluster_nr = tweet['cluster']
        tweets_in_clusters.append(cluster_nr)
    
    return tweets_in_clusters

def validate_clusters(tweets):
    # Instantiate the vectors used for clustering
    vectors = create_np_emotions_array_copy(tweets)

    # Use the existent data about the clusters from the tweets file instead of recomputing the cluster number
    reconstructed_divisive = recompute_clusters_from_divisive(tweets)
    # Validate the clustering methods
    # For Divisive Hierarhical Clustering
    divisive_hierarhical_score = metrics.silhouette_score(vectors, reconstructed_divisive, metric='euclidean')

    return divisive_hierarhical_score

def investigate_kmeans(tweets):
    vectors = create_np_old_emotions_array(tweets)

    # Instantiate clustering methods
    kmeans_clustering_v = kmeans_clustering(tweets)

    # For KMeans Clustering
    kmeans_score = metrics.silhouette_score(vectors, kmeans_clustering_v, metric='euclidean')

    return kmeans_score

def investigate_DBSCAN(tweets):
    vectors = create_np_old_emotions_array(tweets)

    # Instantiate clustering methods
    DBSCAN_clustering_v = dbscan_clustering(tweets)

    DBSCAN_score = metrics.silhouette_score(vectors, DBSCAN_clustering_v)

    return DBSCAN_score

if __name__ == '__main__':
    # tweets = load_tweets("./FlaskApp/perspectives_app/static/json/uklockdown/relabelled_clustered_tweets.json")
    tweets = load_tweets("./resources/emotions_collected/emotions_coronavirus.json")

    print(investigate_DBSCAN(tweets))
