#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  fractal.py                                                                  #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Friday Sep 2019 10:59:37 pm                                       #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import argparse
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

SPAN = 4
INIT_X_MIN = -2.5
INIT_X_MAX = INIT_X_MIN + SPAN

INIT_Y_MIN = -2
INIT_Y_MAX = 2

def parse():
	parser = argparse.ArgumentParser(description='Fractal Renderer')
	parser.add_argument('x')
	parser.add_argument('y')
	return parser.parse_args()

def mandelbrot(x, y, max_iter = 20):
	x = np.linspace(INIT_X_MIN, INIT_X_MAX, x)
	y = np.linspace(INIT_Y_MIN, INIT_Y_MAX, y) * 1j
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

if __name__ == '__main__':
	args = parse()
	mpl.rcParams['toolbar'] = 'None'
	plt.axis('off')
	fig = plt.figure()
	fig.tight_layout()
	plt.imshow(mandelbrot(args.x, args.y))
	plt.show()