import json

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
    tweets = []
    with open(file, 'r') as f:
        clusters = json.load(f)

    return clusters

def max_two_emotions(cluster_dict):
    first_max = 0
    second_max = 0

    for emotion, value in cluster_dict.items():
        if value > first_max:
            first_max = value
            first_emotion = 
        else if value <= first_max && value > second_max:
            second_max = value

def interpret_centroids(clusters, SECOND_TYPE_EMOTIONS):

