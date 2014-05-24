#coding:utf-8
import sys

if len(sys.argv) < 3:
	print("Usage: result dictionary")
	exit(0)


result = set(open(sys.argv[1], "r", encoding = "utf-8").read().split("\n"))
dictionary = set(open(sys.argv[2], "r", encoding = "utf-8").read().split("\n"))

print(len(result.intersection(dictionary)) / len(dictionary))
print(len(result.intersection(dictionary)) / len(result))
