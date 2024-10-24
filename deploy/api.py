import os

import pickle
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from preprocessing import (
    preprocessing_sentence,
)
from sklearn.metrics import f1_score

app = FastAPI()

# load model
with open(
    "/mnt/c/Users/hi/work/project/sentiment-provider-app/provider-sentiment/data/06_models/clf.pickle/2024-10-20T09.46.57.785Z/clf.pickle",
    "rb",
) as file:
    model = pickle.load(file)


class InputText(BaseModel):
    text: str


@app.post("/predict")
def predict_sentiment(input_text: InputText):
    text = input_text.text
    preprocess_text = [preprocessing_sentence(text)]
    prediction = model.predict(preprocess_text)[0]

    sentiment_predict = "Negative" if prediction == 0 else "Positive"

    return {"Sentiment": sentiment_predict}
