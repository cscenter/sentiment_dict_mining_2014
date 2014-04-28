__author__ = 'egor'

"""
Script parameters:
    1: name of file with positive words, which were found by our algorithms (will be tested)
    2: name of file with negative words, which were found by our algorithms
    3: filename of 500-dictionary positive words (for completeness test)
    4: filename of 500-dictionary negative words (for completeness test)
    5: filename of words, which were transfomed by deleting 'не' //not necess.

While execution, you'll need to mark new for big dictionary words from console

Script will create three files in a working directory with names:
    'big_ext_pos.txt',    - new marked positive words
    'big_ext_neg.txt',    - new marked negative words
    'big_ext_neutral.txt' - new marked neutral words
"""

import sys


def read_pos(dict_to_add, filename):
    f = open(filename, 'r')
    for s in f:
        if s.strip(' \n') not in dict_to_add:
            dict_to_add[s.strip(' \n')] = 1
    f.close()


def read_neg(dict_to_add, filename):
    f = open(filename, 'r')
    for s in f:
        if s.strip(' \n') not in dict_to_add:
            dict_to_add[s.strip(' \n')] = -1
    f.close()


def read_neutral(dict_to_add, filename):
    f = open(filename, 'r')
    for s in f:
        if s.strip(' \n') not in dict_to_add:
            dict_to_add[s.strip(' \n')] = 0
    f.close()


if len(sys.argv) < 5:
    sys.exit("Bad arguments!")

completeness_dict = {}  # given completeness 500-dict
new_dict = {}           # dictionary, which were found by our algorithm

#reading dictionaries
read_pos(new_dict, sys.argv[1])
read_neg(new_dict, sys.argv[2])
read_pos(completeness_dict, sys.argv[3])
read_neg(completeness_dict, sys.argv[4])

if len(sys.argv) > 5:
	transformed = set(open(sys.argv[5], 'r', encoding="utf-8").read().split("\n"))
else:
	transformed = []

completeness_value = 0  # number of guessed words from 500-dictionary

f1 = open('compl_not_found.txt', 'w')
f2 = open('compl_correct_found.txt', 'w')
f3 = open('compl_wrong_found.txt', 'w')

words_found = 0
words_correctly_found = 0
words_not_found = 0

for key in completeness_dict.keys():
	if key not in new_dict.keys():
		if key in transformed:
			words_found += 1
			if completeness_dict[key] == - new_dict[key[2:]]:
				words_correctly_found += 1
				f2.write(key + '\n')
			else:
				f3.write(key + '\n')
		else:
			words_not_found += 1
			f1.write(key + '\n')
	else:
		words_found += 1
		if completeness_dict[key] == new_dict[key]:
			words_correctly_found += 1
			f2.write(key + '\n')
		else:
			f3.write(key + '\n')
f1.close()
f2.close()
f3.close()

print('---------------------------------------------')	
print('Completness dict volume = ' + str(len(completeness_dict)) + '\n')
# print('Found + not found count =  ' + str(words_found + words_not_found) + '\n')
print('Words not found = ' + str(words_not_found) + '\n')
print('Correctly found = ' + str(words_correctly_found) + '\n')
print('Completeness value = ' + str(words_correctly_found * 100 / len(completeness_dict)) + ' %\n')
print('Found / All = ' + str(words_found * 100 / len(completeness_dict)) + ' %\n')
print('---------------------------------------------')	
