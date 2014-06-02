__author__ = 'egor'

import getpairs

pair_parser = getpairs.PairParser()

for i in range(1, 27):
    print(i)
    pair_parser.get_pairs('/home/manatee/Programming/SplitBigFile/mystemmed/mfileD' + str(i) + '.txt')

pair_parser.print_pairs_no_neg('results/pairs_no_neg(7).txt')
