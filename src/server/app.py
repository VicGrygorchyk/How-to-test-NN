from typing import List, Literal
import os

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from transformers import pipeline


app = FastAPI()

model_en_checkpoint = os.getenv('MODEL_EN_ABS_PATH')
model_uk_checkpoint = os.getenv('MODEL_UK_ABS_PATH')

# translator_en = pipeline("translation", model=model_en_checkpoint)
# translator_uk = pipeline("translation", model=model_uk_checkpoint)

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

    # result = translator_en(input_to_translate) if source_lang == EN_LANG else translator_uk(input_to_translate)
    return None  # result


@app.post("/classify_cat", response_model=ImageResult)
async def classify_cat(cat_image: ImageToClassify):
    base64_src = cat_image.src
    return {'is_cat': False}


app.mount("/", StaticFiles(directory="build", html=True), name="build")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)