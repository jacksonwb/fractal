#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  fractal.py                                                                  #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import argparse
import numpy as np
import tkinter
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

XMIN = -2.5
XMAX = 1.5
YMIN = -2
YMAX = 2
MAXITER = 15

RUN = True

mpl.use("TkAgg")

def parse():
	parser = argparse.ArgumentParser(description='Fractal Renderer')
	parser.add_argument('w', type=int)
	parser.add_argument('h', type=int)
	return parser.parse_args()

def _quit():
	global RUN
	RUN = False     # stops mainloop
	root.destroy()  # this is necessary on Windows to prevent

class Fractal:
	def __init__(self, axes, w, h, x_min, x_max, y_min, y_max, max_iter = 15):
		self.axes = axes
		self.max_iter = max_iter
		self.iter_boost = 0
		self.w = w
		self.h = h
		self.x_min = x_min
		self.x_max = x_max
		self.y_min = y_min
		self.y_max = y_max
		self.scale = 1
		self.image = self.axes.imshow(self.mandelbrot(self.w, self.h, x_min, x_max, y_min, y_max))
		self.left_click = False
		self.right_click = False

	def reset(self):
		self.x_min = XMIN
		self.x_max = XMAX
		self.y_min = YMIN
		self.y_max = YMAX
		self.max_iter = MAXITER
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
		print('factor:', np.sqrt(1 / radius))
		print('max_iter:', self.max_iter + self.iter_boost)
		self.x_max = center[0] + radius
		self.x_min = center[0] - radius
		self.y_max = center[1] + radius
		self.y_min = center[1] - radius

	def mandelbrot(self, w, h, x_min, x_max, y_min, y_max):
		max_iter = int(self.max_iter) + int(self.iter_boost)
		print(max_iter)
		x = np.linspace(x_min, x_max, w)
		y = np.linspace(y_min, y_max, h) * 1j
		c = x + y.reshape(len(y), 1)
		z = c
		div_time =  max_iter + np.zeros(c.shape, dtype='int')

		for i in range(max_iter):
			z = z ** 2 + c
			div = z * np.conj(z) > 2 ** 2
			div_now = div & (div_time==max_iter)
			div_time[div_now] = i
			z[div] = 2
		return div_time

	def render(self):
		self.image.set_data(self.mandelbrot(self.w, self.h, self.x_min, self.x_max, self.y_min, self.y_max))
		self.image.autoscale()
		self.image.figure.canvas.draw()


def on_key_press(event):
	if event.key == 'escape':
		_quit()
	if event.key == 'r':
		fractal.reset()
	if event.key == '=':
		fractal.iter_boost = min(fractal.iter_boost + 1, 100)
		fractal.render()
	if event.key == '-':
		fractal.iter_boost = max(fractal.iter_boost - 1, 0)
		fractal.render()

def on_click(event, fractal):
	if event.button == 1:
		fractal.left_click = (event.x, event.y)
	if event.button == 3:
		fractal.right_click = (event.x, event.y)

def on_move(event, fractal):
	if fractal.left_click and isinstance(event.xdata, np.float64):
		y_click = fractal.h - event.ydata
		fractal.translate(fractal.left_click[0] - event.xdata, -fractal.left_click[1] + y_click)
		fractal.left_click = (event.xdata, y_click)
		fractal.render()
	if fractal.right_click and isinstance(event.xdata, np.float64):
		y_click = fractal.h - event.ydata
		factor = 1 - (fractal.right_click[1] - y_click) / fractal.h
		fractal.zoom(factor)
		fractal.right_click = (event.xdata, y_click)
		fractal.render()

def on_release(event, fractal):
	if event.button == 1:
		fractal.left_click = None
	if event.button == 3:
		fractal.right_click = None

if __name__ == '__main__':
	args = parse()
	dpi = 200

	root = tkinter.Tk()
	root.wm_title("Fractal")
	root.resizable(width=False, height=False)

	fig = Figure(figsize=(args.w/dpi, args.h/dpi), dpi=dpi)
	fig.subplots_adjust(0,0,1,1)
	ax = fig.add_subplot(111)
	ax.axis('off')
	fractal = Fractal(ax, args.w, args.h, XMIN, XMAX, YMIN, YMAX, MAXITER)

	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
	canvas.mpl_connect("key_press_event", on_key_press)
	canvas.mpl_connect("button_press_event", lambda x: on_click(x, fractal))
	canvas.mpl_connect("button_release_event", lambda x: on_release(x, fractal))
	canvas.mpl_connect("motion_notify_event", lambda x: on_move(x, fractal))

	canvas.draw()
	while RUN:
		try:
			root.update_idletasks()
			root.update()
		except UnicodeDecodeError:
			print("Caught Scroll Error")
	# tkinter.mainloop()