#coding: utf-8
import sys
import os
                   
if len(sys.argv) < 5:
	print("Usage: dict500_pos dict500_neg big_dict_pos big_dict_neg")
	exit(0)


pos_dict = set(open(sys.argv[1], "r", encoding = "utf-8").read().split("\n"))
neg_dict = set(open(sys.argv[2], "r", encoding = "utf-8").read().split("\n"))

res_pos = open(sys.argv[3], "w", encoding = "utf-8")
res_neg = open(sys.argv[4], "w", encoding = "utf-8")

res_pos.write("\n".join(pos_dict))
res_neg.write("\n".join(neg_dict))

for word in pos_dict:
    #запустить mystem
	if s.find("?") != None:
		res_neg.write("\nне" + word)

for word in neg_dict:
	#запустить mystem
	if s.find("?") != None:
		res_pos.write("\nне" + word)