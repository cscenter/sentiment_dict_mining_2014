#encoding=utf-8
from graph_tool.all import Graph, label_components, label_largest_component
from graph_tool.flow import min_cut
import matplotlib.pyplot as plt
import sys

sys.path.append('../quality_check')

import qual
import compl

def get_attractions(in_graph):
    ver_id = in_graph.vertex_properties["id"]
    ver_part = in_graph.vertex_properties["part"]
    edge_weights = in_graph.edge_properties["weight"]
    ver_attract = in_graph.new_vertex_property("double")
    
    for v in in_graph.vertices():
        attraction = 0
        for e in v.out_edges():
            if ver_part[e.target()] == -1:
                attraction -= edge_weights[e]
            else:
                attraction += edge_weights[e]
        ver_attract[v] = attraction
        
    return ver_attract

def get_indexes(vect, l, h):
    """
    finds indexes in sorted vector of 2 elelements - a and b, where
    a - index of last element, which >  h
    b - index of last element which > l
    :param vect - descending sorted array
    :param l - integer, low bound
    :param h - integer, up bound, l <= h
    """
    a = 0
    b = 0
    for i in range(0, len(vect)):
        if vect[i] > h:
            a = i
        if vect[i] > l:
            b = i
    return [a, b]
            
def plot_attractions(in_graph, low, hig):
    ver_attr = sorted(in_graph.vertex_properties["attraction"].a, reverse=True)
    ver_attr = ver_attr[100:-50]
    [a, b] = get_indexes(ver_attr, low, hig)
    plt.plot(range(0, a + 1), ver_attr[:(a + 1)], 'go')
    plt.plot(range(a + 1, b + 1), ver_attr[(a + 1):(b + 1)], 'bo')
    plt.plot(range(b + 1, len(ver_attr)), ver_attr[(b + 1):], 'ro')

print("-------------------------------------------------")    
    
filename = '../pairparser/results/en_pairs(7).txt'
ftag = '7_3imp'
coefficient = 3

word_dict = {} # dict with indexes of nodes by word

f = open(filename, 'r', encoding="utf-8")

pairs_graph = Graph(directed=False)
edge_weights = pairs_graph.new_edge_property("double")
ver_names = pairs_graph.new_vertex_property("string")
ver_id = pairs_graph.new_vertex_property("int")
for line in f:
    spl_line = line.split(' ')

    if len(spl_line) == 1:
        continue

    pos = int(spl_line[0])
    neg = int(spl_line[1])
    cur_weight = pos + coefficient * neg

    w1 = spl_line[2].strip(' \n\uefef')
    w2 = spl_line[3].strip(' \n\uefef')

    if w1 not in word_dict:
        v1 = pairs_graph.add_vertex()
        ver_id[v1] = pairs_graph.vertex_index[v1]
        word_dict[w1] = ver_id[v1]
        ver_names[v1] = w1
    else:
        v1 = pairs_graph.vertex(word_dict[w1])

    if w2 not in word_dict:
        v2 = pairs_graph.add_vertex()
        ver_id[v2] = pairs_graph.vertex_index[v2]
        word_dict[w2] = ver_id[v2]
        ver_names[v2] = w2
    else:
        v2 = pairs_graph.vertex(word_dict[w2])

    if cur_weight == 0:
        continue
    e = pairs_graph.add_edge(v1, v2)
    edge_weights[e] = cur_weight
# adding properties
pairs_graph.vertex_properties["name"] = ver_names
pairs_graph.vertex_properties["id"] = ver_id
pairs_graph.edge_properties["weight"] = edge_weights
print("graph builded")
print(str(len(word_dict)))

largest_label = label_largest_component(pairs_graph)

# reading negative and positive parts
pos_file = open('../results/pos' + ftag + '.txt', 'r', encoding="utf-8")
neg_file = open('../results/neg' + ftag + '.txt', 'r', encoding="utf-8")
positive = []
negative = []
neutral = []


for s in pos_file:
    s = s.strip(' \n\uefef')
    if len(s) != 0:
        positive.append(s)
for s in neg_file:
    s = s.strip(' \n\uefef')
    if len(s) != 0:
        negative.append(s)

ver_part = pairs_graph.new_vertex_property("int")
not_deleted = pairs_graph.new_vertex_property("bool") # not deleted prop
pos_vert = []
neg_vert = []
neu_vert = []

for v in pairs_graph.vertices():
    ver_part[v] = 0
    not_deleted[v] = True
for w in positive:
    ver_part[pairs_graph.vertex(word_dict[w])] = 1
for w in negative:
    ver_part[pairs_graph.vertex(word_dict[w])] = -1
    
# new property
pairs_graph.vertex_properties["part"] = ver_part
pairs_graph.vertex_properties["notdeleted"] = not_deleted

print("graph ready")
print("-------------------------------------------------")

# starting point:
pairs_graph.vertex_properties["attraction"] = get_attractions(pairs_graph)
plot_attractions(pairs_graph, 0, 0)
cur_qual = qual.get_quality(positive, negative, neutral)
cur_comp = compl.get_completeness(positive, negative, neutral)
print("Quality = " + str(cur_qual["q"]))
print("Completeness = " + str(cur_comp["c"]))

# every iteration: deleting vertices with attraction in [low, hig], while...
#while d not in ['+', '-', '0']:
#        print("try again")
#        d = sys.stdin.readline().strip(' \n')
low = -4
hig = 13
while True:
    prev_q = cur_qual["q"]
    prev_c = cur_comp["c"]
    ver_attractions = pairs_graph.vertex_properties["attraction"]
    # cutting vertices with attractions in [low, hig]
    not_deleted = pairs_graph.vertex_properties["notdeleted"]
    for v in pairs_graph.vertices():
        if low <= ver_attractions[v] <= hig:
            neutral.append(ver_names[v])
            if ver_part[v] == 1:
                positive.remove(ver_names[v])
                ver_part[v] = 0
            elif ver_part[v] == -1:
                negative.remove(ver_names[v])
                ver_part[v] = 0
            not_deleted[v] = False
    pairs_graph.set_vertex_filter(not_deleted)
    pairs_graph.purge_vertices()
    # recalculating attractions, plotting and calculating quality and completeness
    pairs_graph.vertex_properties["attraction"] = get_attractions(pairs_graph)
    cur_qual = qual.get_quality(positive, negative, neutral)
    cur_comp = compl.get_completeness(positive, negative, neutral)
    print("-----------------------------------------------")
    print("Sum vol = " + str(len(neutral) + len(positive) + len(negative)))
    print("total neutral cutted = " + str(len(neutral)))
    print("Quality = " + str(cur_qual["q"]))
    print(cur_qual["notfound"])
    print("Completeness = " + str(cur_comp["c"]))
    print("-----------------------------------------------")
    if prev_q == cur_qual["q"]:
        break
pairs_graph.vertex_properties["attraction"] = get_attractions(pairs_graph)
plt.figure(2)
plot_attractions(pairs_graph, 0, 0)
plt.show()
# components_label = label_components(pairs_graph)
# largest_label = label_largest_component(pairs_graph)
# print(components_label[0].a)
# print(largest_label.a)

sys.path.remove('../quality_check')
