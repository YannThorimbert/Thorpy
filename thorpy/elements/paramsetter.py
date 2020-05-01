from thorpy.elements.box import Box
from thorpy.miscgui import style
from thorpy.elements.launchers.dropdownlistlauncher import DropDownListLauncher


class ParamSetter(Box):
    """Put automatically defined elements in a box, in order to set variables.
    """

    @staticmethod
    def make(varsets, elements=None, size=None):
        ps = ParamSetter(varsets, elements, size=size, finish=False)
        ps.finish()
        return ps

    def __init__(self,
                 varsets,
                 elements=None,
                 normal_params=None,
                 size=None,
                 bar=None,
                 file_width=None,
                 finish=True):
        if file_width is None: file_width = style.FILE_WIDTH
##        box_size = style.BOX_SIZE if box_size is None else box_size
        self.scale_list = [DropDownListLauncher] #!paramsetter
        self.varsets = varsets
        if not isinstance(self.varsets, list):
            self.varsets = [self.varsets]
        self.handlers = self.get_handlers() #below, will deny them so they know self
        elements = [] if elements is None else elements
        elements += self.handlers.values()
        Box.__init__(self, elements=elements, normal_params=normal_params,
                        size=size, finish=False)
        if finish:
            self.finish()



    def get_handlers(self):
        """Returns a dictionnary of pairs (i, varname) containing elements."""
        handlers = {}
        for (i, v) in enumerate(self.varsets):
            v_handlers = v.get_handlers()
            for (varname, handler) in iter(v_handlers.items()):
                handler_element, variable = handler
                handler_element.finish()
                if handler_element.__class__ in self.scale_list:
                    handler_element.scale_to_title()
                if variable.help_text:
                    add_basic_help(handler_element, variable.help_text)
                handlers[(i, varname)] = handler_element
        return handlers


##    def reinit_handlers(self):
##        """Returns a dictionnary of pairs (i, varname) containing elements."""
##        handlers = {}
##        for (i, v) in enumerate(self.varsets):
##            v_handlers = v.get_handlers()
##            for (varname, handler) in iter(v_handlers.items()):
##                handler_element, variable = handler
##                handler_element.finish()
##                if variable.help_text:
##                    add_basic_help(handler_element, variable.help_text)
##                handlers[(i, varname)] = handler_element
##        for key in self.handlers:
##            old_handler = self.handlers[key]
##            new_handler = handlers[key]
##            self.replace_element(old_handler, new_handler)
##        self.handlers = handlers

    def reinit_handlers(self):
        """Returns a dictionnary of pairs (i, varname) containing elements."""
        for i, varname in self.handlers:
            value = self.varsets[i].get_value(varname)
            print(self.handlers[(i,varname)], value)
            self.handlers[(i,varname)].set_value(value)


    def save(self):
        for (varset, varname), handler in iter(self.handlers.items()):
            # si varset
            self.varsets[varset].set_value(varname, handler.get_value())
            # sinon si link
            # sinon si fonction

##    def reinit(self):
##        for (varset, varname), handler in iter(self.handlers.items()):
##            self.handlers.remove()
##            # si varset
##            self.varsets[varset].set_value(varname, handler.get_value())
