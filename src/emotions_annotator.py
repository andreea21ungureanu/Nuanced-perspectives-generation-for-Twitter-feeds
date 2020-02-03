import json
from json.decoder import JSONDecodeError
import paralleldots 

class EmotionsAnnotator:
    PARALLEL_DOTS_API_KEY = "tcIdTixALiJhUj5rZmWF8KziS8w442Fq2zzq1QptEP0"

    def __init__(self, sarcasm=False, file_name=""):
        self.sarcasm = sarcasm
        self.file_name = file_name

        paralleldots.set_api_key(self.PARALLEL_DOTS_API_KEY)

    def annotate(self, tweets):
        annotated_tweets = []

        for tweet_text in tweets:
            # Convert the emotion data to a python dictonary to get consistency in the emotion doc
            emotion_dictionary = paralleldots.emotion(tweet_text)
            
            annotated_tweet = {"tweet": tweet_text, 
                                "emotions": emotion_dictionary["emotion"], 
                                }

            if self.sarcasm == True:
                sarcasm_dictionary = paralleldots.sarcasm(tweet_text)
                annotated_tweet["sarcasm"] = sarcasm_dictionary

            annotated_tweets.append(annotated_tweet)
            
        if self.file_name != "":
            self.__save_annotations(annotated_tweets)
    
        return annotated_tweets

    def __save_annotations(self, annotated_tweets):
        # with open(self.file_name, 'r') as infile:
        with open(os.path.join('./resources/',self.file_name), "r") as infile:
            try:
                current_annotated_tweets = json.load(infile)
            except JSONDecodeError:
                current_annotated_tweets = []

        # with open(self.file_name, 'w') as outfile:
        with open(os.path.join('./resources/',self.file_name), "w") as outfile:
            json.dump(current_annotated_tweets + annotated_tweets, outfile)

