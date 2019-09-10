#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  numba_mandelbrot.py                                                         #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Monday Sep 2019 2:12:37 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #
import numpy as np
from numba import jit

@jit(nopython=True)
def mandel(x, y, max_iters):
	"""
	Given the real and imaginary parts of a complex number,
	determine if it is a candidate for membership in the Mandelbrot
	set given a fixed number of iterations.
	"""
	i = 0
	c = complex(x,y)
	z = 0.0j
	for i in range(max_iters):
		z = z*z + c
		if (z.real*z.real + z.imag*z.imag) >= 4:
			return i

	return max_iters

@jit(nopython=True)
def create_fractal(w, h, min_x, max_x, min_y, max_y, iters):
	height = h
	width = w
	image = np.zeros((w, h), dtype=np.uint8)

	pixel_size_x = (max_x - min_x) / width
	pixel_size_y = (max_y - min_y) / height
	for x in range(width):
		real = min_x + x * pixel_size_x
		for y in range(height):
			imag = min_y + y * pixel_size_y
			color = mandel(real, imag, iters)
			image[y, x] = color

	return image

def mandelbrot_numba_kernel(w, h, x_min, x_max, y_min, y_max, max_iters):
	image = create_fractal(w, h, x_min, x_max, y_min, y_max, max_iters)
	return (image)

if __name__ == "__main__":
	XMIN = -2.5
	XMAX = 1.5
	YMIN = -2
	YMAX = 2
	from matplotlib.pylab import imshow, jet, show, ion
	image = mandelbrot_numba_kernel(400, 400, XMIN, XMAX, YMIN, YMAX, 15)
	print(image)
	print(image.dtype)
	imshow(image)
	show()