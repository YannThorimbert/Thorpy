"""VarSet is used when you need to acess some non-constant variable that could
have been modified by the user through the GUI interface during execution.
"""

##from collections import namedtuple

from thorpy._utils.functions import obtain_valid_object
from thorpy.elements.slidersetter import SliderXSetter
from thorpy.elements.inserter import Inserter
from thorpy.elements.checker import Checker
from thorpy.elements.colorsetter import ColorSetter
from thorpy.elements.launchers.colorsetterlauncher import ColorSetterLauncher
from thorpy.elements.browser import Browser
from thorpy.elements.browserlight import BrowserLight
from thorpy.elements.paramsetter import ParamSetter
from thorpy.elements.launchers.dropdownlistlauncher import DropDownListLauncher


def get_handler_for(variable):
    type_ = type(variable.value)
    value = variable.value
    text = variable.text
    limits = variable.limits
    handler_type = variable.handler_type
    more = variable.more
    handler = None
    if handler_type:
        if handler_type == "color choice":
##            cs = ColorSetter(text=text, value=value)
            handler = ColorSetterLauncher(value, text)
        elif handler_type == "file choice":
            limits.setdefault("launcher", False)
            limits.setdefault("light", True)
            limits.setdefault("ddl_size", None)
            limits.setdefault("folders", True)
            limits.setdefault("file_types", None)
            limits.setdefault("files", True)
            if limits["light"]:
                handler = BrowserLight(text=text, path=value,
                                     ddl_size=limits["ddl_size"],
                                     folders=limits["folders"],
                                     files=limits["files"],
                                     file_types=limits["file_types"])
            else:
                handler = Browser(text=text, path=value,
                                 ddl_size=limits["ddl_size"],
                                 folders=limits["folders"],
                                 files=limits["files"],
                                 file_types=limits["file_types"])
        else:
            handler = obtain_valid_object(handler_type, value=value, type_=type_,
                                          text=text, limits=limits)
    elif type_ is tuple:
        if len(value) == 3:
##            handler = ColorSetter(text=text, value=value)
            handler = ColorSetterLauncher(value, text, finish=False)
    elif type_ is list:
        var_text = more.get("var_text", value[0])
        ddlf_size = more.get("ddlf_size", "auto")
        handler = DropDownListLauncher(const_text=text, var_text=var_text,
                                        titles=value, ddlf_size=ddlf_size,
                                        finish=False)
    elif ((type_ is str) or not(limits)) and not(type_ is bool):
        if not(limits) or isinstance(limits,str):
            ilimits = (None, None)
        else:
            ilimits = limits
        handler = Inserter(text, value=str(value), value_type=type_,
                            size=ilimits, finish=False)
        if limits == "float":
            handler.numeric_only = True
            handler.int_only = False
            handler._value_type = float
        elif limits == "int":
            handler.numeric_only = True
            handler.int_only = True
            handler._value_type = int
    elif (type_ is int) or (type_ is float):
        length = more.get("length", 100)
        handler = SliderXSetter(length,
                                limits,
                                text,
                                type_=type_,
                                initial_value=value,
                                finish=False)
    elif type_ is bool:
        handler = Checker(variable.text, value=variable.value, finish=False)
    if handler:
        handler.rank = variable.rank
        return handler
    else:
        raise Exception(
            "Variable doesn't have default handler: " +
            str(text))

class Variable(object):
    """Basic type for Varsetter's variables."""

    def __init__(self, value, text, limits, handler_type, rank, help_text, more):
        self.value = value
        self.text = text
        self.limits = limits
        self.handler_type = handler_type
        self.rank = rank
        self.help_text = help_text
        self.more = more

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class LinkedVariable(Variable):
    """Use this if you need to link an object's variable to the Varsetter."""

    def __init__(self, father, name, text, limits, handler_type, rank,
                    help_text):
        father_value = getattr(father, name)
        Variable.__init__(self, father_value, text, limits, handler_type, rank,
                            help_text)
        self.father = father
        self.name = name

    def set_value(self, value):
        Variable.set_value(self, value)
        setattr(self.father, self.name, value)


