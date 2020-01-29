import json
import tweepy

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
            file.close()