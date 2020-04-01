import emoji
from pyemojify import emojify
import json
import matplotlib.pyplot as plt
from matplotlib import rcParams

import io
from io import BytesIO
from wordcloud import WordCloud

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import os


MAX_FONT_SIZE = 90

EMOJI_MAP = {
"Excited": u"\U0001F973",
"Happy": "\U0001F604",
"Bored": "\U0001F634",
"Sad": "\U0001F641",
"Fear": "\U0001F630",
"Angry": "\U0001F620",
"Surprise": "\U0001F62F"
}
   
def load_tweets(file=''):
    clusters_emotions = []
    
    with open(file, "r") as file:
        clusters_emotions = json.load(file)

    return clusters_emotions

'''
Assign a font sized proportional to total occurances to the emotions

:param value: the value of the emotion in a cluster
:type value: double

:param max_value: the maxium value of an emotion in a cluster:
:type max_value: double

:return: the size of the emoji in the word cloud
:rtype: integer
'''
def get_emoji_weight(value, max_value):
    font_size = (value * MAX_FONT_SIZE) / max_value
    return int(font_size)

'''
Creates the data to be added to the emoji cloud
Each cluster has the emoji for each emotion as a key and the size of the emoji as a value

:param clusters_emotions: the clusters and their emotions
:type clusters_emotions: dictionary of dictionaries

:return: a dictionary containing the clusters and the representative emojis with the associated sizes
:rtype: dictionary
'''
def build_cloud(clusters_emotions):
    emojis_dictionary = {}
    intermediary_emojis = {}

    for cluster_number, emotions in clusters_emotions.items():
        max_value = max(clusters_emotions[cluster_number].values())
        for emotion, value in emotions.items():
            emoji = emojify(EMOJI_MAP[emotion])
            intermediary_emojis.update({emotion: get_emoji_weight(value, max_value)})
        
        emojis_dictionary[cluster_number] = intermediary_emojis
        intermediary_emojis = {}
    print(emojis_dictionary)
    return emojis_dictionary

def makeImage(cloud_dictionary):
    fpath = os.path.join(rcParams["datapath"], "fonts/ttf/OpenSansEmoji.ttf")

    wc = WordCloud( background_color="white")
    # generate word cloud
    for cluster_number, emojis in cloud_dictionary.items():
        wc.generate_from_frequencies(emojis)
        # show
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()


def perspective_file_creation(tweets, file=''): 
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    tweets = load_tweets("/Users/xuti/Desktop/Year3/Semester1/3rd year project/Nuanced-perspectives-generation-for-Twitter-feeds/FlaskApp/perspectives_app/static/json/demdebate/centroids_of_tweets.json")
    text = build_cloud(tweets)
    makeImage(text)
