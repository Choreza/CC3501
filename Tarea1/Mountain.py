import numpy as np
import matplotlib.pyplot as plt
import tqdm 
from Temperature import Temperature

class Mountain:
    def __init__(self, height, width, dh, tol, digits):
        self._d = float(digits)/1000

        self._height = height
        self._width = width
        self._dh = dh

        self._h = int(float(self._height)/self._dh)
        self._w = int(float(self._width)/self._dh)

        self._matrix = np.zeros((self._h, self._w))
        
        self.tol = tol

        self.laplace = True

    def __get_border(self):

        # Lista que, dado un x guarda el y del borde de la montana
        self._m_border = []
        
        # Primer tramo: el mar
        xa = 0
        xb = 1200+400*self._d
        for x in range(0, self.__scl_x(xb)):
            self._m_border.append(self._h)

        # Segundo tramo: la planta
        xa = xb
        xb = xa+120
        for x in range(self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(0))

        # Tercer tramo: inclinacion pequena
        xa = xb
        xb = xa+280
        m = float(100)/300
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x))

        # Cuarto tramo: primera gran inclinacion ascendente
        c = m*(xb-xa)
        xa = xb
        xb = xa+800
        m = (1500+200*self._d-c)/800
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

        # Quinto tramo: primera inclinacion desdendente
        c = m*(xb-xa)+c
        xa = xb
        xb = xa+300
        m = -float(200)/300
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

        # Sexto tramo: segunda gran inclinacion ascendente
        c = m*(xb-xa)+c
        xa = xb
        xb = xa+500
        m = (550-100*self._d)/500
        for x in range(0, self.__scl_x(xb-xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

        # Septimo tramo: Ultima inclinacion desdendente
        c = m*(xb-xa)+c
        xa = xb
        m = -m
        for x in range(0, self._w-self.__scl_x(xa)):
            self._m_border.append(self.__inv_y(m*x+self.__scl_x(c)))

        # Si no se alcanzo a completar el ancho de la matriz, se rellena
        # con el ultimo valor agregado
        while len(self._m_border) < self._w:
            self._m_border.append(self._m_border[len(self._m_border)-1])
        

    def __scl_x(self, x):
        return int(float(x)/self._dh)

    def __scl_y(self, y):
        return int(float(y)/self._dh)

    def __inv_y(self, y):
        return self._h - 1 - y


    def near_nan(self, x, y):
        if np.isnan(self._matrix[max(y-1, 0)][x]):
            return True    
        if np.isnan(self._matrix[min(y+1, self._h-1)][x]):
            return True
        if np.isnan(self._matrix[y][max(0,x-1)]):
            return True
        if np.isnan(self._matrix[y][min(self._w-1,x+1)]):
            return True
        return False


    def __single_iteration(self, old_mat, new_mat, omega):
        
        # Valor maximo de rij 
        max_prom = 0
        for x in range(self._w):
            for y in range(self._h):
                # Si la coordenada actual es NaN, se detiene
                if np.isnan(old_mat[y][x]):
                    continue
    
                prom = 0
                # Posicion actual no toca los bordes, incluyendo los bordes de la montana y el mar
                if 0 < x < self._w-1 and 0 < y < self._h-1:
                    
                    # Caso en que no esta rodeado de NaN
                    if not(self.near_nan(x, y)):
                        prom = 0.25*(old_mat[y+1][x] + old_mat[y][x+1] + old_mat[y-1][x] + 
                                 old_mat[y][x-1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)

                    # Solamente valor inferior es NaN
                    elif np.isnan(old_mat[y+1][x]) and not(np.isnan(old_mat[y][x+1])) and not(np.isnan(old_mat[y][x-1])):
                        prom = 0.25*(2*old_mat[y-1][x]+old_mat[y][x-1]+old_mat[y][x+1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)

                    # Solamente valor derecho es NaN
                    elif not(np.isnan(old_mat[y+1][x])) and np.isnan(old_mat[y][x+1]) and not(np.isnan(old_mat[y][x-1])):
                        prom = 0.25*(old_mat[y+1][x]+old_mat[y-1][x]+2*old_mat[y][x-1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)

                    # Solamente valor izquierdo es NaN
                    elif not(np.isnan(old_mat[y+1][x])) and not(np.isnan(old_mat[y][x+1])) and np.isnan(old_mat[y][x-1]):
                        prom = 0.25*(old_mat[y+1][x]+old_mat[y-1][x]+2*old_mat[y][x+1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)

                    # Lado izquierdo y abajo NaN
                    elif np.isnan(old_mat[y+1][x]) and not(np.isnan(old_mat[y][x+1])) and np.isnan(old_mat[y][x-1]):
                        prom = 0.25*(2*old_mat[y-1][x]+2*old_mat[y][x+1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)

                    # Lado derecho y abajo NaN
                    elif np.isnan(old_mat[y+1][x]) and np.isnan(old_mat[y][x+1]) and not(np.isnan(old_mat[y][x-1])):
                        prom = 0.25*(2*old_mat[y-1][x]+2*old_mat[y][x-1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)


                # Borde superior
                elif 0 < x < self._w-1 and y == 0:
                    prom = 0.25*(old_mat[y][x+1] + 2*old_mat[y+1][x] + 
                        old_mat[y][x-1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2) 

                # Borde izquierdo
                elif x == 0 and 0 < y < self._h-2:
                    prom = 0.25*(old_mat[y+1][x] + 2*old_mat[y][x+1] - 4*old_mat[y][x] +
                        old_mat[y-1][x]- self.__rho(x,y)*self._h**2)

                # Borde derecho
                elif x == self._w-1 and 0 < y <= self._m_border[x]:
                    if not(self.near_nan(x, y)):
                        prom = 0.25*(old_mat[y+1][x] + 2*old_mat[y][x-1] - 4*old_mat[y][x] +
                                old_mat[y-1][x]- self.__rho(x,y)*self._h**2)

                    # Solamente abajo es NaN
                    if np.isnan(old_mat[y+1][x]) and not(np.isnan(old_mat[y][x-1])):
                        prom = 0.25*(2*old_mat[y-1][x]+2*old_mat[y][x-1] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)

                    # Si abajo y a la izquierda es NaN
                    if np.isnan(old_mat[y+1][x] and np.isnan(old_mat[y][x-1])):
                        prom = 0.25*(4*old_mat[y-1][x] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2)

                # Esquina superior izquierda
                elif x == 0 and y == 0:
                    prom = 0.25*(2*old_mat[y+1][x] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2 +
                            2*old_mat[y][x+1])

                # Esquina superior derecha
                elif x == 0 and y == 0:
                    prom = 0.25*(2*old_mat[y+1][x] - 4*old_mat[y][x] - self.__rho(x,y)*self._h**2 +
                            2*old_mat[y][x-1])

                else:
                    continue

                new_mat[y][x] = old_mat[y][x] + prom*omega
                max_prom = max(max_prom, abs(prom))
        return max_prom


    def start(self, omega):

        # Matriz que guarda los nuevos valores de la iteracion
        new_mat = np.copy(self._matrix)

        # Numero de iteraciones
        n_iters = 0

        run = True
        omega = omega-1

        if not (0 <= omega <= 1):
            raise Exception("Omega tiene un valor incorrecto")

        # Se fija un numero de iteraciones
        max_iters = 1500
        while run and n_iters < max_iters:

            # Se actualiza la matriz vieja, para calcular la nueva
            old_mat = np.copy(new_mat)

            # Se obtiene el rij maximo de la iteracion
            r_max = self.__single_iteration(old_mat, new_mat, omega)
            
            n_iters += 1
            print(n_iters, r_max)
            if r_max < self.tol:
                run = False

        self._matrix = np.copy(new_mat)
        return n_iters

    def base_case(self, t):
        # Guarda el ultimo caso base
        self._last_t = t
        self._temp = Temperature(t)

        # Calcula la temperatura atmosferica
        for x in range(self._w):
            for y in range(self._h):
                self._matrix[y][x] = self._temp.get_atm(self.__inv_y(y)*self._dh)
        
        # Se calcula el borde de la montana
        self.__get_border()

        # Rellena con NaN el interior de la montana
        for x in range(self._w):
            for y in range(self._h):
                if y > self._m_border[x]:
                    self._matrix[y][x] = np.nan

        # Inicializa la temperatura del borde de la montana
        for x in range(self._w):
            for y in range(self._h):                
                
                # Se verifica que, este en el borde, o que algun vecino sea NaN
                if y <= self._m_border[x] and self.near_nan(x, y):
                    h = self._dh*(self._h-1-y)
                    self._matrix[y][x] = self._temp.get_cont(h)
                   


        # Inicializa la temperatura de la planta
        for x in range(self._w):

            # Si la altura es superior a la de la planta, se detiene
            if self._m_border[x] < self._h-1:
                break
            
            # Si la altura es la de la planta, la calcula
            if self._m_border[x] == self._h-1:
                self._matrix[self._h-2][x] = self._temp.get_atm(self.__inv_y(y)*self._dh)
                self._matrix[self._h-1][x] = self._temp.get_plant()


    def reset(self):
        self._matrix = np.zeros((self._h, self._w))
        self.base_case(self._last_t)

   
    def __rho(self, x, y):
        if self.laplace:
            return 0
        return 1.0/(x**2 + y**2 + 120)**0.5

    def w_optimo(self):
        """
        Retorna el w optimo
        :return:
        """
        return 4/(2+(np.sqrt(4-(np.cos(np.pi/(self._w-1)) + np.cos(np.pi/(self._h-1)))**2)))
        
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.imshow(self._matrix, interpolation='none')
        plt.colorbar(cax)
        plt.show()



m = Mountain(2000,  4000, 10, 0.001, 991)
m.base_case(16)
m.start(m.w_optimo())
print(m.w_optimo())
m.plot()