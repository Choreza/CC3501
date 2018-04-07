import numpy as np


class Mountain:
    def __init__(self, height, width, dh, digits):
        self._digits = float(digits)/1000

        self._height = height
        self._width = width
        self._dh = dh

        self._h = int(float(self._height)/self._dh)
        self._w = int(float(self._width)/self._dh)

        self._matrix = np.ones((self._h, self._w))

    def get_border(self, x):
        coast = 1200 + 400 * self._digits
        plant = coast + 120
        first_peak = coast + 400
        second_peak = first_peak + 800
        third_peak = second_peak + 300
        fourth_peak = third_peak + 800

        if x < coast:
            return self._h
        elif coast <= x <= plant:
            return self._h - 1
        elif plant < x <= first_peak:
            return self._h - 1 - int(float(100)/300) * (x - plant)
        elif first_peak < x <= second_peak:
            return self._h - 1 - int(float(1500 + 200 * self._digits)/800) * (x - first_peak)
        elif second_peak < x <= third_peak:
            return self._h - 1 + int(float(200)/300) * (x - second_peak)
        elif third_peak < x <= fourth_peak:
            return self._h - 1 - int(float(1850 + 100 * self._digits)/500) * (x - third_peak)
        else:
            return self._h - 1 + int(float(200)/300) * (x - fourth_peak)
