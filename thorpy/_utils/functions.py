"""Miscellaneous functions"""
from random import random

def obtain_valid_object(obj_class, **kwargs):
    """
    Try to obtain a valid instance of obj_class, using those args of kwargs that
    can be given to its __init__ function.
    """
    try:
        obj = obj_class(**kwargs)
    except TypeError:
        obj = obj_class()
        args_okay = {}
        for arg in kwargs:
            if hasattr(obj, arg):
                args_okay[arg] = kwargs[arg]
        obj = obj_class(**args_okay)
    return obj

def get_module_var(s):
    splitted = s.split(".")
    var = splitted[-1]
    modul = ".".join(splitted[:-1])
    return (modul, var)

def random_sign():
    if random() < 0.5:
        return -1
    else:
        return 1

def compress_array(array, new_size):
    """Compress array by averaging over fusionned cells"""
    l = len(array)
    k = l / new_size
    new_array = list()
    for i in range(0, l, k):
        val = sum(array[i:i+k]) / k
        new_array.append(val)
    return new_array


def void_function():
    pass


def get_keys_from_val(dic, val):
    """Get all keys from a value in a dictionnary"""
    toreturn = list()
    for key in dic:
        if dic[key] == val:
            toreturn.append(key)
    return toreturn

def flatten(x):
    """Returns 1D version of <x>"""
    from collections import Iterable
    if isinstance(x, Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

def regroup(tuples):
    """Tuples is a list of tuples.
    (0, lol), (1, truc), (0, bra) --> {0 : [lol, bra], 1 : [truc]}"""
    group = dict()
    existing = list()
    for t in tuples:
        if t[0] in existing:
            group[t[0]].append(t[1])
        else:
            existing.append(t[0])
            group[t[0]] = list([t[1]])
    return group

def fusion_dicts(d1, d2):
    """if d1[i] == d2[i], d[i] = d1[i]"""
    d = union_dicts(d1, d2)
    newd = dict()
    for k in d:
        newd[k] = d[k][0]
    return newd


def union_dicts(d1, d2):
    """Union dictionnaries.
    {1 : 2, 3 : 4} and {1 : 4, 8 : 6} ==> {8: [6], 1: [2, 4], 3: [4]}"""
    df = dict()
    for k in d1:
        df[k] = list([d1[k]])
    for k in d2:
        if k in df:
            df[k].append(d2[k])
        else:
            df[k] = list([d2[k]])
    return df

def union_dicts_list(dl):
    """Performs union_dicts on a whole list of dicts"""
    df = dl[0]
    for i in range(1, len(dl)):
        df = union_dicts(df, dl[i])
    for k in df:
        df[k] = flatten(df[k])
    return df


##d1 = {1 : 2, 3 : 4}
##d2 = {1 : 4, 8 : 6}
##d3 = {1 : 0, 12 : 34}
##print fusion_dicts(d1, d2)
##print union_dicts(d1, d2)
##print union_dicts_list([d1, d2, d3])

def get_func_limits(func, xvals, params=None):
    """Returns minimum and maximum of scalar function <func> in the range given
    by <xvals> and with optionnal <params>"""
    if params:
        yvals = list([func(x, *params) for x in xvals])
    else:
        yvals = list([func(x) for x in xvals])
    minimum = min(yvals)
    maximum = max(yvals)
    return (minimum, maximum)

def convert_array(array, type_):
    """Convert all elements in array to <typ>"""
    for i in range(len(array)):
        for j in range(len(array[i])):
            array[i][j] = type_(array[i][j])


def create_points_list(lists):
    """Transforms two lists values into a list of couple of values"""
    created = list()
    for i in range(len(lists[0])): #typically i in range(2)
        point = list()
        for l in lists: #for each coordinate
            point.append(l[i])
        created.append(point)
    return created


##def float_range(start, end,  step=1.):
##    """Like range() but for floats"""
##    i = start
##    l = list()
##    while i < end:
##        l.append(i)
##        i += step
##    return l

def float_xrange(start, end,  step=1., exceed=False):
    """Like range() but for floats"""
    i = start
    if exceed:
        more = step
    else:
        more = 0.
    while i < end + more:
        yield i
        i += step

def float_range(start, end,  step=1., exceed=False):
    """Returns a range list of float"""
    l = []
    i = start
    if exceed:
        more = step
    else:
        more = 0.
    while i < end + more:
        l.append(i)
        i += step
    return l

def max_index(l):
    """Returns the index of the max value"""
    m = -float("inf") - 1
    index = -1
    for i in range(len(l)):
        if l[i] > m:
            index = i
            m = l[i]
    return index

def min_index(l):
    """Returns the index of the min value"""
    m = float("inf")
    index = -1
    for i in range(len(l)):
        if l[i] < m:
            index = i
            m = l[i]
    return index


def tuple_addition(tuples):
    """Returns a list"""
    length = len(tuples[0])
    toReturn = list([0 for i in range(length)])
    for t in tuples:
        for i in range(length):
            toReturn[i] += t[i]
    return toReturn




##def oneTrueList(li, tru):
##    for el in li:
##        if el is tru:
##            el.state = True
##        else:
##            el.state = False
