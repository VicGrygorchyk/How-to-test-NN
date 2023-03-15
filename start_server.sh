#!/bin/zsh

export MODEL_EN_ABS_PATH=$(pwd)/assets/model_en_uk
export MODEL_UK_ABS_PATH=$(pwd)/assets/model_uk_en
export MODEL_ISCAT_ABS_PATH=$(pwd)/assets/model_cat_v_dog.pt

cd src/server
python app.py
