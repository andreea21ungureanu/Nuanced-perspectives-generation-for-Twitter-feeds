import enchant
import json
from nltk.tokenize import RegexpTokenizer
import tweepy

from emotions_annotator import EmotionsAnnotator
from topic_listener import TopicListener


'''
Connects to the the Twitter Search API

:return: the API connection object
:rtype: object
'''
def initialise_twitter_api():
    auth = tweepy.OAuthHandler("NLIE588gfuBHYFr6gMPG32b97", "bvcGe9jUbE1JPTzyEQnZdJLhhwmMhKyfhEi2S83val5kIis6UC")
    auth.set_access_token("1027862472705945600-cBaQtkTpiPaEf6JNsnGMzO0X69R4dN", "8DuxmQg0cphVsroWQdCxSN5pNQez2QncjCU7F5w6L8EXO")
    
    return tweepy.API(auth)

'''
Removes duplicates from a list

:param original_list: the list containing duplicates
:type original_list: JSON file

:return: a JSON list containing unique elements
:rtype: JSON file
'''
def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    
    return unique_list

def load_tweets(file=''):
    tweets = []
    
    with open(file, "r") as file:
        tweets = json.load(file)

    return make_unique(tweets)

'''
Streams the Twitter Search API to collect tweets on a certain subject

:param api: the API object connection to the Twitter Search API
:param nr_of_tweets: The number of tweets to be collected
:param file_to_save: The path to the file where the content should be saved

:type api: object
:type nr_of_tweets: integer
:type file_to_save: string

:return: JSON file of the collected tweets
:rtype: JSON file
'''
def collect_tweets(api, nr_of_tweets, file_to_save=''):
    # Configure the stream
    topicListener = TopicListener(nr_of_tweets, file_to_save)
    stream = tweepy.Stream(auth=api.auth, listener=topicListener)

    # Run the stream
    print("Starting the stream ...")
    stream.filter(track=["UKlockdown"])

    return topicListener.get_tweets()

'''
Clean the dataset so that non-english tweets are removed

:param tweets: the tweets to be sanitised
:type tweeets: JSON file

:return: the clean list of tweets
:rtype: JSON file
'''
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

'''
Annotate the tweets with the emotions they express

:param tweets: the tweets to be annotated with emotions
:type tweets: JSON file

:return: a list of dictionaries of tweets and their emotions
:rtype: JSON file
'''
def annotate_tweets(tweets):
    print( "\nStarting detecting emotion for the collected tweets:" )
    annotator = EmotionsAnnotator(file_name="./resources/emotions_collected/emotions_uk_lockdown.json")
    
    print( "\nTweets just got emotional. Checkout the file!" )
    return annotator.annotate(tweets)


if __name__ == '__main__':
    api = initialise_twitter_api()
    # tweets = collect_tweets(api, 5000, "./resources/collected_subjects/uk_lockdown.json")
    tweets = load_tweets("./resources/collected_subjects/uk_lockdown.json")
    sanitised_tweets = sanitise_tweets(tweets)
    annotate_tweets(sanitised_tweets)


