# coding=utf-8
import sys
import operator

if len(sys.argv) < 2:
    sys.exit("Bad arguments!")

neutral = {}
positive = {}
negative = {}

try:
    f = open(sys.argv[1])
except IOError:
    sys.exit('cannot open file ' + sys.argv[1])

for s in f:
    s_split = (s.strip()).split(' ')
    # print s.strip()
    # print s_split
    if (s_split[0] == 'не'):
        s_split[0] = s_split[0] + s_split[1]
        s_split[1] = s_split[2]
    
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

sorted_positive = sorted(positive.iteritems(), key = operator.itemgetter(1))
f = open(sys.argv[1] + "positive", 'w')
for key in sorted_positive:
    f.write(key[0] + ' ' + str(key[1]) + '\n')
f.close() 

sorted_negative = sorted(negative.iteritems(), key = operator.itemgetter(1))
f = open(sys.argv[1] + "negative", 'w')
for key in sorted_negative:
    f.write(key[0] + ' ' + str(key[1]) + '\n')
f.close() 

sorted_neutral = sorted(neutral.iteritems(), key = operator.itemgetter(1))
f = open(sys.argv[1] + "neutral", 'w')
for key in sorted_neutral:
    f.write(key[0] + ' ' + str(key[1]) + '\n')
f.close() 
