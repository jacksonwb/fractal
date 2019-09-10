#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  Mandelbrot.py                                                               #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Monday Sep 2019 3:40:44 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import src.numba_mandelbrot as numba_mandelbrot

class Fractal:
	def __init__(self, axes, w, h, x_min, x_max, y_min, y_max, max_iter = 15, kernel = 'nb'):
		self.axes = axes
		self.max_iter = max_iter
		self.iter_boost = 0
		self.init_vals = [x_min, x_max, y_min, y_max, max_iter]
		self.w = w
		self.h = h
		self.x_min = x_min
		self.x_max = x_max
		self.y_min = y_min
		self.y_max = y_max
		self.scale = 1
		self.left_click = False
		self.right_click = False
		self.kernel = {'np':self.mandelbrot_np, 'nb':self.mandelbrot_nb}
		self.active_kernel = kernel
		self.image = self.axes.imshow(self.kernel[self.active_kernel](self.w, self.h, x_min, x_max, y_min, y_max))

	def reset(self):
		self.x_min = self.init_vals[0]
		self.x_max = self.init_vals[1]
		self.y_min = self.init_vals[2]
		self.y_max = self.init_vals[3]
		self.max_iter = self.init_vals[4]
		self.iter_boost = 0
		self.render()

	def translate(self, x, y):
		x_delta = (x / self.w) * (self.x_max - self.x_min)
		y_delta = (y / self.h) * (self.y_max - self.y_min)
		self.x_min, self.x_max = self.x_min + x_delta, self.x_max + x_delta
		self.y_min, self.y_max = self.y_min + y_delta, self.y_max + y_delta

	def zoom(self, factor):
		center = ((self.x_max - self.x_min) / 2 + self.x_min, (self.y_max - self.y_min) / 2 + self.y_min)
		radius = (self.x_max - self.x_min) / 2
		radius = radius * factor
		self.max_iter = min(15 + 2 * np.cbrt(1 / radius), 100)
		self.x_max = center[0] + radius
		self.x_min = center[0] - radius
		self.y_max = center[1] + radius
		self.y_min = center[1] - radius

	def mandelbrot_numpy_kernel(self, w, h, x_min, x_max, y_min, y_max, max_iter):
		x = np.linspace(x_min, x_max, w)
		y = np.linspace(y_min, y_max, h) * 1j
		c = x + y.reshape(len(y), 1)
		z = c
		div_time =  max_iter + np.zeros(c.shape, dtype=np.uint8)

		for i in range(int(max_iter)):
			z = z ** 2 + c
			div = z * np.conj(z) > 4
			div_now = div & (div_time==max_iter)
			div_time[div_now] = i
			z[div] = 2
		return div_time

	def mandelbrot_np(self, w, h, x_min, x_max, y_min, y_max):
		iter_val = self.max_iter + self.iter_boost
		return self.mandelbrot_numpy_kernel(w, h, x_min, x_max, y_min, y_max, iter_val)

	def mandelbrot_nb(self, w, h, x_min, x_max, y_min, y_max):
		iter_val = self.max_iter + self.iter_boost
		return numba_mandelbrot.mandelbrot_numba_kernel(w, h, x_min, x_max, y_min, y_max, iter_val)

	def render(self):
		self.image.set_data(self.kernel[self.active_kernel](self.w, self.h, self.x_min, self.x_max, self.y_min, self.y_max))
		self.image.autoscale()
		self.image.figure.canvas.draw()

	def toggle_kernel(self):
		if self.active_kernel == 'nb':
			print('Set kernel to numpy')
			self.active_kernel = 'np'
		else:
			self.active_kernel = 'nb'
			print('set kernel to numba')

	def set_color_map(self, value):
		color_maps = ['viridis', 'twilight_shifted', 'ocean', 'Greys']
		self.image.cmap = plt.get_cmap(color_maps[value])
		self.render()