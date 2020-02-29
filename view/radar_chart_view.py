import json
import matplotlib.pyplot as plt
import os
import pandas as pd
from math import pi

def load_higher_emotion_centroids(file=''):
    higher_emotion_centroids = []

    with open(file, "r") as file:
        higher_emotion_centroids = json.load(file)

    return higher_emotion_centroids

def set_data(higher_emotion_centroids):
    radar_data = {'group': [],
                    'Guilt': [],
                    'Delight': [],
                    'Pride': [],
                    'Despair': [],
                    'Disappointment': [],
                    'Envy': [],
                    'Alarm': [],
                    'Outrage': []
                    }

    for cluster_id, higher_emotion_dict in higher_emotion_centroids.items():
        radar_data['group'].append(cluster_id)
        for higher_emotion, value in higher_emotion_dict.items():
            radar_data[higher_emotion].append(value)
    
    return pd.DataFrame(radar_data)

def make_spider(radar_data, row, title, color):
    # number of variable
    categories=list(radar_data)[1:]
    N = len(categories)
    
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # Initialise the spider plot
    ax = plt.subplot(2,2,row+1, polar=True)
    
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([20,40,60,80,100,120,140,160,180], ["20","40","60","80","100","120","140"], color="grey", size=10)
    plt.ylim(0,200)
    
    # Ind1
    values=radar_data.loc[row].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.4)
    
    # Add a title
    plt.title(title, size=11, color=color, y=1.1)
    

    
if __name__ == '__main__':
    higher_emotion_centroids = load_higher_emotion_centroids("./FlaskApp/perspectives_app/static/json/brexit/higher_emotions_centroids_of_tweets.json")
    plot_data = set_data(higher_emotion_centroids)
    
    # ------- PART 2: Apply to all individuals
    # initialize the figure
    my_dpi=96
    plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)
    
    # Create a color palette:
    my_palette = plt.cm.get_cmap("Set2", plot_data.index.stop)
    
    # Loop to plot
    for row in range(0, plot_data.index.stop-1):
        print(row)
        make_spider(plot_data, row=row, title="", color=my_palette(row))
        plt.savefig('./FlaskApp/perspectives_app/static/images/plot_'+plot_data['group'][row] + '.png', bbox_inches='tight')
        plt.clf()
    plt.show()
    
