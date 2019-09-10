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
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.Mandelbrot import Fractal

XMIN = -2.5
XMAX = 1.5
YMIN = -2
YMAX = 2
MAXITER = 15
RUN = True
root = None

def parse():
	parser = argparse.ArgumentParser(description='Fractal Renderer')
	parser.add_argument('w', type=int)
	parser.add_argument('h', type=int)
	parser.add_argument('-k', '--kernel', choices=['np', 'nb'], default='nb')
	return parser.parse_args()

def _quit():
	global RUN
	RUN = False     # stops mainloop
	root.destroy()  # this is necessary on Windows to prevent

def on_key_press(event, fractal):
	if event.key == 'escape':
		_quit()
	if event.key == 'r':
		fractal.reset()
	if event.key == '=':
		fractal.iter_boost = min(fractal.iter_boost + 1, 100)
		print('increase iter_boost to:', fractal.iter_boost)
		fractal.render()
	if event.key == '-':
		fractal.iter_boost = max(fractal.iter_boost - 1, 0)
		print('decrease iter_boost to:', fractal.iter_boost)
		fractal.render()
	if event.key == 't':
		fractal.toggle_kernel()
		fractal.render()
	if event.key == '1':
		fractal.set_color_map(0)
	if event.key == '2':
		fractal.set_color_map(1)
	if event.key == '3':
		fractal.set_color_map(2)
	if event.key == '4':
		fractal.set_color_map(3)

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
		print('current iter_max: ', int(fractal.max_iter + fractal.iter_boost))

def on_release(event, fractal):
	if event.button == 1:
		fractal.left_click = None
	if event.button == 3:
		fractal.right_click = None

def on_close():
	_quit()

def run_fractal(width, height, kernel):
	dpi = 200

	global root
	root = tkinter.Tk()
	root.wm_title("Fractal")
	root.resizable(width=False, height=False)
	root.protocol('WM_DELETE_WINDOW', on_close)

	fig = Figure(figsize=(width/dpi, height/dpi), dpi=dpi)
	fig.subplots_adjust(0,0,1,1)
	ax = fig.add_subplot(111)
	ax.axis('off')
	fractal = Fractal(ax, width, height, XMIN, XMAX, YMIN, YMAX, MAXITER, kernel)

	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
	canvas.mpl_connect("key_press_event", lambda x: on_key_press(x, fractal))
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

if __name__ == '__main__':
	args = parse()
	run_fractal(args.w, args.h, args.kernel)