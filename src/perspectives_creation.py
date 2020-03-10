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
"Self appraisal": "appraisal of the each invdividual's impact in the group on the subject",
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
"Angry": "Correlated to physical pain inflicted by an attacker or psychological pain caused by thoughts about real or imagined harm done by another. The behaviour motivated by it refer to fighting or other forms of aggressive behaviour.",
"Sad": "",
"Happy": "Correlated to successful performance of genetically predetermined life sustaining and propagating behaviours but ultimately the moment when hopes are realised and success achieved. The behaviour is motivated by Life sustaining and propagating behaviours and the achievement of objectives.",
"Bored": "",
"Surprise": "Correlated to mismatch between experience expected and experience that occurs. The behaviour is motivated by attention, laughter or behavioural immobility depending on the degree of mismatch.",
"Fear": "Correlated to expectation of a negative outcome. The behaviours are consistent with a negative outcome.",
"Aggressiveness": "",
"Pessimism": "",
"Optimism": "",
"Anxiety": "",
"Envy": "Correlated to resenting another’s success, coveting their possessions or the attention they receive, or guarding and hoarding own possessions. Behaviour motivated by selfishness.",
"Pride": "Correlated to pleasant thoughts that derive from the execution of behaviours that are in accordance with personal beliefs and values. Behaviours consistent with personal beliefs and ideas about ‘right’ and ‘wrong’ Behaviours designed to enhance feelings of self-satisfaction.",
"Outrage": "",
"Despair": "Correlated to the expectation of a negative outcome. The behaviours are consistent with a negative outcome.",
"Delight": "",
"Guilt": "Correlated to painful thoughts about real or imagined public failure to meet social standards and/or selfcriticism that derives from failure to behave in accordance with personal beliefs and values. Behaviours consistent with personal beliefs and ideas about ‘right’ and ‘wrong’.",
"Awe": "Correlated to novel stimulation of moderate or low intensity and no mismatch with expectations. Behaviour motivated by orienting reflex, moderate behavioural arousal, exploration.",
"Disapproval": "",
"Confusion": ""
}

def load_higher_emotions(file=''):
    higher_emotions = []
    
    with open(file, "r") as file:
        higher_emotions = json.load(file)
    return higher_emotions

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

# Get a list of keys from dictionary which has the given value
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()

    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys

def perspective_file_creation(tweets, file=''):
    # Dump to a file
    
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    higher_emotions = load_higher_emotions("./FlaskApp/perspectives_app/static/json/demdebate/higher_emotions.json")
    initial_text = create_basic_template(higher_emotions)
    extra_text = create_extra_template(higher_emotions)
    perspective_file_creation(initial_text, "./FlaskApp/perspectives_app/static/json/demdebate/initial_perspective.json")
    perspective_file_creation(extra_text, "./FlaskApp/perspectives_app/static/json/demdebate/extra_perspective.json")
