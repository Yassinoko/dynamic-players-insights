import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

#app.state.model = load_model()

@app.get("/")
# To be able to read Jason's video and store it
def read_root():
    pass


@app.post("/upload_video")
# To be able to read Jason's video and store it
def read_test(test):
    return {"upper_test" : test.upper()}
    # preprocessed_video = nikolay_preproc(jason file path)
    # predict = nikolay_model(preprocessed_video)
    # return kpi(predict)

# Process video

# Predict video

# Create KPIs

# Return final video to Jason

# app.get("predict")
