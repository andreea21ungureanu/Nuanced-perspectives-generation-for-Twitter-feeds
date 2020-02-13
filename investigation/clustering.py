import json
from sklearn import metrics
import os

from src.clustering import create_np_emotions_array
from src.clustering import divisive_hierarhical_clustering
from src.clustering import kmeans_clustering

def load_tweets(file=''):
    tweets = []
    # with open(file, 'r') as f:
    with open(file, "r") as file:
        tweets = json.load(file)

    return tweets

def validate_clusters(tweets):
    # Instantiate the vectors used for clustering
    vectors = create_np_emotions_array(tweets)

    # Instantiate clustering methods
    divisive_hierarhical_clustering_v = divisive_hierarhical_clustering(tweets)
    kmeans_clustering_v = kmeans_clustering(tweets)

    # Validate the clustering methods
    # For Divisive Hierarhical Clustering
    divisive_hierarhical_score = metrics.silhouette_score(vectors, divisive_hierarhical_clustering_v, metric='euclidean')

    # For KMeans Clustering
    kmeans_score = metrics.silhouette_score(vectors, kmeans_clustering_v, metric='euclidean')

    if max(divisive_hierarhical_score, kmeans_score) == divisive_hierarhical_score:
        print("DIVISIVE")
    else:
        print("KMEANS")


if __name__ == '__main__':
    tweets = load_tweets("./resources/emotions.json")
    validate_clusters(tweets)

