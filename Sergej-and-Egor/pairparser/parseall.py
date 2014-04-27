__author__ = 'egor'

import getpairs

pair_parser = getpairs.PairParser()

for i in range(1, 27):
    print(i)
    pair_parser.get_pairs('/home/egor/PycharmProjects/SplitBigFile/mystemmed/mfile' + str(i) + '.txt')

pair_parser.print_pairs_no_neg('results/all_pairs_no_neg(2).txt')
