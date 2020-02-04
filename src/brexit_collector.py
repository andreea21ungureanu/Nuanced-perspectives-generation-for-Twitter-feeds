import enchant
from nltk.tokenize import RegexpTokenizer
import tweepy

from emotions_annotator import EmotionsAnnotator
from topic_listener import TopicListener

def initialise_twitter_api():
    auth = tweepy.OAuthHandler("1ZFHYjytKK4Nb3bFqMKkPfh4V", "3yeGXrB2GkPc6zoACILhKKvh0Jh3E1tdfdEqZwlKbOupCmX1hl")
    auth.set_access_token("1027862472705945600-cBaQtkTpiPaEf6JNsnGMzO0X69R4dN", "8DuxmQg0cphVsroWQdCxSN5pNQez2QncjCU7F5w6L8EXO")
    
    return tweepy.API(auth)

def collect_tweets(api, nr_of_tweets, file_to_save=''):
    # Configure the stream
    topicListener = TopicListener(nr_of_tweets, file_to_save)
    stream = tweepy.Stream(auth=api.auth, listener=topicListener)

    # Run the stream
    print("Starting the stream ...")
    stream.filter(track=["brexit"])

    return topicListener.get_tweets()

if __name__ == '__main__':
    api = initialise_twitter_api()
    counter  = 0
    while (counter <= 49):
        tweets = collect_tweets(api, 5, "resources/brexit_tweets_test.json")
        counter += 1