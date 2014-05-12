#encoding=utf-8
__author__ = 'egor'

"""
Script parameters:
    1: name of file with words to mark
"""

import sys

if len(sys.argv) < 3:
    sys.exit("Bad args!")

f = open(sys.argv[1], "r", encoding = "utf-8")
f1 = open(sys.argv[2], "a+", encoding = "utf-8")
new_dict = {}

print('Mark new words with +, - or 0')
for s in f:
    print(s.strip(' \n') + ': ')
    d = sys.stdin.readline().strip(' \n')
    if d == "exit":
        lst = f.readlines()
        lst.insert(0, s)
        f.close()
        f = open(sys.argv[1], 'w', encoding = "utf-8")
        f.writelines(lst)
        f.close()
        f1.close()
        sys.exit("Ok")
    while d not in ['+', '-', '0']:
        print("try again")
        d = sys.stdin.readline().strip(' \n')
    if d == '+':
        new_dict[s.strip(' \n')] = 1
    elif d == '-':
        new_dict[s.strip(' \n')] = -1
    elif d == '0':
        new_dict[s.strip(' \n')] = 0
    f1.write(s.strip(' \n') + ' ' + d + '\n')
        
f.close()    
f1.close()

fpos = open('new_pos.txt', 'w', encoding = "utf-8")
fneg = open('new_neg.txt', 'w', encoding = "utf-8")
fneu = open('new_neu.txt', 'w', encoding = "utf-8")
for key in new_dict.keys():
    if new_dict[key] == 1:
        fpos.write(key + '\n')
    elif new_dict[key] == 0:
        fneu.write(key + '\n')
    elif new_dict[key] == -1:
        fneg.write(key + '\n')
fpos.close()
fneg.close()
fneu.close()