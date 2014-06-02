# coding=utf-8

import sys
import subprocess
import os

"""
Script parameters:
    1: pos file
    2: neg file
    3: neu file
"""

my_dict = {}
real_words = []

for l in open(sys.argv[1], 'r', encoding="utf-8"):
    my_dict[l.strip(' \n')] = 1
for l in open(sys.argv[2], 'r', encoding="utf-8"):
    my_dict[l.strip(' \n')] = -1
for l in open(sys.argv[3], 'r', encoding="utf-8"):
    my_dict[l.strip(' \n')] = 0

buf_name = 'buf_no_neg_words.txt'
buf_file = open(buf_name, 'w')    
for w in my_dict:
    if w[:2] == 'не':
        buf_file.write(w[2:] + '\n')
buf_file.close()

# making all words unique
data = set(open(buf_name, 'r', encoding="utf-8").read().split("\n"))
buf_file = open(buf_name, 'w')
for w in data:
    buf_file.write(w + '\n')
buf_file.close()

# passing file generated above to mystem to conclude which word exists without 'не'
m_buf_name = "mstem_neg_words.txt"
os.system(' '.join(["mystem", "-nlwe", "utf-8", buf_name, m_buf_name]))
mdata = set(open(m_buf_name, 'r', encoding="utf-8").read().split("\n"))
for w in mdata:
    if w[-2:] != "??":
        spl_w = w.split('|')
        for word in spl_w:
            real_words.append(word)

new_dict = {}
for w in my_dict:
    if w[:2] == 'не':
        if w[2:] in real_words:
            new_dict[w[2:]] = -my_dict[w]
        else:
            new_dict[w] = my_dict[w]
    else:
        new_dict[w] = my_dict[w]

fpos = open('new_pos.txt', 'w', encoding="utf-8")
fneg = open('new_neg.txt', 'w', encoding="utf-8")
fneu = open('new_neu.txt', 'w', encoding="utf-8")
for w in new_dict:
    if new_dict[w] == 1:
        fpos.write(w + '\n')
    elif new_dict[w] == 0:
        fneu.write(w + '\n')
    elif new_dict[w] == -1:
        fneg.write(w + '\n')
fpos.close()
fneg.close()
fneu.close()

# removing temp files
os.remove(m_buf_name)
os.remove(buf_name)             