class FuncLauncher(Variable):
    """Use this if you need to execute a function just after setting the value.
    """

    def __init__(
            self,
            func,
            dictargs,
            value,
            text,
            limits,
            handler_type,
            rank,
            help_text):
        Variable.__init__(self, value, text, limits, handler_type, rank, help_text)
        self.func = func
        self.dictargs = dictargs


class PostFuncLauncher(FuncLauncher):

    def set_value(self, value):
        Variable.set_value(self, value)
        self.func(self.dictargs)


class PreFuncLauncher(FuncLauncher):

    def set_value(self, value):
        self.func(self.dictargs)
        Variable.set_value(self, value)


class VarSet(object):
    """Dynamically creates attributes so that one can acess them as if they were
    variables of a module.
    """

    EXCEPTION_TEXT = "Tried to name a variable like a built-in attribute"+\
                      " or method. Please use the syntax hack provided by"+\
                      " thorpy. It is also possible that you try to add a"+\
                      " key that already exist. In that case use the method"+\
                      " set_variable of this object."""

    def __init__(self, variables=None):
        if not variables:
            variables = {}
        self.variables = variables
        self._current_rank = -1

    def add(self, varname, value, text, limits=None, handler_type=None,
            rank=None, help_text=None, more=None):
        rank = self._get_rank() if rank is None else rank
        if more is None : more = {}
        if not varname in self.__dict__:
            v = Variable(value, text, limits, handler_type, rank, help_text, more)
            self.variables[varname] = v
            self.__dict__[varname] = v.get_value()
        else:
            raise Exception(VarSet.EXCEPTION_TEXT)

    def add_link(self, varname, obj, text, limits=None, handler_type=None,
                 rank=None, help_text=None, more=None):
        """Use this if you need to link an object's variable to the Varsetter.
        """
        rank = self._get_rank() if rank is None else rank
        if more is None : more = {}
        if not varname in self.__dict__:
            v = LinkedVariable(obj, varname, text, limits, handler_type, rank,
                                help_text, more)
            self.variables[varname] = v
            self.__dict__[varname] = v.get_value()
        else:
            raise Exception(VarSet.EXCEPTION_TEXT)

    def add_func(self, varname, func, dictargs, value, text, limits=None,
                 handler_type=None, rank=None, post=True, help_text=None,
                 more=None):
        """Use this if you need to execute a function just before/after
        setting the value.
        """
        rank = self._get_rank() if rank is None else rank
        if more is None : more = {}
        if not varname in self.__dict__:
            if post:
                v = PostFuncLauncher(
                    func,
                    dictargs,
                    value,
                    text,
                    limits,
                    handler_type,
                    rank,
                    help_text,
                    more)
            else:
                v = PreFuncLauncher(
                    func,
                    dictargs,
                    value,
                    text,
                    limits,
                    handler_type,
                    rank,
                    help_text,
                    more)
            self.variables[varname] = v
            self.__dict__[varname] = v.get_value()
        else:
            raise Exception(VarSet.EXCEPTION_TEXT)

    def set_value(self, varname, value):
        self.variables[varname].set_value(value)
        setattr(self, varname, value)

    def get_value(self, varname):
        return self.variables[varname].get_value()

    def set_variable(self, varname, variable):
        self.variables[varname] = variable
        setattr(self, varname, variable.value)

##    def get_handlers(self):
##        handlers = {}
##        for varname in self.variables:
##            handler = get_handler_for(self.variables[varname])
##            handlers[varname] = handler
##        return handlers

    def get_handlers(self):
        handlers = {}
        for varname, variable in self.variables.items():
            handler = get_handler_for(variable)
            handlers[varname] = (handler, variable)
        return handlers

    def _get_rank(self):
        self._current_rank += 1
        return self._current_rank

    def create_paramsetter(self, name_txt="", launched_txt="", box_els=None):
        box_els = [] if not box_els else box_els
        ps = ParamSetter([self], name_txt, launched_txt, box_els)
        ps.finish()
        return ps