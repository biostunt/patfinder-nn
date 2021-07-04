import re
from typing import Tuple
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import Sequential
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
import numpy as np
from dataset import generate_dataset, get_point_by_direction
import tensorflow.keras.activations as activ

dataX, dataY = generate_dataset(20000)


class Network:
    def __init__(self) -> None:
        model = Sequential()
        model.add(Dense(4, input_shape=(dataX.shape[1],)))
        model.add(Dense(128, activation=activ.tanh))
        model.add(Dense(64, activation=activ.tanh))
        model.add(Dense(8, activation=activ.selu))
        model.add(Dense(8, activation=activ.softmax))

        model.compile(optimizer='adam', loss='categorical_crossentropy',
                      metrics='accuracy')
        self.model = model

    def train(self):

        self.model.fit(dataX, dataY, batch_size=5,
                       epochs=5, validation_split=0.2)

    def check_model(self):
        predict_count = 100
        predictX, predictY = generate_dataset(predict_count)
        res = self.model.predict(predictX)

        right_answers = 0
        for i in range(0, len(predictX)):
            if np.argmax(res[i]) == np.argmax(predictY[i]):
                right_answers += 1
        print(
            f'current percent of predicted vals: {right_answers}/{predict_count}')

    def predict(self, currX, currY, finishX, finishY):
        res = self.model.predict(np.array([[currX, currY, finishX, finishY]]))
        res = res[0]
        x, y = get_point_by_direction(currX, currY, np.argmax(res))
        return x, y
