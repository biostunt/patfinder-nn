from typing import Tuple
import numpy as np
import tensorflow.keras as keras

STEP_BY_MAP = 1
MAP_SIZE = 100


def mutate_num(num):
    return np.round(num, 1)


def generate_point():
    x = np.random.randint(0, MAP_SIZE)
    y = np.random.randint(0, MAP_SIZE)
    return x, y


def distance_between_points(x1, y1, x2, y2):
    return np.math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_point_by_direction(x1, y1, direction):
    step = STEP_BY_MAP
    points = [
        [x1 - step, y1 + step], [x1, y1 + step], [x1 + step, y1 + step],
        [x1 - step, y1], [x1 + step, y1],
        [x1 - step, y1 - step], [x1, y1 - step], [x1 + step, y1 - step]
    ]
    return points[direction][0], points[direction][1]


def find_optimal_step(x1, y1, x2, y2):
    step = STEP_BY_MAP
    points = [
        [x1 - step, y1 + step], [x1, y1 + step], [x1 + step, y1 + step],
        [x1 - step, y1], [x1 + step, y1],
        [x1 - step, y1 - step], [x1, y1 - step], [x1 + step, y1 - step]
    ]
    distances = []
    for vals in points:
        distances.append(distance_between_points(vals[0], vals[1], x2, y2))
    step = np.argmin(distances)
    return step


def generate_dataset_ranged(count) -> Tuple[np.ndarray, np.ndarray]:
    data_x = []
    data_y = []
    for i in range(count):
        x1, y1 = generate_point()
        x2, y2 = generate_point()
        step = find_optimal_step(x1, y1, x2, y2)
        data_x.append([x1, y1, x2, y2])
        data_y.append(keras.utils.to_categorical(step, num_classes=8))
    return data_x, data_y


def generate_dataset_closed(count):
    data_x = []
    data_y = []
    for i in range(count):
        x1, y1 = generate_point()
        x2, y2 = get_point_by_direction(x1, y1, np.random.randint(0, 7))
        step = find_optimal_step(x1, y1, x2, y2)
        data_x.append([x1, y1, x2, y2])
        data_y.append(keras.utils.to_categorical(step, num_classes=8))
    return data_x, data_y


def generate_dataset(count):
    dataX1, dataY1 = generate_dataset_ranged(int(count / 2))
    dataX2, dataY2 = generate_dataset_closed(int(count / 2))
    dataX = np.array(dataX1 + dataX2)
    np.random.shuffle(dataX)
    dataY = [keras.utils.to_categorical(
        find_optimal_step(*sets), num_classes=8) for sets in dataX]
    dataY = np.array(dataY)
    return dataX, dataY


dataX, dataY = generate_dataset(10000)
