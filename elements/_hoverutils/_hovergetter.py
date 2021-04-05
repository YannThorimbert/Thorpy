from pygame import Surface

from thorpy.miscgui import functions, style
from thorpy.painting.painters.optionnal.illuminer import IlluminerAlphaExcept as Illuminer
from thorpy.painting import pilgraphics



def get_already_illuminated_title(hoverable, state, color=None):
    color = style.COLOR_TXT_HOVER if color is None else color
    fusionner = hoverable._states[state].fusionner
    old_color_target = fusionner.painter.color_target
    old_color_bulk = fusionner.painter.color_bulk
    fusionner.painter.color_target = color
    fusionner.painter.color_bulk = color
    img = fusionner.get_hover_fusion()
    fusionner.painter.color_target = old_color_target
    fusionner.painter.color_bulk = old_color_bulk
    return img


def get_not_already_illuminated_title(hoverable, state, color=None):
    color = style.COLOR_TXT_HOVER if color is None else color
    #produce illumination then blit it on the painter not fusionned.
    fusionner = hoverable._states[state].fusionner
    target_img = hoverable.get_image(state)
    r = target_img.get_rect()
    #the shadow will be larger in order to make free space for fadeout.
    shadow_radius = 2
    r.inflate_ip(2*shadow_radius, 2*shadow_radius)
    img = Surface(r.size)
    img.fill((255, 255, 255, 255))
    img.blit(target_img, (shadow_radius, shadow_radius))
    shadow = pilgraphics.get_shadow(img,
                                    radius=shadow_radius,
                                    black=255,
                                    alpha_factor=0.95,
                                    decay_mode="exponential",
                                    color=color)
    shadow = shadow.subsurface(shadow.get_rect().inflate((-2*shadow_radius, -2*shadow_radius)))
    return shadow

def get_illuminated_title(hoverable, state, color=None):
    if is_illuminated(hoverable, state):
        return get_already_illuminated_title(hoverable, state, color)
    else:
        return get_not_already_illuminated_title(hoverable, state, color)

def get_highlighted_title(hoverable, state, color=None):
    color = style.COLOR_TXT_HOVER if color is None else color
    return hoverable._states[state].fusionner.get_hover_fusion(color=color)

def get_all_highlighted_title(hoverable, state, colors):
    color_text, color_bulk = colors
    if not color_text:
        color_text=style.COLOR_TXT_HOVER
    if not color_bulk:
        color_bulk=style.COLOR_BULK_HOVER
    fusionner = hoverable._states[state].fusionner
    old_color_painter = None
    if hasattr(fusionner, "painter"):
        if hasattr(fusionner.painter, "color"):
            old_color_painter = fusionner.painter.color
            fusionner.painter.color = color_bulk
    illuminer = is_illuminated(hoverable, state)
    if illuminer:
        old_color_target = fusionner.painter.color_target
        old_color_bulk = fusionner.painter.color_bulk
        fusionner.painter.color_target = color_text
        fusionner.painter.color_bulk = color_text
    img = fusionner.get_hover_fusion()
    if old_color_painter:
        fusionner.painter.color = old_color_painter
    if illuminer:
        fusionner.painter.color_target = old_color_target
        fusionner.painter.color_bulk = old_color_bulk
    return img

def is_illuminated(hoverable, state):
    fusionner = hoverable._states[state].fusionner
    if hasattr(fusionner, "painter"):
        if isinstance(fusionner.painter, Illuminer):
            return True
    return False

def get_img_highlighted(hoverable, state, color=None):
    if is_illuminated(hoverable, state):
        return get_illuminated_title(hoverable, state, color)
    else:
        return get_highlighted_title(hoverable, state, color)

def get_img_painter(hoverable, state, color=None):
    color = style.COLOR_TXT_HOVER if color is None else color
    fusionner = hoverable._states[state].fusionner
    if hasattr(fusionner, "painter"):
        fusionner.painter.hovered=True
    illuminer = is_illuminated(hoverable, state)
    if illuminer:
        old_color_target = fusionner.painter.color_target
        old_color_bulk = fusionner.painter.color_bulk
        fusionner.painter.color_target = color
        fusionner.painter.color_bulk = color
    img = fusionner.get_hover_fusion()
    if illuminer:
        fusionner.painter.color_target = old_color_target
        fusionner.painter.color_bulk = old_color_bulk
    if hasattr(fusionner, "painter"):
        fusionner.painter.hovered=False
    return img

def get_img_redraw(hoverable, state, params):
    paint_params = params["params"]
    paint_params["size"] = hoverable.get_ghost_size()
    painter = functions.obtain_valid_painter(params["painter"],
                                             **paint_params)
    return painter.get_fusion(hoverable.get_title(), True)
