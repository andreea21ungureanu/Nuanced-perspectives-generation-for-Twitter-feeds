import json
import operator
import os

from clustering import divisive_hierarhical_clustering, create_clustering_result_vector, create_centroids

#TODO: ("Sad", "Happy"): "Bittersweetness",
SECOND_TYPE_EMOTIONS = {("Excited", "Angry"): "Aggressiveness",
                        ("Excited", "Sad"): "Pessimism",
                        ("Excited", "Happy"): "Optimism",
                        ("Excited", "Surprise"): "Confusion",
                        ("Excited", "Fear"): "Anxiety",
                        ("Angry", "Sad"): "Envy",
                        ("Angry", "Happy"): "Pride",
                        ("Angry", "Surprise"): "Outrage",
                        ("Angry", "Fear"): "Frozenness",
                        ("Sad", "Surprise"): "Disapproval",
                        ("Sad", "Fear"): "Despair",
                        ("Happy", "Surprise"): "Delight",
                        ("Happy", "Fear"): "Guilt",
                        ("Surprise", "Fear"): "Awe"
                        }

def load_clusters(file=''):
    clusters = []

    with open(file, "r") as file:
        clusters = json.load(file)
    return clusters

'''
Selects the first two emotions that have the highest values

:param cluster_dict: the dictionary containing the total value for eachhigher emotion
                     for each cluster
:type cluster_dict: dictionary

:return: the highest two emotions and their values in a quadruple
:rtype: tuple
'''
def max_two_emotions(cluster_dict):
    first_max = 0
    second_max = 0
    third_max = 0 
    first_emotion = ""
    second_emotion = ""
    third_emotion = ""

    #sorted_dict = dict( sorted(cluster_dict.items(), key=operator.itemgetter(1),reverse=True))

    for emotion, value in cluster_dict.items():
        # Change value and name of the emotion based on it's value
        if value > first_max:
            third_max = second_max
            third_emotion = second_emotion
            second_max = first_max
            second_emotion = first_emotion
            first_max = value
            first_emotion = emotion
        elif value <= first_max and value > second_max:
            third_max = second_max
            third_emotion = second_emotion
            second_max = value
            second_emotion = emotion
        elif value <= second_max:
            third_max = value
            third_emotion = emotion

    return first_emotion, second_emotion, first_max, second_max, third_max, third_emotion

'''
Computes threshold for each cluster in order to determine if the
higher emotion should be computed using make_higher_emotions or not.
The logic focuses on considering the average value an emotion should
have in a cluster and checking if that value is exceeded or not.

:param cluster_dict: the dictionary containing the total value for eachhigher emotion
                     for each cluster
:type cluster_dict: dictionary

:return: the threshold that the cluster need to overcome
:rtype: double
'''
def compute_threshold(cluster_dict):
    cluster_total_sum = 0
    for emotion, value in cluster_dict.items():
        cluster_total_sum += value
    
    return (cluster_total_sum/7)*2

'''
Decide whether to use the higher emotion or the highest basic emotion into creating
the perspectives

:param first_emotion: the highest basic emotion
:type first_emotion: double

:param second_emotion: the second highest basic emotion
:type second_emotion: double

:param cluster_dict: the dictionary containing the total value for eachhigher emotion
                     for each cluster
:type cluster_dict: dictionary

:return: true if the higher emotion value should be used for creating the perspective
         false otherwise
:rtype: bool
'''
def make_higher_emotions(first_emotion, second_emotion, cluster_dict):
    return first_emotion - second_emotion <= compute_threshold(cluster_dict)

'''
Swaps elements in a tuple. The tuple object in python is not assignable

:param element1: first element to swap
:type element1: tuple element

:param element2: second element to swap
:type element2: tuple element

:return: tuple with the swapped elements
:rtype: tuple
'''
def tuple_swap(element1, element2):
    temp = element1
    element1 = element2
    element2 = temp

    return element1, element2
