import os, fileinput

pattern_src = '<span class="o">.</span><span class="n">make</span><span class="p">(</span>'
pattern_dst = '<span class="p">(</span>'

def replace_in_file(fn, src, dst):
    with open(fn,"r") as f:
        new_lines = [line.replace(src, dst) for line in f.readlines()]
    with open(fn,"w") as f:
        for line in new_lines:
            f.write(line)


for dir in ["examples", "tutorials"]:
    for fn in os.listdir(dir):
        if fn.endswith(".html"):
            replace_in_file(os.path.join(dir,fn), pattern_src, pattern_dst)
