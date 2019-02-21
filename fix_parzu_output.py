import sys
import re

prevlinenumber = 0

outlines = []

for line in open(sys.argv[1],'r').readlines():
    if re.match("\d+", line.strip().split("\t")[0]):    # should match only real lines
        linetoapp = line.strip().split("\t")
        linenumber = int(linetoapp[0])
        if linenumber <= prevlinenumber:                # current line is start of next sentence
            outlines.append("")
        outlines.append(line)
        prevlinenumber = linenumber

with open(sys.argv[2], 'w') as f:
    for line in outlines:
        f.write(line + "\n")