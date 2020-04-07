import json
import os
import string

def load_tweets(file=''):
    tweets = []
    
    with open(file, "r") as file:
        tweets = json.load(file)

    return tweets

def size_of_tweets(tweets):
    result = 0
    counter = 0
    # For each tweet in the file, compute the number of words it contains
    for tweet in tweets:
        result += sum([i.strip(string.punctuation).isalpha() for i in tweet.split()]) 
        print(tweet.split().strip(string.punctuation).isalpha())
        counter += 1
    
    return result/counter

def clustered_file_creation(tweets, file=''):
    # Dump to a file
    # with open(file,"w") as file:
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    tweets = load_tweets("./resources/collected_subjects/dem_debate_tweets.json")
    print(size_of_tweets(tweets))