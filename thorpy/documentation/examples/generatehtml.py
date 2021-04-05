"""VERY simplistic. Full of issues. Never use it."""


def get_line_content(line):
    char = ""
##    if "'" in line:
##        char = "'"
##        lines = line.split("'")
    if '"' in line:
        char = '"'
        lines = line.split('"')
    else:
        return [], [line]
    strs = [char+s+char for s in lines[1::2]]
    nostrs = lines[0::2]
    return strs, nostrs

def treat_number(line):
    numbers = ".1234567890"
    beg = -1
    new_line = ""
    for i,char in enumerate(line):
        treated = False
        if char in numbers:
            if i >= 1:
                if line[i-1] in ":=()[], ":
                    beg = i
                    new_line += "<span class='number'>" + char
                    treated = True
        else:
            if beg >= 0:
               new_line += "</span>" + char
               beg = -1
               treated = True
        if not treated:
            new_line += char
    return new_line

def generate(title, src, img, dst, text):
    f = open(src, "r")
    lines = f.readlines()
    f.close()
    #
    f = open(template_src, "r")
    template = f.readlines()
    f.close()
    #
    ndocstr = 0
    f = open(dst, "w")
    for line in template:
        if "###CODE###" in line:
            for codeline in lines:
                comment = None
                if codeline.startswith('"""'):
                    codeline, comment = "", codeline
                    ndocstr += 1
                elif ndocstr == 1:
                    codeline, comment = "", codeline
                if "#" in codeline:
                    if codeline[0] == "#":
                        codeline, comment = "", codeline
                    else:
                        codeline, comment = codeline.split("#")
                strs, nostr = get_line_content(codeline)
                new_nostr = []
                for code in nostr:
                    for k in keywords:
                        code = code.replace(k, "<span class='keyword'>"+k+"</span>")
                    code = treat_number(code)
                    new_nostr.append(code)
                new_strs = []
                for i in range(len(strs)):
                    new_strs.append("<span class='str'>" + strs[i] + "</span>")
                codeline = ""
                for i in range(len(new_nostr)):
                    codeline += new_nostr[i]
                    if i < len(new_strs):
                        codeline += new_strs[i]
                if comment:
                    if comment.startswith('"""') or ndocstr==1:
                        codeline += "<span class='comment'>" + comment + "</span>"
                    else:
                        codeline += "<span class='comment'>#" + comment + "</span>"
                f.write(codeline)
        elif "###LINES###" in line:
            for i in range(len(lines)):
                f.write(str(i)+"\n")
        elif "###TEXT###" in line:
            f.write(text)
        elif "###TITLE###" in line:
            f.write(title)
        elif "###IMG###" in line:
            f.write(img)
        else:
            f.write(line)
    f.close()

gen = [
("overview.html", "Elements overview", '<a href="overview.png"><img src="overview.png" valign="top" class="tutoimg"/></div></a>',
"../../examples/overview.py",
"<p>ThorPy provides a fast way to let user decide between a list of choices. As for alerts, you may either need blocking or non-blocking choices.</p>"),

("style.html", "Basic styling", '<a href="style.png"><img src="style.png" valign="top" class="tutoimg"/>',
"../../examples/basicstyling.py",
"<p>The code below shows a few ways to tune the appearance of your elements - size, colors, fonts, ... You can also see these functions "+\
"summarized in the <a href='../documentation/userguide/cheatsheet.html#style'>cheat sheet</a>. Moreover, you can find a tutorial for "+\
"writing your own design template <a href='../tutorials/painters.html'>here</a>.</p>"),

("submenus.html", "Submenus", '<a href="submenus.png"><img src="submenus.png" valign="top" class="tutoimg"/>',
"../../examples/submenus.py",
''),

("shadows.html", "Shadows", '<a href="shadows.png"><img src="shadows.png" valign="top" class="tutoimg"/>',
"../../examples/shadows.py",
'<p>The code below shows how to check if the user can generate shadows and how to generate them. We also give a few parameters for the'+\
' shadow at the end of the code. Note that this code is suitable for generating shadows of objects that are supposed to stand '+\
'"vertically" on the ground. If not, you can either manually parametrize the shadow by setting its vertical attribute to'+\
' <code>False</code> or use <code>thorpy.makeup.set_button_shadow</code>.</p><p>If you want to use the same awesome'+\
' character image as the one in the example below, you can find it <a href="character.png">here</a>.</p>'),

("image_buttons.html", "Image buttons", "",
"../../examples/imagebuttons.py",
'<p>Here is shown a fast way to create buttons from images. The image used can be different for normal, hover and pressed states. '+\
'If no image is passed for hover and/or pressed states, the image for normal state will be used by default.</p><p>The files used '+\
'in this example are <a href="normal.png">normal.png</a>, <a href="hover.png">hover.png</a> and <a href="pressed.png">pressed.png</a>.</p>'),

("pools.html", "Radio buttons and togglable elements", "",
"../../examples/radiobuttons.py",
'<p>The code below shows how to set up radio buttons so that there is always only one that is selected. Also, togglable buttons '+\
'are defined, which behave the same way, except that we allow them to be all unselected.</p>'),

("alerts.html", "Alerts", "",
"../../examples/alerts.py",
'<p>The code below shows how to set up alerts (box appearing on the screen and delivering a message to the user).'+\
' You can use blocking and non-blocking alerts, depending on your needs.</p>'),

("choices.html", "User choices", "",
"../../examples/userchoices.py",
"<p>The code below produces an application summarizing most of the common built-in elements that one would use in a program. In addition, "+\
"an help element has been added to each element presented in order to show dynamic help to the user during execution. Note that there is many"+\
"other available built-in elements : you can check them on the <a href='../documentation/userguide/cheatsheet.html#elements'>cheat sheet</a>.</p>"),

("launching.html", "Advanced menus and launching elements", "",
"../../examples/advancedmenus.py",
'<p>The code below present different ways to launch elements into the current menu.</p>'),

("launching.html", "Advanced menus and launching elements", "",
"../../examples/advancedmenus.py",
'<p>The code below present different ways to launch elements into the current menu.</p>'),

("fx.html", "Smoke, fire and explosion debris", '<a href="fx.png"><img src="fx.png" valign="top" class="tutoimg"/></div></a>',
"../../examples/specialeffects.py",
'<p>We show here how to use smokes and debris generators. For this, we use this <a href="boat_example.png">ship sprite</a>.</p>'),

("userchoices2.html", "User choices (2)", "",
"../../examples/userchoices2.py",
'<p> It is shown here how to use user input on several procedurally generated buttons. </p>'),
]



keywords = ["for ", "if ", "def ", "class ", "from ", "import ", "print"]
src = "../../examples/basicstyling.py"
dst = "caca2.html"
template_src = "template.html"

for dst, title, img, src, text in gen:
    generate(title, src, img, dst, text)

