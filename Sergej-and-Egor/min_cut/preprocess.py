#encoding=utf-8
from graph_tool.all import Graph, label_components, graph_draw, label_largest_component, arf_layout
from graph_tool.flow import min_cut
from operator import itemgetter

filename = '../pairparser/results/en_pairs(7).txt'
print(filename)
coefficient = 5.278

word_dict = {}
add_dict = {}

f = open('bad.txt', 'r', encoding="utf-8")
for s in f:
    # print(s.split(' ')[0])
    add_dict[s.split(' ')[0]] = 1

f = open(filename, 'r', encoding="utf-8")
pairs_graph = Graph(directed=False)
edge_weights = pairs_graph.new_edge_property("int")
pos_weights = pairs_graph.new_edge_property("int")
neg_weights = pairs_graph.new_edge_property("int")
ver_names = pairs_graph.new_vertex_property("string")
for line in f:
    spl_line = line.split(' ')

    if len(spl_line) == 1:
        continue

    pos = int(spl_line[0])
    neg = int(spl_line[1])
    cur_weight = pos + coefficient * neg

    w1 = spl_line[2].strip(' \n\uefef')
    w2 = spl_line[3].strip(' \n\uefef')

    if w1 in add_dict or w2 in add_dict:
        continue

    if w1 not in word_dict:
        v1 = pairs_graph.add_vertex()
        word_dict[w1] = pairs_graph.vertex_index[v1]
        ver_names[v1] = w1
    else:
        v1 = pairs_graph.vertex(word_dict[w1])

    if w2 not in word_dict:
        v2 = pairs_graph.add_vertex()
        word_dict[w2] = pairs_graph.vertex_index[v2]
        ver_names[v2] = w2
    else:
        v2 = pairs_graph.vertex(word_dict[w2])

    e = pairs_graph.add_edge(v1, v2)
    edge_weights[e] = cur_weight
    pos_weights[e] = pos
    neg_weights[e] = neg

print("graph builded")

#fout = open('p_pairs7.txt', 'w', encoding='utf-8')
#for e in pairs_graph.edges():
#    if e.source().out_degree() == 1 or e.target().out_degree() == 1:
#        continue
#    else:
#        fout.write(str(pos_weights[e]) + ' ' + str(neg_weights[e]) + ' ' + ver_names[e.source()] + ' ' + ver_names[e.target()] + '\n')
    
# sorted by degrees vertices
degr = []

for v in pairs_graph.vertices():
    degr.append((v, v.out_degree()))

degr = sorted(degr, key=itemgetter(1))
fout = open('deg_sort.txt', 'w', encoding='utf-8')
for tup in degr:
    fout.write(ver_names[tup[0]] + ' ' + str(tup[1]) + '\n')
   
#find min subset of words conected to all others
#vol = len(word_dict)
#print(vol)
#cur = 0
#fout = open('dominators.txt', 'w', encoding='utf-8')
#while cur <= vol:
#    v = max(degr, key=itemgetter(1))[0]
#    fout.write(ver_names[v] + '\n')
#    cur += v.out_degree()
#    print(cur)
#    print(ver_names[v])
#    for u in v.out_neighbours():
#        for e in u.out_edges():
#            if e.target() in v.out_neighbours():
#                pairs_graph.remove_edge(e)
#    pairs_graph.remove_vertex(v)
#    degr = []
#    for v in pairs_graph.vertices():
#        degr.append((v, v.out_degree()))

# for cutted graph ---------------------------
filename = '../pairparser/results/p_pairs7.txt'
print(filename)
coefficient = 3

word_dict = {}
add_dict = {}

f = open('bad.txt', 'r', encoding="utf-8")
for s in f:
    # print(s.split(' ')[0])
    add_dict[s.split(' ')[0]] = 1

f = open(filename, 'r', encoding="utf-8")
pairs_graph_m = Graph(directed=False)
edge_weights = pairs_graph_m.new_edge_property("int")
pos_weights = pairs_graph_m.new_edge_property("int")
neg_weights = pairs_graph_m.new_edge_property("int")
ver_names = pairs_graph_m.new_vertex_property("string")
for line in f:
    spl_line = line.split(' ')

    if len(spl_line) == 1:
        continue

    pos = int(spl_line[0])
    neg = int(spl_line[1])
    cur_weight = pos + coefficient * neg

    w1 = spl_line[2].strip(' \n\uefef')
    w2 = spl_line[3].strip(' \n\uefef')

    if w1 in add_dict or w2 in add_dict:
        continue

    if w1 not in word_dict:
        v1 = pairs_graph_m.add_vertex()
        word_dict[w1] = pairs_graph_m.vertex_index[v1]
        ver_names[v1] = w1
    else:
        v1 = pairs_graph_m.vertex(word_dict[w1])

    if w2 not in word_dict:
        v2 = pairs_graph_m.add_vertex()
        word_dict[w2] = pairs_graph_m.vertex_index[v2]
        ver_names[v2] = w2
    else:
        v2 = pairs_graph_m.vertex(word_dict[w2])

    if cur_weight == 0:
        continue
    e = pairs_graph_m.add_edge(v1, v2)
    edge_weights[e] = cur_weight

print("graph builded")

degr = []
for v in pairs_graph_m.vertices():
    degr.append((v, v.out_degree()))

degr = sorted(degr, key=itemgetter(1))
fout = open('deg_sort_m.txt', 'w', encoding='utf-8')
for tup in degr:
    fout.write(ver_names[tup[0]] + ' ' + str(tup[1]) + '\n')
    
# find min subset of words conected to all others
vol = len(word_dict)
print(vol)
cur = 0
fout = open('dominators1.txt', 'w', encoding='utf-8')
while cur <= vol:
    v = max(degr, key=itemgetter(1))[0]
    fout.write(ver_names[v] + '\n')
    cur += v.out_degree()
    print(cur)
    print(ver_names[v])
    for u in v.out_neighbours():
        for e in u.out_edges():
            if e.target() in v.out_neighbours():
                pairs_graph_m.remove_edge(e)
    pairs_graph_m.remove_vertex(v)
    degr = []
    for v in pairs_graph_m.vertices():
        degr.append((v, v.out_degree()))
