#!/bin/bash
# Main script running the python files

SRC_PATH="$(pwd)/src"
VIEW_PATH="$(pwd)/view"

cd "$SRC_PATH" 
python3 tweets_get_emotional.py &&
python3 clustering.py &&
python3 higher_emotion_builder.py

cd "$VIEW_PATH"
python3 radar_chart_view.py