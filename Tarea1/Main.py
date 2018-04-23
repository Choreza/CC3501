#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Mountain import Mountain
from Plotter import Plotter


#  Inicializa la montana
m = Mountain(2000, 4000, 20, 0.001, 991)

# Tiempos y omegas  agraficar
times = [0, 8, 12, 16, 20]
omegas = [1.1, 1.5, 1.8, 2.0]

# m.laplace = False #Descomentar para obtener ecuacion de Poisson

# Clase que grafica, segundo parametro indica numero de iteraciones
plt = Plotter(m, 1000)

# Se grafican distintas cosas, descomentar para ejecutar segun
# necesidad

#plt.plot_cmp_omegas(0, omegas)
#plt.plot_cmp_hours(m.w_optimo(), times)
#plt.plot_exec_time(0, omegas)