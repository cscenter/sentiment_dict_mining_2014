import sys


def loop(set):
    global graph, output_file
    for item in set:
        if item in graph:
            sum_pos = 0
            sum_neg = 0
            for key in graph[item]:
                sum_pos += int(graph[item][key][0])
                sum_neg += int(graph[item][key][1])
            output_file.write(item + ';' + str(sum_pos + sum_neg) + '\n')
        pass


if len(sys.argv) != 6:
    print("Usage: PlotBuilder.py graph_file, pos_file, neu_file, neg_file, output_file")
else:
    graph_file = open(sys.argv[1], "r", encoding="utf-8")
    pos_file = open(sys.argv[2], "r", encoding="utf-8")
    neu_file = open(sys.argv[3], "r", encoding="utf-8")
    neg_file = open(sys.argv[4], "r", encoding="utf-8")
    output_file = open(sys.argv[5], "w", encoding="utf-8")

    pos_set = set(line.strip() for line in pos_file)
    neu_set = set(line.strip() for line in neu_file)
    neg_set = set(line.strip() for line in neg_file)

    graph = dict()

    for line in graph_file:
        (word1, word2, pos_rel, neg_rel) = line.split()
        if not word1 in graph:
            edge = dict()
            edge[word2] = (pos_rel, neg_rel)
            graph[word1] = edge
        else:
            graph[word1][word2] = (pos_rel, neg_rel)
        pass

    loop(pos_set)
    loop(neg_set)




