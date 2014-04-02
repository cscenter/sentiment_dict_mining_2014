#coding: utf-8
import sys

inp = open("output.txt", "r", encoding = "cp1251")
out = open("input.txt", "w", encoding = "cp1251")

lines = inp.read().split("\n")

for line in lines:
    begin, line = line.split(":")
    ends = line.split(";")
    for end in ends:
    	if len(end.split(" ")) > 2:
    	    out.write(begin + end + "\n")