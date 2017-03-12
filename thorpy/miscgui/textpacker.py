from thorpy.miscgui.painterstyle import WRITER

def pack_text(width, text, element=None, sep=" "):
    """Returns a string with new lines inserted in order to fit the specified
    width.
    Specify element arg if you want to use element's writer to calculate text
    size."""
    if element:
        writer = element.get_title()._writer
    else:
        writer = WRITER()
    new_text = ""
    split_text = text.split(sep)
    current_width = 0
    for word in split_text:
        original_word = str(word)
        newline = False
        while "\n" in word:
            newline = True
            word = word.replace("\n","")
        word_width = writer.get_width(word)
        current_width += word_width
        if current_width > width:
            new_text += "\n"
            current_width = word_width
        final_word = original_word + sep
        if newline:
            current_width = 0
        new_text += final_word
    return new_text
