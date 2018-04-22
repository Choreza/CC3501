from Mountain import Mountain
from Plotter import Plotter

m = Mountain(2000, 4000, 20, 0.001, 991)
times = [0, 8, 12, 16, 20]
omegas = [1.1, 1.5, 1.8, 2.0]

plt = Plotter(m, 2000)

plt.plot_cmp_omegas(0, omegas)
plt.plot_cmp_hours(m.w_optimo(), times)
plt.plot_exec_time(0, omegas)