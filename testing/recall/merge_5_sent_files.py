#coding: utf-8
import sys

if len(sys.argv) < 7:
    print("Usage: 5 files to merge and res_file")
    exit(0)


inp = open(sys.argv[1], "r", encoding = "utf-8")
res = set(inp.read().split("\n"))
inp.close()

for i in range(2, 6):    
	inp = open(sys.argv[i], "r", encoding = "utf-8")
	tmp = set(inp.read().split("\n"))
	print(tmp)
	res = res.union(tmp)
	inp.close()

resFile = open(sys.argv[6], "w", encoding = "utf-8")
resFile.write("\n".join(res))

