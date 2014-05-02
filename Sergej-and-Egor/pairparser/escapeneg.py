# coding=utf-8

__author__ = 'egor'

import sys
import subprocess
import os


def add_pair(dict_to_add, adj1, adj2, p_pos, p_neg):
    """Adds pair of two adjectives into dictionary
        """
    if adj1 > adj2:
        adj1, adj2 = adj2, adj1


    if adj1 not in dict_to_add:
        dict_to_add[adj1] = {}
        dict_to_add[adj1][adj2] = [0, 0]
    elif adj2 not in dict_to_add[adj1]:
        dict_to_add[adj1][adj2] = [0, 0]

    dict_to_add[adj1][adj2][0] += p_pos
    dict_to_add[adj1][adj2][1] += p_neg


def escape_from_neg(fnamein, fnameout, ftransformed):
    my_dict = []  # dictionary with words, which appeared with 'не' at the beginning and exist (in a real world)
    pairs_dict = {}  # dictionary for pairs.

    # creating file with all the words with 'не' at the beginning
    buf_name = 'results/buf_no_neg_words.txt'
    buf_file = open(buf_name, 'w')
    fin = open(fnamein, 'r')
    for s in fin:
        spl_str = s.split(' ')
        if len(spl_str) < 4:
            print("=)")
            continue
        a1 = spl_str[2].strip(' \n')
        a2 = spl_str[3].strip(' \n')
        if a1[:2] == 'не':
            buf_file.write(a1[2:] + '\n')
        if a2[:2] == 'не':
            buf_file.write(a2[2:] + '\n')
    buf_file.close()
    fin.close()

    # making all words unique
    data = set(open(buf_name, 'r', encoding="utf-8").read().split("\n"))
    buf_file = open(buf_name, 'w')
    for w in data:
        buf_file.write(w + '\n')
    buf_file.close()

    # passing file generated above to mystem to conclude which word exists without 'не'
    m_buf_name = "results/mstem_neg_words.txt"
    os.system(' '.join(["mystem", "-nlwe", "utf-8", buf_name, m_buf_name]))
    mdata = set(open(m_buf_name, 'r', encoding="utf-8").read().split("\n"))
    for w in mdata:
        if w[-2:] != "??":
            spl_w = w.split('|')
            for word in spl_w:
                my_dict.append(word)

    tf = open(ftransformed, 'w')
    # generating new pairs
    fin = open(fnamein, 'r')
    for s in fin:
        spl_str = s.split(' ')
        if len(spl_str) < 4:
            print("=)")
            continue
        p_pos = int(spl_str[0])
        p_neg = int(spl_str[1])
        a1 = spl_str[2].strip(' \n')
        a2 = spl_str[3].strip(' \n')
        neg = 1
        if a1[:2] == 'не':
            if a1[2:] in my_dict:
                tf.write(a1 + '\n')
                a1 = a1[2:]
                neg *= -1
        if a2[:2] == 'не':
            if a2[2:] in my_dict:
                tf.write(a2 + '\n')
                a2 = a2[2:]
                neg *= -1
        if neg == -1:
            p_pos, p_neg = -p_neg, -p_pos

        add_pair(pairs_dict, a1, a2, p_pos, p_neg)

    tf.close()
    fin.close()

    data = set(open(ftransformed, 'r', encoding="utf-8").read().split("\n"))
    tf = open(ftransformed, 'w')
    for w in data:
        tf.write(w + '\n')
    tf.close()

    # writing all pairs to file
    f = open(fnameout, 'w')
    size = 0
    for a1 in pairs_dict.keys():
        size += len(pairs_dict[a1])
    f.write(str(size) + '\n')
    for w1 in pairs_dict.keys():
        for w2 in pairs_dict[w1].keys():
            f.write(' '.join([str(pairs_dict[w1][w2][0]), str(pairs_dict[w1][w2][1]), w1, w2, '\n']))
    f.close()

    # removing temp files
    os.remove(m_buf_name)
    os.remove(buf_name)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.stderr.write('ERROR: Bad arguments')
        sys.exit(1)

    # first arg - file with pairs in form [%m% %n% %adj1% %adj2%], m - number of pos. conj; n - number of neg. conj.
    # second arg - where to write
    # third arg - filename for file with transformed adjectives (with не)

    escape_from_neg(sys.argv[1], sys.argv[2], sys.argv[3])