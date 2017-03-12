"""Functions to handle files reading"""
from thorpy._utils.strhandler import convert_str, get_between_keys

def get_lines_as_list(filename, to_del='\n'):
    """Returns all the lines of the file in a list"""
    with open(filename, "r") as f:
        text = f.readlines()
    f.close()
    lines = list([])
    for i in range(len(text)):
        lines.append(text[i].rstrip(to_del))
    return lines

def get_data_as_2d_array(filename, delimiter=" ", to_del='\n'): #!convert (dernier argu) supprime
    """Suitable for data array"""
    data = list([])
    lines = get_lines_as_list(filename, to_del)
    for line in lines:
        splitted = line.split(delimiter)
        while '' in splitted:
            splitted.remove('')
        data.append(splitted)
    return data

def get_column_from_array(array, column, type_=float):
    l = list()
##    print len(array), len(array[0]), column
    for line in array:
        if line:
            value = type_(line[column])
            l.append(value)
    return l

def get_column_from_datafile(filename, column, sep=" ", type_=float):
    array = get_data_as_2d_array(filename, sep)
    return get_column_from_array(array, column, type_)

def get_data_name(filename, name, delimiter=" = ", stop=" "):
    lines = get_lines_as_list(filename)
    true_name = name + delimiter
    for line in lines:
        try:
            found = get_between_keys(line, true_name, stop)
            return found
        except:
            pass
    return -1


class ParamsLoader(object):

    def __init__(self, filename, attr, sep, comm, del_spaces=True,
                    del_comms=True, del_no_attr=True):
        """
        <attr> : attributor (e.g "=")
        <sep> : separator (e.g ",") ; defines a new line
        <comm> : comment (e.g "#")
        <del_spaces> : ignore all spaces
        <del_comms> : ignore all comments
        <del_no_attr> : ignore all line that don't contain <attr>"""
        self.filename = filename
        self.attr = attr
        self.sep = sep
        self.comm = comm
        self.text = self.get_txt(del_spaces, del_comms, del_no_attr)
        self.params = self.get_all_params()

    def get_txt(self, del_spaces, del_comms, del_no_attr):
        text = get_lines_as_list(self.filename, "")
        # 1
        if del_no_attr:
            for (numline, line) in enumerate(text):
                if not(self.attr in line):
                    text.pop(numline)
        # 2
        if del_comms:
            for numline in range(len(text)):
                beg = text[numline].find(self.comm)
                text[numline] = text[numline][:beg]
        # 3
        if del_spaces:
            for numline in range(len(text)):
                text[numline] = text[numline].replace(" ", "")
        # 4
        for (numline, line) in enumerate(text):
            if line.count(self.sep) > 1:
                newlines = text[numline].split(self.sep)
                text.pop(numline)
                for line in newlines:
                    text.insert(0, line)
        # 5
        while "" in text:
            text.remove("")
        return text

    def get_all_params(self, verbose=True):
        params = dict()
        for line in self.text:
            splitted = line.split("=")
            if len(splitted) == 2:
                if verbose:
                    if splitted[0] in params:
                        print(splitted[0] + " appears multiple time in file " +\
                                 self.filename + " !")
                params[splitted[0]] = splitted[1]
        return params

    def get(self, param, type_=str, typ2=int):
        if param in self.params:
            if type_ == int:
                value = float(self.params[param])
                return int(value)
            elif type_ == tuple or type_ == list:
                values = self.params[param]
                values = values.replace("(", "").replace(")", "").split(",")
                for i in range(len(values)):
                    values[i] = convert_str(values[i], typ2)
                return type_(values)
            else:
                return type_(self.params[param])
        else:
            raise Exception(param + " is not in file " + self.filename)

