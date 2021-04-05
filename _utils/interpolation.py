import math

def get_y_quad(x, beg, end, M): #quadratic interpolation
    W = end - beg
    actual_x = x - beg
    return M*actual_x*(2-actual_x/W)/W

def get_y_linear(x, beg, end, M): #linear interpolation
    return (x-beg) * M / (end-beg)

def get_y_exp(x, beg, end, M, B=1.):
    W = end - beg
    actual_x = x - beg
    A = M / (math.exp(B*W) - 1.)
    return A * (math.exp(B*actual_x) - 1.)


_functions = {"linear":get_y_linear,
              "quadratic":get_y_quad,
              "exponential":get_y_exp}

def get_y(x, beg, end, M=255, before=0, after=255, mode="linear"):
    if x < beg:
        return before
    elif x > end:
        return after
    return _functions[mode](x,beg,end,M)