'''
DOUBLE FUNCTIONALITY FUNCTION
I. Computes the higher emotion for a cluster given the basic emotions
II. Add the highest basic emotion if the threshold for a higher emotion is not overcame

:param clusters: the dictionary of clusters mapping to basic emotions
:type clusters: dictionary

:return: dictionary or the higher/basic that are going to be used in the further computations
:rtype: dictionary
'''
def interpret_centroids(clusters):
    higher_emotions_dict = {}
    basic_and_higher_emotions_dict = {}
    
    for cluster_number, centroid in clusters.items():
        emotions_to_add = max_two_emotions(centroid)
        emotions_type_higher = make_higher_emotions(emotions_to_add[2], emotions_to_add[3], centroid)

        if emotions_type_higher == True:
            emotion_modified_1 = emotions_to_add[0]
            emotion_modified_2 = emotions_to_add[1]

            if emotions_to_add[0] == "Bored":
                emotion_modified_1 = emotions_to_add[1]
            
            if emotions_to_add[1] == "Bored":
                emotion_modified_2 = emotions_to_add[5]

            for emotions, higher_emotion in SECOND_TYPE_EMOTIONS.items():
                if (emotions[0] == emotion_modified_1 and emotions[1] == emotion_modified_2) or (emotions[0] == emotion_modified_2 and emotions[1] == emotion_modified_1):
                    higher_emotions_dict[cluster_number] = higher_emotion
        else:
            higher_emotions_dict[cluster_number] = emotions_to_add[0]
   
    return higher_emotions_dict

'''
Computes the higher emotion representing the center of the cluster

:param clusters: the dictionary of clusters mapping to basic emotions
:type clusters: dictionary

:return: the dictionary containing the higher emotions for each cluster
:rtype: dictionary
'''
def higher_emotion_centroids(clusters):
    higher_emotions_clusters_dict = {}

    for cluster_number, centroid_normal_emotions in clusters.items():
        temp_higher_emotion_dict = {}
        for normal_pair_emotions, higher_emotion in SECOND_TYPE_EMOTIONS.items():
            temp_higher_emotion_dict[higher_emotion] = centroid_normal_emotions[normal_pair_emotions[0]] + centroid_normal_emotions[normal_pair_emotions[1]]
        
        higher_emotions_clusters_dict[cluster_number] = temp_higher_emotion_dict

    return higher_emotions_clusters_dict

# def create_unique_clusters(tweets_to_cluster):
#     counter = 10

#     divisive_clustering = divisive_hierarhical_clustering(tweets, counter)
#     clusters_centroids = create_centroids(create_clustering_result_vector(tweets, divisive_clustering))
#     print(clusters_centroids)
#     clustered_tweets = interpret_centroids(clusters_centroids)

#     # check for unique values 
#     flag = False
#     while flag == False:
#         counter += 1
#         divisive_clustering = divisive_hierarhical_clustering(tweets, counter)
#         clusters_centroids = create_centroids(create_clustering_result_vector(tweets, divisive_clustering))
#         clustered_tweets = interpret_centroids(clusters_centroids)

#         flag = len(clustered_tweets) != len(set(clustered_tweets.values())) 
    
#     return clustered_tweets


def clusters_file_creation(tweets, file=''):
    with open(file, "w") as file:
        file.write(json.dumps(tweets))


if __name__ == '__main__':
    centroids_of_tweets = load_clusters("./FlaskApp/perspectives_app/static/json/uklockdown/centroids_of_tweets.json")

    tweets = load_clusters("./resources/emotions_collected/emotions_uk_lockdown.json")
    clustered_tweets = create_unique_clusters(tweets)

    higher_emotion_clustered_tweets = higher_emotion_centroids(centroids_of_tweets)
    
    clusters_file_creation(higher_emotion_clustered_tweets, "./FlaskApp/perspectives_app/static/json/uklockdown/higher_emotions_centroids_of_tweets.json")
    clusters_file_creation(clustered_tweets, "./FlaskApp/perspectives_app/static/json/uklockdown/higher_emotions.json")
