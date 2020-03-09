import json
import os

POSITIVE_NEGATIVE_MAP = {
"Excited": 1,
"Angry": 0,
"Sad": 0,
"Happy": 1,
"Bored": 0,
"Fear": 0,
"Aggressiveness": 0,
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
"Aggressiveness": "Event-related",
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
"Aggressiveness": "Negative and forceful",
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

def perspective_file_creation(tweets, file=''):
    # Dump to a file
    
    with open(file, "w") as file:
        file.write(json.dumps(tweets))

if __name__ == '__main__':
    higher_emotions = load_higher_emotions("./FlaskApp/perspectives_app/static/json/coronavirus/higher_emotions.json")
    initial_text = create_basic_template(higher_emotions)
    perspective_file_creation(initial_text, "./FlaskApp/perspectives_app/static/json/coronavirus/initial_perspective.json")
