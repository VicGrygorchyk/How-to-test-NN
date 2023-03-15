from typing import List, Literal
import os
import re

import torch
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from transformers import pipeline
import base64
from PIL import Image
from io import BytesIO

from transform import transform
from cats_classifier import get_pred, load_model


app = FastAPI()

model_en_checkpoint = os.getenv('MODEL_EN_ABS_PATH')
model_uk_checkpoint = os.getenv('MODEL_UK_ABS_PATH')
model_cls_checkpoint = os.getenv('MODEL_ISCAT_ABS_PATH')

translator_en = pipeline("translation", model=model_en_checkpoint)
translator_uk = pipeline("translation", model=model_uk_checkpoint)

cls_model = load_model(model_cls_checkpoint)

EN_LANG = 'en'
UK_LANG = 'uk'


class TranslateInput(BaseModel):
    input: str = 'TranslateInput'
    source_lang: str = Literal['en', 'uk']


class TranslatedText(BaseModel):
    translation_text: str = 'TranslatedText'


class ImageToClassify(BaseModel):
    src: str


class ImageResult(BaseModel):
    is_cat: bool


@app.post('/translate', response_model=List[TranslatedText])
async def translate(translate_input: TranslateInput) -> List[TranslatedText]:
    input_to_translate = translate_input.input
    source_lang = translate_input.source_lang
    if not input_to_translate:
        raise HTTPException(status_code=400, detail="Nothing to translate")
    with torch.no_grad():
        result = translator_en(input_to_translate) if source_lang == EN_LANG else translator_uk(input_to_translate)
    return result


@app.post("/classify_cat", response_model=ImageResult)
async def classify_cat(cat_image: ImageToClassify):
    try:
        base64_src = cat_image.src
        im = Image.open(BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', base64_src)))).convert('RGB')
        im_transformed = transform(im)
        res = get_pred(cls_model, im_transformed)
        print(res)
        return {'is_cat': res == 'cat'}
    except(Exception) as exc:
        print(exc)
        raise HTTPException(status_code=400, detail="Якась бісова помилка")


app.mount("/", StaticFiles(directory="build", html=True), name="build")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)
