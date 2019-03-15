import os
os.remove("./new.html")

f0 = open("./cheatsheet.html", "r")
f1 = open("./new.html", "w")



for line in f0.readlines():
    if '<a href="#">' in line:
        newline = line.replace('<a href="#">', '<code>')
        newline = newline.replace('</a>', '</code>')
    else:
        newline = line
    f1.write(newline)

f0.close()
f1.close()