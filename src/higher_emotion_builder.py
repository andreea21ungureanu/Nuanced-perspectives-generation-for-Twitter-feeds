import json
import os

# TODO: Add not bored
SECOND_TYPE_EMOTIONS = {("Happy", "Fear"): "Guilt",
                        ("Happy", "Excited"): "Delight",
                        ("Happy", "Angry"): "Pride",
                        ("Sad", "Fear"): "Despair",
                        ("Sad", "Excited"): "Disappointment",
                        ("Sad", "Angry"): "Envy",
                        ("Fear", "Excited"): "Alarm",
                        ("Angry", "Excited"): "Outrage",
                        }

def load_clusters(file=''):
    clusters = []
    # with open(file, 'r') as f:
    with open(file, "r") as file:
        clusters = json.load(file)

    return clusters

def max_two_emotions(cluster_dict):
    first_max = 0
    second_max = 0

    for emotion, value in cluster_dict.items():
        if value > first_max:
            first_max = value
            first_emotion = emotion
        elif value <= first_max and value > second_max:
            second_max = value
            second_emotion = emotion
    
    return first_emotion, second_emotion

def interpret_centroids(clusters):
    higher_emotions_dict = {}
    
    for cluster_number, centroid in clusters.items():
        emotions_to_add = max_two_emotions(centroid)
        print(centroid)
        for emotions, higher_emotion in SECOND_TYPE_EMOTIONS.items():
            if (emotions[0] == emotions_to_add[0] and emotions[1] == emotions_to_add[1]) or (emotions[0] == emotions_to_add[1] and emotions[1] == emotions_to_add[0]):
                higher_emotions_dict[cluster_number] = higher_emotion
   
    return higher_emotions_dict

def higher_emotion_centroids(clusters):
    higher_emotions_clusters_dict = {}

    for cluster_number, centroid_normal_emotions in clusters.items():
        temp_higher_emotion_dict = {}
        for normal_pair_emotions, higher_emotion in SECOND_TYPE_EMOTIONS.items():
            temp_higher_emotion_dict[higher_emotion] = centroid_normal_emotions[normal_pair_emotions[0]] + centroid_normal_emotions[normal_pair_emotions[1]]
        
        higher_emotions_clusters_dict[cluster_number] = temp_higher_emotion_dict

    return higher_emotions_clusters_dict


def clusters_file_creation(tweets, file=''):
    # Dump to a file
    # with open(file,"w") as file:
    with open(file, "w") as file:
        file.write(json.dumps(tweets))


if __name__ == '__main__':
    centroids_of_tweets = load_clusters("./FlaskApp/perspectives_app/static/json/centroids_of_tweets.json")
    clustered_tweets = interpret_centroids(centroids_of_tweets)
    higher_emotion_clustered_tweets = higher_emotion_centroids(centroids_of_tweets)
    clusters_file_creation(higher_emotion_clustered_tweets, "./FlaskApp/perspectives_app/static/json/higher_emotions_centroids_of_tweets.json")
    clusters_file_creation(clustered_tweets, "./FlaskApp/perspectives_app/static/json/higher_emotions.json")

