#coding: utf-8
import sys
                   
if len(sys.argv) < 5:
	print("Usage: res_pos res_neg big_dict_pos big_dict_neg")
	exit(0)


data_pos = set(open(sys.argv[1], "r", encoding = "cp1251").read().split("\n"))
data_neg = set(open(sys.argv[2], "r", encoding = "cp1251").read().split("\n"))
data = data_pos.union(data_neg)
pos_dict = set(open(sys.argv[3], "r", encoding = "utf-8").read().split("\n"))
neg_dict = set(open(sys.argv[4], "r", encoding = "utf-8").read().split("\n"))
neut_dict = set(open(sys.argv[5], "r", encoding = "utf-8").read().split("\n"))
dict = pos_dict.union(neg_dict)
dict = dict.union(neut_dict)

print("pos_precision = ", repr(len(data_pos.intersection(pos_dict)) / len(data_pos.intersection(dict))))
print("neg_precision = ", repr(len(data_neg.intersection(neg_dict)) / len(data_neg.intersection(dict))))
print("precision = ", repr((len(data_pos.intersection(pos_dict)) + len(data_neg.intersection(neg_dict))) / len(data.intersection(dict))))

'''res_pos = open(sys.argv[5], "w", encoding = "utf-8")
res_neg = open(sys.argv[6], "w", encoding = "utf-8")

res_pos.write("\n".join(pos_dict.intersectionion(data)))
res_neg.write("\n".join(neg_dict.intersectionion(data)))'''



