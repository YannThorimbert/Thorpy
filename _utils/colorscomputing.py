"""Provides treatment of colors"""
import math
from random import random

from thorpy._utils.functions import random_sign

def get_alpha_color(c, alpha=None):
    if alpha is None:
        return c
    else:
        return (c[0], c[1], c[2], alpha)

def to_rgba(color):
    if len(color) == 3:
        return (color[0], color[1], color[2], 255)
    elif len(color) == 4:
        return color
    else:
        raise Exception("Invalid color argument")

def make_compatible(c1, c2):
    """Adapt c1 to c2"""
    if len(c1) < len(c2):
        return to_rgba(c1)
    else:
        return c1

def normalize_color(c):
    colors = [int(c[0]), int(c[1]), int(c[2])]
    for (i, color) in enumerate(colors):
        if color < 0:
            colors[i] = 0
        elif color > 255:
            colors[i] = 255
    return colors


def get_random_color(basis, mask):
    """For example, if mask[0] = 12, the red component of the color si in the
    range [basis[0] - mask, basis[0] + mask]
    """
    r = basis[0] + random_sign() * random() * mask[0]
    g = basis[1] + random_sign() * random() * mask[1]
    b = basis[2] + random_sign() * random() * mask[2]
    return normalize_color((r, g, b))

def square_color_norm(c):
    return c[0]**2 + c[1]**2 + c[2]**2

def color_norm(c):
    return math.sqrt(square_color_norm(c))

def lightness(c):
    return (max(c) + min(c)) / 2

def color_average(c):
    return sum(c) / 3

def luminosity(c):
    return 0.21*c[0] + 0.72*c[1] + 0.07*c[2]

def dot_product(v1, v2):
    """Returns the dot product of two vectors that are modeled as dicts"""
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def cosine_similarity(v1, v2):
    """Returns the cos similarity of two vectors that are modeled as dicts"""
    n1 = color_norm(v1)
    n2 = color_norm(v2)
    if n1 > 0. and n2 > 0.:
        product = dot_product(v1, v2)
        normalization = n1 * n2
        return product / normalization
    else:
##        return float(n1 == n2)
        return 0.

def different_color(c):
    return (c[0] + 10, c[1] + 10, c[2] + 10)

def negative_color(c):
    r = (c[0] + 127) % 256
    g = (c[1] + 127) % 256
    b = (c[2] + 127) % 256
    return (r, g, b)

def is_gray(c):
    return (c[0] == c[1] == c[2])

def mid_color(c1, c2):
    """Returns medium color between c1 and c2"""
    r = int(0.5 * (c1[0] + c2[0]))
    g = int(0.5 * (c1[1] + c2[1]))
    b = int(0.5 * (c1[2] + c2[2]))
    try:
        a = int(0.5 * (c1[3] + c2[3]))
        return (r, g, b, a)
    except IndexError:
        return (r, g, b)

def linear_combination(c1, c2, k1):
    """Returns medium color between c1 and c2"""
    k2 = 1. - k1
    r = int(k1*c1[0] + k2*c2[0])
    g = int(k1*c1[1] + k2*c2[1])
    b = int(k1*c1[2] + k2*c2[2])
    return (r,g,b)

def linear_combination_rgba(c1, c2, k1):
    """Returns medium color between c1 and c2"""
    k2 = 1. - k1
    r = int(k1*c1[0] + k2*c2[0])
    g = int(k1*c1[1] + k2*c2[1])
    b = int(k1*c1[2] + k2*c2[2])
    a = int(k1*c1[3] + k2*c2[3])
    return (r,g,b)

def difference(c1, c2):
    return (c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2])

def grow_color(factor, color):
    """grow a color"""
    red = factor * color[0]
    green = factor * color[1]
    blue = factor * color[2]
    return (red, green, blue)

scale_color = grow_color

def multiply_colors(c1, c2):
    return (c1[0] * c2[0], c1[1] * c2[1], c1[2] * c2[2])


class LinearInterpolation:
    """Liner interpolation"""

    def __init__(self, vals):
        self.parts = len(vals) - 1
        self.vals = vals
        self.build_functions()
        self.last_val = self.get_last_val()
        self.first_val = self.get_first_val()

    def build_function(self, couple1, couple2):
        gradient = (couple2[1] - couple1[1]) / (couple2[0] - couple1[0])
        y_intercept = couple1[1] - gradient * couple1[0]
        return (gradient, y_intercept)

    def build_functions(self):
        self.funcs = list()
        length = len(self.vals)
        if length == 1: #funcs is a single constant function
            self.funcs.append((0, self.vals[0][1]))
        else:
            for i in range(length-1):
                func = self.build_function(self.vals[i], self.vals[i+1])
                self.funcs.append(func)

##    def which_i(self, x_value):
##        i = 0
##        for couple in self.vals:
##            if couple < x_value:
##                return i - 1
##            else:
##                i += 1
##        return -1

    def which_i(self, x_value):
        if self.vals[0][0] >= x_value:
            return -1
        else:
            for i in range(len(self.vals)):
                if x_value < self.vals[i][0]:
                    return i - 1
            return -2


##    def which_i(self, x_value):
##        i = 0
##        while(x_value > self.vals[i][0]):
##            if i+2 >= len(self.vals):
##                i = -1
##                break
##            i += 1
##        return i

    def get_last_val(self):
        return self.vals[len(self.vals)-1][1]

    def get_first_val(self):
        return self.vals[0][1]

    def evaluate(self, x_value):
        i = self.which_i(x_value)
        if i == -1:
            return self.first_val
        elif i == -2:
            return self.last_val
        else:
            return self.funcs[i][0] * x_value + self.funcs[i][1]



class LinearColorRule:
    """Perform transformation from number to color"""

    def __init__(self, interpols=None):
        if not interpols:
            r = LinearInterpolation([(0., 0), (1., 255)])
            g = LinearInterpolation([(0., 0), (0.5, 255), (1., 0)])
            b = LinearInterpolation([(0., 255), (1., 0)])
            self.interpols = (r, g, b)
        else:
            self.interpols = interpols

    def get_color(self, value):
        r = self.interpols[0].evaluate(value)
        g = self.interpols[1].evaluate(value)
        b = self.interpols[2].evaluate(value)
        return (r, g, b)