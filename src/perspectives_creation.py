import json
import os
from higher_emotion_builder import SECOND_TYPE_EMOTIONS

POSITIVE_NEGATIVE_MAP = {
"Excited": 1,
"Angry": 0,
"Sad": 0,
"Happy": 1,
"Bored": 0,
"Fear": 0,
"Aggressiveness": 0,
"Frozenness": 0,
"Pessimism": 0,
"Optimism": 1,
"Anxiety": 0,
"Envy": 0,
"Pride": 0,
"Outrage": 0,
"Despair": 0,
"Delight": 1,
"Guilt": 0,
"Awe": 1,
"Disapproval": 0
}

KIND_MAP = {
"Excited": "Future appraisal",
"Angry": "Event-related",
"Sad": "Event-related",
"Happy": "Event-related",
"Bored": "Related to object properties",
"Fear": "Future appraisal",
"Surprise": "Related to object properties",
"Aggressiveness": "Event-related",
"Frozenness": "Future appraisal",
"Pessimism": "Future appraisal",
"Optimism": "Future appraisal",
"Anxiety": "Future appraisal",
"Envy": "Social",
"Pride": "Self appraisal",
"Outrage": "Event-related",
"Despair": "Related to object properties",
"Delight": "Event-related",
"Guilt": "Event-related",
"Awe": "Event-related",
"Disapproval": "Event-related",
"Confusion": "Event-related"
}

KIND_INTERPRETATION = {
"Future appraisal": "appraisal of the future impact of the subject",
"Self appraisal": "appraisal of the each individual's impact in the group on the subject",
"Event-related": "events taking place as part of this subject",
"Related to object properties": "instances composing the subject",
"Social": "Social aspects of the subject"
}

HUMAINE_EARL_MAP = {"Excited": "Positive and lively",
"Angry": "Negative and forceful",
"Sad": "Negative and passive",
"Happy": "Positive and lively",
"Bored": "Negative and passive",
"Fear": "Negative and not in control",
"Surprise": "Reactive",
"Aggressiveness": "Negative and forceful",
"Frozenness": "Negative and not in control",
"Pessimism": "Negative thoughts",
"Optimism": "Positive thoughts",
"Anxiety": "Negative and not in control",
"Envy": "Negative thoughts",
"Pride": "Negative thoughts",
"Outrage": "Negative and forceful",
"Despair": "Negative and passive",
"Delight": "Positive and lively",
"Guilt": "Negative thoughts",
"Awe": "Reactive",
"Disapproval": "Negative thoughts",
"Confusion": "Negative and not in control"
}

HUMAINE_INTERPRETATION = {
"Positive and lively": ("support for the subject", "willing to stand up for it"),
"Positive thoughts": ("support for the subject", ""),
"Negative and forceful": ("lack of support for the subject", "willing to stand up for it"),
"Negative and passive": ("lack of support  for the subject", "thinking it is negligible"),
"Negative and not in control": ("lack of support  for the subject", "incapable of taking action"),
"Negative thoughts": ("lack of support  for the subject", ""),
"Reactive": ("","willing to get involved")
}

DESCRIPTION_MAP = {
"Excited": "",
"Angry": "Correlated to physical agony dispensed by an aggressor or mental torment brought about by contemplations about genuine or envisioned mischief done by another. The behaviour motivated by it refers to fighting or different types of forceful conduct.",
"Sad": "",
"Happy": "Correlated to the successful performance of life-sustaining and propagating habits naturally programmed but eventually the time when hopes are recognised and successfully accomplished. The behaviour is motivated by propagating behaviours and the fulfilment of goals.",
"Bored": "",
"Surprise": "Correlated to discrepancy among predicted perception and events that arise. The behaviour is motivated by exposure, amusement or mental exhaustion based on the level of mismatch.",
"Fear": "Correlated to the expectation of a negative outcome. The behaviours are consistent with a negative result.",
"Aggressiveness": "",
"Pessimism": "",
"Optimism": "",
"Anxiety": "",
"Envy": "Correlated to envy the progress of another, to covet their belongings or the recognition they get, or to protect and store own belongings. Behaviour motivated by selfishness.",
"Pride": "Correlated to pleasant thoughts arising from the conduct of actions that adhere to moral beliefs and principles. Behaviours are consistent with social views about 'right' and 'false' theories. Behaviours designed to boost thoughts of self-indulgence.",
"Outrage": "",
"Despair": "Correlated to the awaiting of disappointing results. The behaviours are associated with a negative outcome.",
"Delight": "",
"Guilt": "Correlated to stressful emotions regarding a true or perceived inability of the society to follow moral expectations and/or self-criticism arising from an inability to conform with personal beliefs and principles. Behaviour aligned with 'right' and 'false' moral values and theories.",
"Awe": "Correlated to novel stimulation of high or low intensity and no contradictions in beliefs. Motivated actions through automatic awareness, mild behavioural anticipation, discovery.",
"Disapproval": "",
"Confusion": ""
}

