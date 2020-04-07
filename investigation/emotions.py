import json
import os
import sys
import paralleldots 


PARALLEL_DOTS_API_KEY = "tcIdTixALiJhUj5rZmWF8KziS8w442Fq2zzq1QptEP0"

tweet_excited = "There's a festival next week. I'm looking forward to this"
tweet_angry = "WTF is wrong with you?"
tweet_sad = "I don't think I can live for another day"
tweet_happy = "What a great day!"
tweet_bored = "I can't be bothered to go to uni today"
tweet_fear = "I hope I'm not going to die because of this virus"
tweet_surprise = "Wow! That outcome was unexpected!"

def emotions_tester():
    #annotator = EmotionsAnnotator(file_name="./resources/investigation/emotions.json")

    outcome = paralleldots.emotion(tweet_fear)
    emotion_outcome = outcome['emotion']
    excited_outcome = emotion_outcome['Fear']
    print(emotion_outcome)
    if (excited_outcome >= 0.4):
        return True
    return False

if __name__ == '__main__':
    paralleldots.set_api_key(PARALLEL_DOTS_API_KEY)
    print(emotions_tester())
