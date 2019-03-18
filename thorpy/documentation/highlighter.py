import sys

with open(sys.argv[1],"r") as f:
    codelines = f.readlines()

with open(sys.argv[2],"r") as f:
    oldlines = f.readlines()

with open(sys.argv[2],"w") as f:
    for line in oldlines:
        if "<***INSERT_CODE***>" in line:
            for i,codeline in enumerate(codelines):
                f.write(str(i)+" "+codeline)
        else:
            f.write(line)