def load_higher_emotions(file=''):
    higher_emotions = []
    
    with open(file, "r") as file:
        higher_emotions = json.load(file)
    return higher_emotions

'''
Defines the template for the initial perspective

:param higher_emotions: the higher emotions list characterising each cluster
:type higher_emotions: JSON file

:return: the text of the perspective
:rtype: JSON file
'''
def create_basic_template(higher_emotions):
    perspective_initial_explanation_dict = {}

    for cluster_number, higher_emotion in higher_emotions.items():
        humaine_value = HUMAINE_EARL_MAP[higher_emotion]
        kind_value = KIND_MAP[higher_emotion]

        if HUMAINE_INTERPRETATION[humaine_value][0] == "":
            perspective_initial_explanation_dict[cluster_number] = "This group focuses on the " + KIND_INTERPRETATION[kind_value] + " part. They are " + HUMAINE_INTERPRETATION[humaine_value][1]
        elif HUMAINE_INTERPRETATION[humaine_value][1] == "":
            perspective_initial_explanation_dict[cluster_number] = "This group focuses on the " + HUMAINE_INTERPRETATION[humaine_value][0] +  ", in particular the " + KIND_INTERPRETATION[kind_value] + "."
        else:
            perspective_initial_explanation_dict[cluster_number] = "This group focuses on the " + HUMAINE_INTERPRETATION[humaine_value][0] +  ", in particular the " + KIND_INTERPRETATION[kind_value] + ". They are " + HUMAINE_INTERPRETATION[humaine_value][1]

    return perspective_initial_explanation_dict

'''
Defines the template for the extra perspective 

:param higher_emotions: the higher emotions list characterising each cluster
:type higher_emotions: JSON file

:return: the text of the extra perspective
:rtype: JSON file
'''
def create_extra_template(higher_emotions):
    perspective_extra_explanation_dict = {}

    for cluster_number, higher_emotion in higher_emotions.items():
        extra_value = DESCRIPTION_MAP[higher_emotion]
        key = getKeysByValue(SECOND_TYPE_EMOTIONS, higher_emotion)[0]

        if extra_value == "":
            perspective_extra_explanation_dict[cluster_number] = DESCRIPTION_MAP[key[0]] + DESCRIPTION_MAP[key[1]]
        else:
            perspective_extra_explanation_dict[cluster_number] = extra_value
    
    return perspective_extra_explanation_dict

'''
Retrieves the keys from a dictionary given a value

:param dictOfElements: dictionary containing objects
:type dictOfElements: dictionary object

:param valueToFind: the value for which we want to retieve the keys
:type valueToFind: string

:return: list of keys associated to the given value
:rtype: list
'''
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()

    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])

    if listOfKeys == []:
        return valueToFind
    return listOfKeys

def perspective_file_creation(tweets, file=''): 
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    higher_emotions = load_higher_emotions("./FlaskApp/perspectives_app/static/json/uklockdown/higher_emotions.json")
    initial_text = create_basic_template(higher_emotions)
    extra_text = create_extra_template(higher_emotions)
    perspective_file_creation(initial_text, "./FlaskApp/perspectives_app/static/json/uklockdown/initial_perspective.json")
    perspective_file_creation(extra_text, "./FlaskApp/perspectives_app/static/json/uklockdown/extra_perspective.json")
