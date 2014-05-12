# coding=utf-8
import sys
import operator

if len(sys.argv) < 2:
    sys.exit("Bad arguments!")

neutral = {}
positive = {}
negative = {}

try:
    f = open(sys.argv[1], "r", encoding = "utf-8")
except IOError:
    sys.exit('cannot open file ' + sys.argv[1])

for s in f:
    s_split = (s.strip()).split(' ')
    # print s.strip()
    # print s_split
    if (s_split[0] == 'не'):
        s_split[0] = s_split[0] + s_split[1]
        s_split[1] = s_split[2]
    
    # print(s_split)
    if (s_split[1] == "+"):
        if s_split[0] in positive:
            positive[s_split[0]] += 1 
        else: positive[s_split[0]] = 1
    elif (s_split[1] == "-"):
        if s_split[0] in negative:
            negative[s_split[0]] += 1 
        else: negative[s_split[0]] = 1
    elif (s_split[1] == "0"):
        if s_split[0] in neutral:
            neutral[s_split[0]] += 1 
        else: neutral[s_split[0]] = 1

f.close()

print(sys.argv[1].split('.txt'))
f = open(sys.argv[1].split('.txt')[0] + "_pos.txt", 'w', encoding = "utf-8")
for key in positive:
    f.write(key + '\n')
f.close() 

f = open(sys.argv[1].split('.txt')[0] + "_neg.txt", 'w', encoding = "utf-8")
for key in negative:
    f.write(key  + '\n')
f.close() 

f = open(sys.argv[1].split('.txt')[0] + "_neu.txt", 'w', encoding = "utf-8")
for key in neutral:
    f.write(key + '\n')
f.close() 
