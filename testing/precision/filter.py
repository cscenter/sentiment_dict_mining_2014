#coding: utf-8
import sys
                   
if len(sys.argv) < 7:
	print("Usage: res_pos res_neg dict500_pos dict500_neg big_dict_pos big_dict_neg")
	exit(0)


data = set(open(sys.argv[1], "r", encoding = "utf-8").read().split("\n"))
data = data.union(set(open(sys.argv[2], "r", encoding = "utf-8").read().split("\n")))
pos_dict = set(open(sys.argv[3], "r", encoding = "utf-8").read().split("\n"))
neg_dict = set(open(sys.argv[4], "r", encoding = "utf-8").read().split("\n"))

res_pos = open(sys.argv[5], "w", encoding = "utf-8")
res_neg = open(sys.argv[6], "w", encoding = "utf-8")

res_pos.write("\n".join(pos_dict.intersection(data)))
res_neg.write("\n".join(neg_dict.intersection(data)))

