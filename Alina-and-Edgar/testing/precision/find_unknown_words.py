#coding: utf-8
import sys

if len(sys.argv) < 6:
	print("Usage: found_words unknown_words big_dict_pos big_dict_neg big_dict_neutral")
	exit(0)


data = set(open(sys.argv[1], "r", encoding = "utf-8").read().split("\n"))
out = open(sys.argv[2], "a", "utf-8")

pos = open(sys.argv[3], "r", encoding = "utf-8")
neg = open(sys.argv[4], "r", encoding = "utf-8")
neut = open(sys.argv[5], "r", encoding = "utf-8")

big_dict = set(pos.read().split("\n"))
big_dict = big_dict.union(set(neg.read().split("\n")))
big_dict = big_dict.union(set(neut.read().split("\n")))

data = data.minus(big_dict)

out.write("\n".join(data))
