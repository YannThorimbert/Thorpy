"""Philosophy :
    Initializer is used only in elements initialization. It contains a dict
    that stores all non-default value needed by user for the element considered.
    For common non-trivial elements, there is one Initializer instance per graphical
    possible state ; these instances shouldn't set non-graphical, or more
    generally non-state-related attributes. "normal_params" do it.

    It also set the default values for instanciating elements. For trivial
    attributes, this can be done directly into the element __init__ function
    with initializer.get(param, default_value). Indeed, all the get_* function
    of Initializer are for complex attributes to obtain (e.g fusionner, painter,
    ...).
"""

from thorpy.miscgui.title import Title
from thorpy.miscgui import functions, style, painterstyle
from thorpy.painting.fusionner import _Fusionner, FusionnerText
from thorpy.painting.writer import Writer

def _get_generic_object(obj, params):
    to_pop = list()
    for p in params:
        if params[p] is None:
            to_pop.append(p)
    for p in to_pop:
        params.pop(p)
    return obj(**params)


def init_params(argument):
    """Returns an initializer using <argument> if <argument> is a dict or None,
    else returns <argument>.
    """
    if not argument:
        return Initializer()
    elif isinstance(argument, dict):
        return Initializer(argument)
    else:
        return argument


class Initializer(object):

    def __init__(self, args=None):
        if not args:
            args = dict()
        self.params = args

    def _normalize(self, element):
        self.polite_set("txt", element.current_state.fusionner.title._text)

    def polite_set(self, name, value):
        """Set value to name if name is not in params, else do nothing.
        Almost equivalent to self.params.setdefault(name, value).
        """
        if not(name in self.params):
            self.params[name] = value

    def get_painter(self, painter=None):
        if "painter" in self.params:
            painter = self.params["painter"]
        elif not painter:
            painter = painterstyle.DEF_PAINTER(size=style.SIZE)
        paint_size = self.params.get("painter size")
        if paint_size:
            painter.size = paint_size
        return painter

    def get_fusionner(self):
        if "fusionner" in self.params:
            return self.params["fusionner"]
        else:
            painter = self.get_painter()
            title = self.get_title()
            colorkey = self.params.get("colorkey")
            params = {"painter": painter, "title": title,
                      "colorkey": colorkey}
            type_ = self.params.get("style")
            if type_ == "text":
                params.pop("painter")
                fusionner = _get_generic_object(FusionnerText, params)
                return fusionner
            elif type_ == "help":
                pain = functions.obtain_valid_painter(painterstyle.HELP_PAINTER,
                                                      size=style.HELP_SIZE,
                                                      color=style.DEF_HELP_COLOR)
                params["painter"] = self.get_painter(pain)
            elif type_ == "normal":
                pass
            elif type_:
                functions.debug_msg("Unknown style : " + str(type_))
            return _get_generic_object(_Fusionner, params)

    def get_title(self):
        if "title" in self.params:
            return self.params["title"]
        else:
            text = self.params.get("txt", "")
##            writer = self.params.get("writer")
            writer = self.get_writer()
            pos = self.params.get("txt pos")
            params = {"text": text, "writer": writer, "pos": pos}
            return _get_generic_object(Title, params)

    def get_writer(self):
        font_name=self.params.get("font_name")
        color=self.params.get("font_color")
        size=self.params.get("font_size")
        params = {"font_name":font_name, "color":color, "size":size}
        return _get_generic_object(Writer, params)
