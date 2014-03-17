import sys
import os
import string

def parse(str):
	res = list()
	s = str.split("{")
	
	if len(s) < 2:
		res.append(s[0])
		return res

	form = s[0]
	s = s[1].split("=")
	word = s[0]
	res.append(word)
	if len(s) == 1:
		return res
	POS = s[1]

	res.append(POS)
	res.append(s[2:])
	
	return res

if len(sys.argv) < 3:
	print("File names are required")
	exit(0)


TextFile = open(sys.argv[2], "w", encoding = "utf-8")
inFile = open(sys.argv[1], "r", encoding = "utf-8")
line = inFile.read().split("\n")
line = [x.replace("_", "") for x in line]
line = [parse(x.lower()) for x in line if len(x) > 0]
	
l = len(line)
i = 0
while i < l:
	if len(line[i]) < 2:
		i += 1
		continue

	word = line[i][0]
	POS = line[i][1]
	info =line[i][2]
	if POS == "a":
		res = list()
		res.append(word)
		while i < l - 2:
			#print(line[i + 1])
			if (line[i + 1][0] == ",") or (len(line[i + 1]) > 1 and line[i + 1][0] == "\u0438"):
				i += 2
				if (len(line[i]) > 1 and line[i][1] == "a" and line[i][2] == info):
					#print(word, "\u0438", line[i][0])
					res.append((line[i][0], 1))
			elif (len(line[i + 1]) > 1 and line[i + 1][0] == "\u043D\u043E"):
				i +=2
				if (len(line[i]) > 1 and line[i][1] == "a" and line[i][2] == info):
					#print(word, "\u043D\u043E", line[i][0])
					res.append((line[i][0], -1))
			else:
				break
		if len(res) > 1:	 	
			TextFile.write(str(res) + "\n")
	i += 1