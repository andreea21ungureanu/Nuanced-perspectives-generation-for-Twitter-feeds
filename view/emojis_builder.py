import cairo
import json
import numpy as np
import os


MAX_FONT_SIZE = 5
EMOJI_SIZE = 35
DIAGRAM_SIZE = 500

EMOTION_TO_FILE = {
    "Happiness": "./view/emojis/happy_emoji.png",
    "Sadness": "./view/emojis/sad_emoji.png",
    "Fear": "./view/emojis/fear_emoji.png",
    "Excitement": "./view/emojis/excited_emoji.png",
    "Anger": "./view/emojis/angry_emoji.png"
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
            size = EMOJI_SIZE * get_emoji_weight(value, max_value)
            intermediary_emojis.update({emotion: size})

        emojis_dictionary[cluster_number] = intermediary_emojis
        intermediary_emojis = {}

    print(emojis_dictionary)
    return emojis_dictionary

def draw_image(ctx, image, rho, phi, height, width):
    """Draw a scaled image on a given context."""
    image_surface = cairo.ImageSurface.create_from_png(image)

    # calculate proportional scaling
    image_width = image_surface.get_width()
    image_height = image_surface.get_height()
    width_ratio = float(width) / float(image_width)
    height_ratio = float(height) / float(image_height)
    scale_xy = min(height_ratio, width_ratio)

    # Calculate cartesian coordinates
    x, y = pol2cart(rho, phi)
    x = x + (DIAGRAM_SIZE / 2) - (width / 2)
    y = y + (DIAGRAM_SIZE / 2) - (height / 2)

    # scale image and add it
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale_xy, scale_xy)
    ctx.set_source_surface(image_surface)

    ctx.paint()
    ctx.restore()

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def makeImage(emojis_dictionary, out_dir):
    phi_delta = 360 / len(emojis_dictionary)

    for cluster_nr, emotions in emojis_dictionary.items():
        with cairo.SVGSurface(out_dir + "cluster_" + str(cluster_nr) + ".svg", DIAGRAM_SIZE, DIAGRAM_SIZE) as surface:
            context = cairo.Context(surface)
        
            phi = 0
            rho_modifier = 0
            for emotion, size in emotions.items():
                image = EMOTION_TO_FILE[emotion]
                rho = size / 2
                
                if size > 0:
                    draw_image(context, image, rho + rho_modifier, phi, size, size)
                
                phi += phi_delta
                rho_modifier = size / 2

def perspective_file_creation(tweets, file=''): 
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    tweets = load_tweets("./FlaskApp/perspectives_app/static/json/brexit/relabelled_centroids_of_tweets.json")
    text = build_cloud(tweets)
    makeImage(text, "./FlaskApp/perspectives_app/static/images/brexit/emojiCloud/")
