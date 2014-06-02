#from pyx import *
import matplotlib
import sys
import pylab as P


if len(sys.argv) < 4:
	print("Usage: data pos_dict neg_dict")
	exit(0)

inp = open(sys.argv[1], "r", encoding = "cp1251")
pos = set(open(sys.argv[2], "r", encoding = "utf-8").read().split("\n"))
neg = set(open(sys.argv[3], "r", encoding = "utf-8").read().split("\n"))

words = list()                                    
num = list()
scores = list()
t = list()

src = inp.read().split("\n")
n = 0
for line in src:
	if len(line) == 0:
		break

	num.append(n)
	word, score	= line.split(",")
	words.append(word)
	scores.append(int(score))
	t.append((int(score), n))
	n += 1
#print(words)
#print(scores)

dict = dict()

t.sort()
t.reverse()

scores = [x[0] for x in t]

for i in range(n):
	sc, nn  = t[i]
	dict[words[nn]] = i

pos_ind = list()
pos_sc = list()
for w in pos.intersection(dict.keys()): 
	print(w)
	if len(w) == 0:
		continue
	print(w)
	pos_ind.append(dict[w] + 100)
	pos_sc.append(scores[dict[w]])

#print(pos_ind)

neg_ind = list()
neg_sc = list()
for w in neg.intersection(dict.keys()):
	print(w)
	if len(w) == 0:
		continue	
	
	neg_ind.append(dict[w] + 100)
	neg_sc.append(scores[dict[w]])

#print(neg_ind)

def build_plot(m):
	#m = 2000  #len(scores)
	pos_sc_tmp = [pos_sc[i] for i in range(len(pos_ind)) if pos_ind[i] < m + 100]
	neg_sc_tmp = [neg_sc[i] for i in range(len(neg_ind)) if neg_ind[i] < m + 100]
	pos_ind_tmp = [x for x in pos_ind if x < m + 100]
	neg_ind_tmp = [x for x in neg_ind if x < m + 100]

	P.plot(range(100, m + 100), scores[:m:])
	P.plot(pos_ind_tmp, pos_sc_tmp, 'g.')
	P.plot(neg_ind_tmp, neg_sc_tmp, 'r.')

	#P.show()
	P.savefig("plot" + (str(m) if m < len(scores) else ""))

	P.clf()

build_plot(len(scores))
build_plot(500)
build_plot(1000)
build_plot(2000)

n, bins, patches = P.hist(scores, len(scores) + 1, histtype='bar', range = (-1000, 1000), log = 1)
#P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
#P.show()
P.savefig("hist")