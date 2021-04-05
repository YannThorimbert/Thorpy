"""Functions to handle strings"""

OKAY_BEFORE = ["", " ", ".", "="]
OKAY_AFTER = ["", " "]

def exact_replace(text, src, target, okay_before=None, okay_after=None):
    if not okay_before:
        okay_before = OKAY_BEFORE
    if not okay_after:
        okay_after = OKAY_AFTER
    beg = 0
    indices = []
    L = len(src)
    while beg < len(text):
        found = text.find(src, beg)
        if found == 0 and "" in okay_before:
            if text[L] in okay_after:
                indices.append(found)
        elif found > 0:
            if text[found-1] in okay_before:
                if found + L < len(text):
                    if text[found+L] in okay_after:
                        indices.append(found)
                elif "" in okay_after:
                    indices.append(found)
        else:
            break
        beg = found + L
    new_txt = ""
    beg = 0
    for i in indices:
        new_txt += text[beg:i] + target
        beg = i + L
    new_txt += text[beg:]
    return new_txt

##s = "a=lol= =lol lol= bonjour lol kevinlolkeivin heinlol lolhein .lol, gracealol lol dfg"
##print(exact_replace(s, "lol", "katapult"))

def convert_str(value, type_):
    if type_ == int:
        value = float(value)
    return type_(value)

##class NoFinish(Exception):
##    """Exception for get_between_key"""
##
##    def __init__(self, end):
##        Exception.__init__(self, "End of line but " + str(end) + " not found")

def get_between_keys(text, beg, end=None, first=True, finish=False):
    """
    Returns the text between <beg> and <end>.

    If <end> is None, returns all that follows <beg>.

    If <first> is True, <txt> must begin with <beg>

    If <finish> is True, <end> must be in <txt>.
    """
    a = text.find(beg)
    if a < 0: #no begin found
        return None
##        raise Exception("No begin '" + beg + "' found in '" + text + "'")
    else:
        if first and (a != 0): #a is not first char and <first> is True
##            raise Exception("Not first char")
            return None
        l = len(beg)
        if end is None:
            return text[a+l::]
        b = text[a+l::].find(end)
        if b < 0:
            if finish: #no end found and <finish> is True
                raise NoFinish(end)
            else:
                return text[a+l::]
        else:
            return text[a+l:b+l]

def get_between_possible_keys(text, beg, ends):
    """Like get_between_keys, but for multiple possible ends. Returns the result
    that corresponds to the nearest end found from beg."""
    scores = list()
    for end in ends:
        try:
            r = get_between_keys(text, beg, end, finish=True)
            index = text[1::].find(end)
            scores.append((index, end, r))
        except NoFinish:
            pass
    if scores:
        scores.sort()
        return scores[0][2]
    else:
        raise Exception("No end found")



def get_parent_folder(path, sep="/"):
    """Returns the path corresponding to the parent folder of <path>."""
    l = len(path)
    n = -1
    for i in range(l-2, -1, -1):
        if path[i] == sep:
            n = i
            break
    if n > 0:
        return path[:n+1]
    else:
        return -1

def simplify_str(filename):
    """Remove all the path from a filename ; returns only the actual name"""
    for i in range(len(filename)-1, -1, -1):
        char = filename[i]
        if char == "/" or char == "\\":
            return filename[i+1:].replace(".txt", "")
    return filename

def no_minus_zero(n):
    """Removes possibles '-0.'"""
    if n.startswith(" "):
        n = n[1::]
    if n.startswith("-"):
        for char in n[1:]:
            if char != "." and char != "0":
                return n
        return n[1:]
    return n


def format_number(number, number_int=False, tot=10, dec=4, format_t="f"):
    """Convert a number to string.
    number_int : first convert the number to an integer.
    tot : ???.
    dec : number of decimals
    format : format style ('f' for float, 'e' for scientific, ...)
    """
    if number_int:
        return str(int(number))
    else:
        s = "{:" + str(tot) + "." + str(dec) + format_t + "}"
        sform = s.format(number)
        return no_minus_zero(sform)

def del_spaces(text):
    """"abc def" => "abcdef"""
    return text.replace(" ", "")
##    return ' '.join(text.split())


def str_dist(new, original, lowerize=True):
    """Measures difference between two strings"""
    if lowerize:
        new = new.lower()
        original = original.lower()
    len_diff = abs(len(new) - len(original))
    length = min(len(new), len(original))
    for i in range(length):
        len_diff += not(new[i] == original[i])
    return len_diff

def longest_str(textes):
    """Returns longest text in a list"""
    if not textes:
        return -1
    else:
        maxlen = -1
        for text in textes:
            l = len(text)
            if l > maxlen:
                maxlen = l
                toReturn = text
        return toReturn


def explode_string(text):
    """Returns a list containing all the chars in <txt> one by one"""
    chars = []
    for char in text:
        chars.append(char)
    return chars


def get_extension(s, delimiter='.'):
    """Returns what belongs after delimiter"""
    ext = ""
    point = False
    for c in s:
        if c == delimiter:
            ext = ""
            point = True
        if point:
            ext += c
    return ext

def get_without_extension(s, extension):
    """Returns s without what is after the point"""
    lw = len(s)
    le = len(extension)
    return s[0:lw-le]

def list_to_str(l):
    return "".join(l)