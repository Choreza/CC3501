from Mountain import Mountain
import matplotlib.pyplot as plt
import time

class Plotter:
	def __init__(self, mountain, max_iters):
		self._mountain = mountain
		self._max_iters = max_iters
		
	def plot_cmp_omegas(self, time, omegas):
		for w in omegas:
		    self._mountain.base_case(time)
		    self._mountain.start(w, self._max_iters)
		    self._mountain.plot()

	def plot_cmp_hours(self, omega, times):
		temp = []
		for t in times:
			self._mountain.base_case(t)
			self._mountain.start(self._mountain.w_optimo(), self._max_iters)
			temp.append(self._mountain.mean_temp())

		plt.plot(times, temp, 'ro')
		plt.title("Temperatura Promedio para distintos momentos del día (W="+(str(omega)+"0000")[0:3]+")")
		plt.xlabel("Horas del día [h]")
		plt.ylabel("Temperatura Promedio Atmosférica [°Celsius]")
		plt.savefig("figures/meantemp-w"+(str(omega)+"0000")[0:3]+".png")
		plt.close()

	def plot_exec_time(self, time, omegas):		
		exec_times = []
		for w in omegas:
			self._mountain.base_case(time)

			start_time = self.__currmillis()
			self._mountain.start(w, self._max_iters)
			execution_time = self.__currmillis() - start_time

			exec_times.append(execution_time)

		plt.plot(omegas, exec_times, 'ro')
		plt.title("Tiempo de Ejecución para distintos Omegas (t="+str(time)+")")
		plt.xlabel("Omegas")
		plt.ylabel("Tiempo de Ejecución [s]")
		plt.savefig("figures/exectimes-t"+str(time)+".png")
		plt.close()

	def __currmillis(self):
		return int(round(time.time() * 1000))