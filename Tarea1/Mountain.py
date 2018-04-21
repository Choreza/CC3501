import numpy as np
import matplotlib.pyplot as plt
import tqdm 
from Temperature import Temperature

class Mountain:
    def __init__(self, height, width, dh, digits):
        self._d = float(digits)/1000

        self._height = height
        self._width = width
        self._dh = dh

        self._h = int(float(self._height)/self._dh)
        self._w = int(float(self._width)/self._dh)

        self._matrix = np.zeros((self._h, self._w))

    def _get_border(self):
        self._m_border = []
        xa = 0
        xb = 1200+400*self._d
        for x in range(0, self.__scl_x(xb)):
            self._m_border.append(self._h)

        xa = xb
        xb = xa+120
        for x in range(self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(0))

        xa = xb
        xb = xa+280
        m = float(100)/300
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x))

        c = m*(xb-xa)
        xa = xb
        xb = xa+800
        m = (1500+200*self._d-c)/800
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

        c = m*(xb-xa)+c
        xa = xb
        xb = xa+300
        m = -float(200)/300
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

        c = m*(xb-xa)+c
        xa = xb
        xb = xa+500
        m = (550-100*self._d)/500
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

        c = m*(xb-xa)+c
        xa = xb
        m = -m
        for x in range(0, self._w-self.__scl_x(xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

    def __scl_x(self, x):
        return int(float(x)/self._dh)

    def __scl_y(self, y):
        return int(float(y)/self._dh)

    def __inv_y(self, y):
        return self._h - 1 - y



    def base_case(self, t):
        self._temp = Temperature(t)
        for y in range(self._h):
            for x in range(self._w):
                self._matrix[y][x] = self._temp.get_atm(self.__inv_y(y)*self._dh)
        
        self._get_border()
        for x in range(self._w):
            for y in range(self._h):
                if y > self._m_border[x]:
                    self._matrix[y][x] = np.nan

        for y in range(self._h):
            for x in range(self._w):
                if y > self._m_border[x]:
                    break
                xy = np.isnan(self._matrix[y][x])
                y_m1 = np.isnan(self._matrix[min(y+1, self._h-1)][x])
                x_m1 = np.isnan(self._matrix[y][x-1])
                x_p2 = np.isnan(self._matrix[y][min(self._w-1,x+1)])
                if y <= self._m_border[x] and (xy or y_m1 or x_m1 or x_p2):
                    h = self._dh*(self._h-1-y)
                    self._matrix[y][x] = self._temp.get_cont(h)

        for x in range(self._w):
            if self._m_border[x] < self._h-1:
                break
            if self._m_border[x] == self._h-1:
                self._matrix[self._h-1][x] = self._temp.get_plant()

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.imshow(self._matrix, interpolation='none')
        plt.colorbar(cax)
        plt.show()



m = Mountain(2000,  4000, 10, 991)
m.base_case(0)
m.plot()