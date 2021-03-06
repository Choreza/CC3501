#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class Temperature:
	def __init__(self, t):
		self._time = t

	def get_cont(self, y):
		"""
        Retorna la temperatura continental, dada una altura
        :return:
        """
		if y >= 1800:
			return 0
		else:
			return 20

	def get_sea(self):
		"""
        Retorna la temperatura del mar, segun la hora
        :return:
        """
		if self._time < 8:
			return 4
		elif 8 <= self._time < 16:
			return (self._time-8)*2 + 4
		else:
			return -(self._time-16)*2 + 20

	def get_plant(self):
		"""
        Retorna la temperatura de la planta, segun la hora
        :return:
        """
		return 400*(2 + np.cos(self._time*np.pi/float(12)))

	def get_atm(self, y):
		"""
        Retorna la temperatura atmosferica
        :return:
        """
		return -y*float(6)/1000 + self.get_sea()