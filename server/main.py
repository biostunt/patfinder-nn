import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from route_finder import Network
import uvicorn


app = FastAPI()
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

network = Network()
network.train()
network.check_model()


@app.get('/check-connection')
def check_connection():
    return {'isAlive': True}


class PredictData(BaseModel):
    currX: int
    currY: int
    finishX: int
    finishY: int


@app.post('/predict-route')
def predict_route(data: PredictData):
    x, y = network.predict(data.currX, data.currY, data.finishX, data.finishY)
    return {'x': x, 'y': y}


# uvicorn.run(app, host='0.0.0.0', port=8000)
