import numpy as np
import tqdm
import matplotlib.pyplot as plt

class Mountain:
    def __init__(self, height, width, dh, digits):
        self._digits = float(digits)/1000

        self._height = height
        self._width = width
        self._dh = dh

        self._h = int(float(self._height)/self._dh)
        self._w = int(float(self._width)/self._dh)

        self._matrix = np.ones((self._h, self._w))
        self._mountain_border = []
        self.__calculate_border()

    def __calculate_border(self):
        dax = self.__scale_x(1200 + 400 * self._digits + 1)
        for i in range(dax):
            self._mountain_border.append(self._h)

        dbx = dax + self.__scale_x(120)
        for i in range(dax, dbx):
            self._mountain_border.append(self._h - 1)

        dax = dbx
        dbx += self.__scale_x(280)
        last_peak = 0
        for i in range(dax, dbx):
            x = i - dax
            h = int(x * (float(100)/300))
            self._mountain_border.append(self.__inverse_y(h))
            if i == dbx - 1:
                last_peak = h

        dax = dbx
        dbx += self.__scale_x(800)
        for i in range(dax, dbx):
            x = i - dax
            h = int(x * (float(1500 + 200 * self._digits)/800)) + last_peak
            self._mountain_border.append(self.__inverse_y(h))
            if i == dbx - 1:
                last_peak = h

        dax = dbx
        dbx += self.__scale_x(300)
        for i in range(dax, dbx):
            x = i - dax
            h = -int(x * (float(200)/300)) + last_peak
            self._mountain_border.append(self.__inverse_y(h))
            if i == dbx - 1:
                last_peak = h

        dax = dbx
        dbx += self.__scale_x(500)
        for i in range(dax, dbx):
            x = i - dax
            h = int(x * (float(550 - 100 * self._digits)/500)) + last_peak
            self._mountain_border.append(self.__inverse_y(h))
            if i == dbx - 1:
                last_peak = h

        dax = dbx
        for i in range(dax, self._w):
            x = i - dax
            h = -int(x * (float(200)/300)) + last_peak
            self._mountain_border.append(self.__inverse_y(h))
            if i == dbx - 1:
                last_peak = h

    def __scale_x(self, x):
        return int(float(x * self._w)/4000)

    def __scale_y(self, y):
        return int(float(x * self._w)/2000)

    def __inverse_y(self, y):
        return self._h - 1 - y

    def start(self):
        for _ in tqdm.tqdm(range(1)):
            for x in range(self._w):
                for y in range(self._h):
                    if self._mountain_border[x] <= y:
                        self._matrix[y][x] = np.nan

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.imshow(self._matrix, interpolation = 'none')
        plt.colorbar(cax)
        plt.show()


m = Mountain(2000,  4000, 1, 991)
m.start()
m.plot()