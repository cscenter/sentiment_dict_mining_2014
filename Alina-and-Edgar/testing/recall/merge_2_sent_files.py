#coding: utf-8
import sys

if len(sys.argv) < 5:
    print("Usage: merge_2_sent_files.py first_file second_file result_file diff_file")
    exit(0)

firstFile = open(sys.argv[1], "r", encoding = "utf-8")
secondFile = open(sys.argv[2], "r", encoding = "utf-8")
resFile = open(sys.argv[3], "w", encoding = "utf-8")
diffFile = open(sys.argv[4], "w", encoding = "utf-8")

firstLines = sorted(firstFile.read().split("\n"))
secondLines = sorted(secondFile.read().split("\n"))

def less(s, t):
	l = min(len(s), len(t))
	for i in range(l):
		if s[i] != t[i]:
			return (True if s[i] < t[i] else False)
	return True if len(s) < len(t) else False

j = 0
for first in firstLines:
    while j < len(secondLines) and less(secondLines[j], first):
    	diffFile.write(secondLines[j] + "\n")
    	j += 1

    if j == len(secondLines):
    	diffFile.write(first + "\n")
    	continue		
    if secondLines[j] == first:
    	j += 1
    	resFile.write(first + "\n")
    else:
    	diffFile.write(first + "\n")