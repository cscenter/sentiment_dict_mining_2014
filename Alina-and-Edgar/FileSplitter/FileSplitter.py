__author__ = 'Edgar'


import sys


if len(sys.argv) != 5:
    print("Usage: FileSplitter.py source_file file_with_neg_adj file_with_pos_adj file_with_neu_adj")
else:
    source_file = open(sys.argv[1], "r")
    file_with_neg_adj = open(sys.argv[2], "w")
    file_with_pos_adj = open(sys.argv[3], "w")
    file_with_neu_adj = open(sys.argv[4], "w")

    lines = source_file.readlines()

    for line in lines:
        temp = line.replace('\n', ' ').split()
        if temp[-1] == '+':
            file_with_pos_adj.write(temp[0] + '\n')
        elif temp[-1] == '-':
            file_with_neg_adj.write(temp[0] + '\n')
        elif temp[-1] == '0':
            file_with_neu_adj.write(temp[0] + '\n')