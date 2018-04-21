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

    def __get_border(self):
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
        # Guarda el ultimo caso base
        self._last_t = t
        self._temp = Temperature(t)

        # Calcula la temperatura atmosferica
        for y in range(self._h):
            for x in range(self._w):
                self._matrix[y][x] = self._temp.get_atm(self.__inv_y(y)*self._dh)
        
        # Se calcula el borde de la montana
        self.__get_border()

        # Rellena con NaN el interior de la montana
        for x in range(self._w):
            # Itera por bajo el borde solamente
            for y in range(int(self._m_border[x])+1, self._h):
                self._matrix[y][x] = np.nan

        # Inicializa la temperatura del borde de la montana
        for y in range(self._h):
            for x in range(self._w):

                # Si y esta bajo el borde, se detiene
                if y > self._m_border[x]:
                    break
                
                y_m1 = np.isnan(self._matrix[min(y+1, self._h-1)][x])
                x_m1 = np.isnan(self._matrix[y][x-1])
                x_p2 = np.isnan(self._matrix[y][min(self._w-1,x+1)])

                # Se verifica que, este en el borde, o que algun vecino sea NaN
                if y <= self._m_border[x] and (y_m1 or x_m1 or x_p2):
                    h = self._dh*(self._h-1-y)
                    self._matrix[y][x] = self._temp.get_cont(h)

        # Inicializa la temperatura de la planta
        for x in range(self._w):

            # Si la altura es superior a la de la planta, se detiene
            if self._m_border[x] < self._h-1:
                break
            
            # Si la altura es la de la planta, la calcula
            if self._m_border[x] == self._h-1:
                self._matrix[self._h-1][x] = self._temp.get_plant()

    def reset(self):
        self._matrix = np.zeros((self._h, self._w))
        self.base_case(self._last_t)

    def _single_iteration(self, matrix_new, matrix_old, omega):
        """
        Inicia calculo sólo 1 iteración
        :return:
        """
        for y in range(self._h):
            for x in range(self._w):
                # Si se cumple la condicion, la posiciones (x,y) son nan de ahi en adelante
                if y >= self._m_border[x]:
                    break

                # Valor anterior de la matriz promediado
                prom = 0

                # General
                if 1 < y < self._h - 2 and x < self._w - 2:
                    prom = 0.25 * (matrix_old[y - 1][x] + matrix_old[y + 1][x] + matrix_old[y][x - 1] +
                                   matrix_old[y][x + 1] - 4 * matrix_old[y][x])

                # Borde superior
                if y == 0 and x < self._w - 2:
                    prom = 0.25 * (2 * matrix_old[y + 1][x] + matrix_old[y][x - 1] +
                                   matrix_old[y][x + 1] - 4 * matrix_old[y][x])

                # Borde superior derecho
                if y == 0 and x == self._w - 1:
                    prom = 0.25 * (2 * matrix_old[y + 1][x] + 2 * matrix_old[y][x - 1] - 4 * matrix_old[y][x])

                # Borde superior izquierdo
                if y == 0 and x == 0:
                    prom = 0.25 * (2 * matrix_old[y + 1][x] + 2 * matrix_old[y][x + 1] - 4 * matrix_old[y][x])

               

                # Calcula nuevo valor
                matrix_new[y][x] = matrix_old[y][x] + prom * omega

    def w_optimo(self):
        """
        Retorna el w optimo
        :return:
        """
        return 4/(2+(math.sqrt(4-(math.cos(math.pi/(self._w-1)) + math.cos(math.pi/(self._h-1)))**2)))
        
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.imshow(self._matrix, interpolation='none')
        plt.colorbar(cax)
        plt.show()



m = Mountain(2000,  4000, 10, 991)
m.base_case(0)
m.plot()