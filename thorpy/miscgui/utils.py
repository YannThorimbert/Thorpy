from thorpy.miscgui.title import Title
from thorpy.painting.painters.painter import Painter
from thorpy.painting.fusionner import _Fusionner

def get_void_state():
##    from thorpy.miscgui.title import Title
##    from thorpy.painting.painter import Painter
##    from thorpy.miscgui.fusionner import _Fusionner
    title = Title("")
    painter = Painter(None)
    fusionner = _Fusionner(painter, title)
    return State(fusionner)