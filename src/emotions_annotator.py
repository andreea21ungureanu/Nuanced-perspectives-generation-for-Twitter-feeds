import json
from json.decoder import JSONDecodeError
import os
import paralleldots 
import time

class EmotionsAnnotator:
    PARALLEL_DOTS_API_KEY = "tcIdTixALiJhUj5rZmWF8KziS8w442Fq2zzq1QptEP0"

    def __init__(self, sarcasm=False, file_name=""):
        self.sarcasm = sarcasm
        self.file_name = file_name

        paralleldots.set_api_key(self.PARALLEL_DOTS_API_KEY)
    
    def make_unique(self, original_list):
        unique_list = []
        [unique_list.append(obj) for obj in original_list if obj not in unique_list]
        return unique_list

    def annotate(self, tweets):
        annotated_tweets = []
        counter = 0

        for tweet_text in tweets:
            # Convert the emotion data to a python dictonary to get consistency in the emotion doc
            if counter >= 60:
                counter = 0
                time.sleep(60)
            
            emotion_dictionary = paralleldots.emotion(tweet_text)
            #emotion_dictionary['emotion']['abc'] = 1 - emotion_dictionary['emotion']['def']
            counter += 1
            
            annotated_tweet = {"tweet": tweet_text, 
                                "emotions": emotion_dictionary["emotion"], 
                                }
           

            if self.sarcasm == True:
                sarcasm_dictionary = paralleldots.sarcasm(tweet_text)
                annotated_tweet["sarcasm"] = sarcasm_dictionary
        
            annotated_tweets.append(annotated_tweet)
            
            self.__save_annotations(annotated_tweets)
            annotated_tweets = []
            
        # if self.file_name != "":
        #     self.__save_annotations(annotated_tweets)
    
        return make_unique(annotated_tweets)

    def __save_annotations(self, annotated_tweets):
        with open(self.file_name, "r") as infile:
            try:
                current_annotated_tweets = json.load(infile)
            except JSONDecodeError:
                current_annotated_tweets = []

        with open(self.file_name, "w") as outfile:
            json.dump(current_annotated_tweets + annotated_tweets, outfile)

