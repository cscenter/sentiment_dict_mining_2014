#coding: utf-8
import sys

if len(sys.argv) < 5:
	print("Usage: annotated_pos annotated_neg big_dict_pos big_dict_neg")
	exit(0)

data = set(open(sys.argv[1], "r", encoding = "utf-8").read().split("\n"))
data = data.union(set(open(sys.argv[2], "r", encoding = "utf-8").read().split("\n")))

res_pos = open(sys.argv[3], "a", encoding = "utf-8")
res_neg = open(sys.argv[4], "a", encoding = "utf-8")

for word in data:
	if word[0] == "+":
		res_pos.write("\n" + word[1 : ])
	if word[0] == "-":
		res_neg.write("\n" + word[1 : ])
