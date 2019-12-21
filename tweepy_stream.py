import tweepy
import paralleldots 
import json

class TopicListener(tweepy.StreamListener):
    def __init__(self, max_tweets, file_name=""):
        self.tweets = []
        self.max_tweets = max_tweets
        self.file_name = file_name
        
        super(TopicListener, self).__init__()

    def on_status(self, status):
        full_tweet_text = self.get_status_text(status)
        if (not full_tweet_text is None):
            self.tweets.append(full_tweet_text)

        if (len(self.tweets) > self.max_tweets):
            self.save_to_file()
            return False

        return True

    def get_tweets(self):
        return self.tweets

    def get_status_text(self, status):
        if hasattr(status, "retweeted_status"):  # Check if Retweet   
            try:
                return status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                return status.retweeted_status.text
        else:
            try:
                return status.extended_tweet["full_text"]
            except AttributeError:
                return status.text

    def save_to_file(self):
        if self.file_name != "":
            file = open(self.file_name, "a")
            file.write(json.dumps(self.tweets))
            file.write("\n")
            file.close

auth = tweepy.OAuthHandler("1ZFHYjytKK4Nb3bFqMKkPfh4V", "3yeGXrB2GkPc6zoACILhKKvh0Jh3E1tdfdEqZwlKbOupCmX1hl")
auth.set_access_token("1027862472705945600-cBaQtkTpiPaEf6JNsnGMzO0X69R4dN", "8DuxmQg0cphVsroWQdCxSN5pNQez2QncjCU7F5w6L8EXO")
api = tweepy.API(auth)

# Configure the stream
topicListener = TopicListener(20, "tweets.json")
stream = tweepy.Stream(auth=api.auth, listener=topicListener)

# Run the stream
print("Starting the stream ...")
stream.filter(track=["brexit"])

# Look at the tweets we've collected
collected_tweets = topicListener.get_tweets();
print("\nThe streaming ended. The following tweets were collected: ")
# print(collected_tweets)

# API key for Parallel Dots
parallel_dots_api_key = "tcIdTixALiJhUj5rZmWF8KziS8w442Fq2zzq1QptEP0"
paralleldots.set_api_key( parallel_dots_api_key )

# Create file to save the emotions from tweets
emotions_file = open("emotions.json","a+")
#emotions_file = open("emotions.txt","a+")

print( "\nStarting detecting emotion for the collected tweets:" )
emotions_file.write('[')
for tweet_text in collected_tweets:
    # Convert the emotion data to a python dictonary to get consistency in the emotion doc
    emotion_dictionary = paralleldots.emotion(tweet_text)
    emotions_file.write(json.dumps({"tweet": tweet_text, 
                                    "emotions": emotion_dictionary["emotion"], 
                                    "sarcasm": paralleldots.sarcasm(tweet_text)
                                    }))
    emotions_file.write(',')
emotions_file.write('{}')
emotions_file.write(']')
print( "\nTweets just got emotional. Checkout the file!" )
paralleldots.usage()