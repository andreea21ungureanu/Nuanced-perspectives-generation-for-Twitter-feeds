import enchant
import json
from nltk.tokenize import RegexpTokenizer
import tweepy

from emotions_annotator import EmotionsAnnotator
from topic_listener import TopicListener

def initialise_twitter_api():
    auth = tweepy.OAuthHandler("zH15Zp6FvdKKqHFrtwNlFDuga", "qt44eT3R54iFG8szB61e0X1cQe2BKf9L39trtKpbOIfNygC2l6")
    auth.set_access_token("1027862472705945600-cBaQtkTpiPaEf6JNsnGMzO0X69R4dN", "8DuxmQg0cphVsroWQdCxSN5pNQez2QncjCU7F5w6L8EXO")
    
    return tweepy.API(auth)

def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list

def load_tweets(file=''):
    tweets = []
    
    with open(file, "r") as file:
        tweets = json.load(file)

    return make_unique(tweets)

def collect_tweets(api, nr_of_tweets, file_to_save=''):
    # Configure the stream
    topicListener = TopicListener(nr_of_tweets, file_to_save)
    stream = tweepy.Stream(auth=api.auth, listener=topicListener)

    # Run the stream
    print("Starting the stream ...")
    stream.filter(track=["brexit"])

    return topicListener.get_tweets()

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


def annotate_tweets(tweets):
    print( "\nStarting detecting emotion for the collected tweets:" )
    annotator = EmotionsAnnotator(file_name="./resources/emotions_dem_debate.json")
    
    print( "\nTweets just got emotional. Checkout the file!" )
    return annotator.annotate(tweets)


if __name__ == '__main__':
    # api = initialise_twitter_api()
    # tweets = collect_tweets(api, 30, "../resources/brexit_tweets.json")
    tweets = load_tweets("./resources/collected_subjects/coronavirus_tweets.json")
    sanitised_tweets = sanitise_tweets(tweets)
    annotate_tweets(sanitised_tweets)


