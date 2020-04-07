import copy
import json
import operator
import os

import enchant
from nltk.tokenize import RegexpTokenizer

from clustering import create_centroids

#TODO: ("Sad", "Happy"): "Bittersweetness",
SECOND_TYPE_EMOTIONS = {("Excitement", "Anger"): "Aggressiveness",
                        ("Excitement", "Sadness"): "Pessimism",
                        ("Excitement", "Happiness"): "Optimism",
                        ("Excitement", "Fear"): "Anxiety",
                        ("Anger", "Sadness"): "Envy",
                        ("Anger", "Happiness"): "Pride",
                        ("Anger", "Fear"): "Frozenness",
                        ("Sadness", "Fear"): "Despair",
                        ("Happiness", "Fear"): "Guilt"
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
    
    return (cluster_total_sum/5)*2

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

def flip_dictionary(higher_emotions_dict):
    flipped_dict = {} 
    
    for cluster_number, higher_emotion in higher_emotions_dict.items(): 
        if higher_emotion not in flipped_dict: 
            flipped_dict[higher_emotion] = [cluster_number] 
        else: 
            flipped_dict[higher_emotion].append(cluster_number) 
    
    return flipped_dict

def form_dominant_emotion_dict(flipped_dict, clusters):
    final_higher_emotions_dict ={}

    for emotion, list_of_cluster_nr in flipped_dict.items():
        if len(list_of_cluster_nr) > 1:
            maxx = 0
            max_cluster_nr = 0
            for cluster_nr in list_of_cluster_nr: 
                higest_basic_emotion = max_two_emotions(clusters[cluster_nr])[2]

                if higest_basic_emotion > maxx:
                    maxx = higest_basic_emotion
                    max_cluster_nr = cluster_nr
            
            final_higher_emotions_dict[max_cluster_nr] = emotion
        else:
            final_higher_emotions_dict[list_of_cluster_nr[0]] = emotion
    
    return final_higher_emotions_dict

def relabel_tweets(tweets, final_higher_emotions_dict, flipped_dict):
    copy_tweets = copy.deepcopy(tweets)
    for tweet in copy_tweets:
        found_flag = False
        for cluster, emotion in final_higher_emotions_dict.items():
            if tweet['cluster'] == int(cluster):
                found_flag = True
        
        if found_flag == False:
            tweet_dominant_emotion = ''
            for emotion, list_of_cluster_nr in flipped_dict.items():
                for cluster_nr in list_of_cluster_nr: 
                    # print(tweet['cluster'])
                    if tweet['cluster'] == int(cluster_nr):
                        tweet_dominant_emotion = emotion

            for cluster_nr, emotion in final_higher_emotions_dict.items():
                if emotion == tweet_dominant_emotion:
                    tweet['cluster'] = int(cluster_nr)
    return copy_tweets

def relabel_cluster_numbers(final_higher_emotions_dict):
    counter = 0
    temp_dict = {}
    from_old_to_new_val_dict = {}
    for cluster_nr, emotion in final_higher_emotions_dict.items():
        temp_dict[counter] = final_higher_emotions_dict[cluster_nr]
        from_old_to_new_val_dict[counter] = int(cluster_nr)
        counter += 1
    
    return temp_dict, from_old_to_new_val_dict

def create_final_clusters(higher_emotions_dict, clusters, tweets):
    
    # Flip dictionary so that each value forms a list of the keys it is mapped to
    flipped_dict = flip_dictionary(higher_emotions_dict)
    # print(flipped_dict)

    # Choose the max cluster_nr from the list of cluster numbers
    # and with that form the final dictionary
    final_higher_emotions_dict = form_dominant_emotion_dict(flipped_dict, clusters)

    # Re-label the tweets with the new clusters they should belong to
    relabelled_tweets = relabel_tweets(tweets, final_higher_emotions_dict, flipped_dict)

    # Re-label the cluster numbers with ascending consecutive numbers 
    dict_from_new_to_old = relabel_cluster_numbers(final_higher_emotions_dict)[1]
    final_higher_emotions_dict = relabel_cluster_numbers(final_higher_emotions_dict)[0]
    # print(dict_from_new_to_old)
    # Do the same re-labelling of the cluster numbers with ascending consecutive numbers but for tweets
    for tweet in relabelled_tweets:
        for new_val, old_val in dict_from_new_to_old.items():
            if tweet['cluster'] == old_val:
                tweet['cluster'] = new_val

    # print(relabelled_tweets)
    return final_higher_emotions_dict, relabelled_tweets

def cluster_numbers(final_higher_emotions_dict):
    clusters_nr_dict = {}
    cluster_list = []
    for cluster_nr, emotion in final_higher_emotions_dict.items():
        cluster_list.append(cluster_nr)
    
    clusters_nr_dict["clusters"] = cluster_list
    return clusters_nr_dict


def file_creation(tweets, file=''):
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

def sanitise_tweets(tweets):
    # Sanitize tweets in order to get rid of the ones in different languages or containing no words in english
    print("\nTime to sanitize these tweets! We only want the wholesome content.")
    dictionary = enchant.Dict("en_GB")
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    for tweet in tweets:
        tokenised_tweet = tokenizer.tokenize(tweet)
        counter = 0
        for token in tokenised_tweet:
            if dictionary.check(token):
                counter += 1;
            
        if counter <= len(tokenised_tweet)/2:
            tweets.remove(tweet)
    
    return tweets



if __name__ == '__main__':
    tweets = load_clusters("./FlaskApp/perspectives_app/static/json/brexit/clustered_tweets.json")
    centroids_of_tweets = load_clusters("./FlaskApp/perspectives_app/static/json/brexit/centroids_of_tweets.json")

    clustered_tweets = interpret_centroids(centroids_of_tweets)
    final_higher_emotions = create_final_clusters(clustered_tweets,centroids_of_tweets, tweets)[0]
    relabelled_tweets = create_final_clusters(clustered_tweets,centroids_of_tweets, tweets)[1]

    relabelled_centroids_of_tweets = create_centroids(relabelled_tweets)
    higher_emotion_clustered_tweets = higher_emotion_centroids(relabelled_centroids_of_tweets)
    cluster_numbers = cluster_numbers(final_higher_emotions)

    file_creation(higher_emotion_clustered_tweets, "./FlaskApp/perspectives_app/static/json/brexit/higher_emotions_centroids_of_tweets.json")
    file_creation(final_higher_emotions, "./FlaskApp/perspectives_app/static/json/brexit/higher_emotions.json")
    file_creation(relabelled_tweets, "./FlaskApp/perspectives_app/static/json/brexit/relabelled_clustered_tweets.json")
    file_creation(cluster_numbers, "./FlaskApp/perspectives_app/static/json/brexit/clusters.json")
    file_creation(relabelled_centroids_of_tweets, "./FlaskApp/perspectives_app/static/json/brexit/relabelled_centroids_of_tweets.json")
