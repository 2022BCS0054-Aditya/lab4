import os
import pickle
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

model_path = os.path.join(os.getcwd(), "outputs", "model.pkl")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.post("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

@app.post("/predict")
def predict(data: WineFeatures):
    data_dict =data.model_dump()
    formatted_data = {key.replace("_", " "): value for key, value in data_dict.items()}
    input_df = pd.DataFrame([formatted_data])

    try:
        input_df = input_df[model.feature_names_in_]
    except AttributeError:
        column_order = [
            'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
            'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
            'pH', 'sulphates', 'alcohol'
        ]
        input_df = input_df[column_order]

    prediction = model.predict(input_df)
    return {
        "name": "Aditya U Baliga",
        "roll_no": "2022BCS0054",
        "wine_quality": float(prediction[0])
    }