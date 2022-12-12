#!/bin/zsh

export MODEL_EN_ABS_PATH=/models/saved
export MODEL_UK_ABS_PATH=/models/saved_ukr
export MODEL_ISCAT_ABS_PATH=/models/saved_cat_cls

cd src/server
python app.py
