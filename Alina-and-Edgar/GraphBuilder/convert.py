#coding: utf-8
import sys

if len(sys.argv) < 3:
	print("Usage: convet.py graph_file edges_file")

inp = open(sys.argv[1], "r", encoding = "utf-8")
out = open(sys.argv[2], "w", encoding = "cp1251")

lines = inp.read().split("\n")

for line in lines:
	if len(line) == 0:
		continue
	begin, line = line.split(":")

	if len(begin) == 0:
		continue
	
	ends = line.split(";")
	for end in ends:
		if len(end.split(" ")) > 2:
		    out.write(begin + end + "\n")