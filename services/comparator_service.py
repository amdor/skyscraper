# -*- coding: utf-8 -*-
from enum import Enum
import logging

CAR_KEY = 'CarUri'
WORTH_KEY = 'worth'
#pairing keys of the data collection from HTML to the features
AGE = ['Évjárat', 'age']
CONDITION = ['Állapot', 'condition']
MASS = ['Saját tömeg', 'mass']
POWER = ['Teljesítmény', 'power']
PRICE = [('Akciós ár', 'Vételár'), 'price']
SPEEDOMETER = ['Kilométeróra állása', 'speedometer']
TRUNK = ['Csomagtartó', 'trunk']


class Conditions(Enum):
    COMMON = 'Normál'
    EXCELENT = 'Kitűnő'
    UNDAMAGED = 'Sérülésmentes'
    PRESERVED = 'Megkímélt'
    NOVEL = 'Újszerű'


def get_car_value(car_data):
    """
    This function enumerates through parameters of given car's primary parameters
    and generates their worth from them.
    Orders the values descendingly, returns the ordered array, in which each element has a Name and Value property
    """
    # Value marker
    car_worth = 0
    return car_worth


def compare_cars(cars_data):
    """
    This should be the entry point of this library
    Requires a data dictionary, where only CarUri is mandatory key
    all the keys are optional see all accepted keys at the start of the file
    Modifies input parameter structure: adds a "worth" key to it
    """
    for car_data in cars_data:
        if CAR_KEY in car_data:
            logging.debug('Getting value of %s (analyzing data)', CAR_KEY)
            car_data[WORTH_KEY] = get_car_value(car_data)
