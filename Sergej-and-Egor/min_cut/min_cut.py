#encoding=utf-8
from graph_tool.all import Graph, label_components, graph_draw, label_largest_component, arf_layout
from graph_tool.flow import min_cut

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
pairs_graph = Graph(directed=False)
edge_weights = pairs_graph.new_edge_property("int")
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

    if cur_weight == 0:
        continue
    e = pairs_graph.add_edge(v1, v2)
    edge_weights[e] = cur_weight

print("graph builded")

components_label = label_components(pairs_graph)
largest_label = label_largest_component(pairs_graph)
#print(components_label[0].a)
#print(largest_label.a)

mc, part = min_cut(pairs_graph, edge_weights)

print("Min cut value = " + str(mc))

f1 = open('first_part.txt', 'w', encoding="utf-8")
f2 = open('sec_part.txt', 'w', encoding="utf-8")
f3 = open('add_comp.txt', 'w', encoding="utf-8")

count1 = 0
count2 = 0
for key in word_dict.keys():
    # print(key)
    # print(part[pairs_graph.vertex(word_dict[key])])
    v = pairs_graph.vertex(word_dict[key])
    if largest_label[v] == 1:  # if only in largest component
        if part[v] == 0:
            count1 += 1
            f1.write(key + '\n')
        else:
            count2 += 1
            f2.write(key + '\n')
    else:
        f3.write(key + ' ' + str(components_label[0][v]) + ' ' + str(part[v]) + '\n')

f1.close()
f2.close()
f3.close()

# position = arf_layout(pairs_graph, max_iter=3)
# graph_draw(pairs_graph, pos=position, vertex_text=ver_names, edge_text=edge_weights, vertex_size=5, vertex_font_size=10,
#          edge_font_size=15, vertex_fill_color=part)

# improving cut
print("Improving cut")
dists = pairs_graph.new_vertex_property("int")
pos = 0
neg = 1
polarity = ["pos", "neg"]
if count1 < count2:
    pos, neg = neg, pos
    polarity = ["neg", "pos"]

bad_vertices = {}
for v in pairs_graph.vertices():
    dists[v] = 0
    for w in v.out_neighbours():
        if part[w] == pos:
            dists[v] += edge_weights[pairs_graph.edge(v, w)]
        else:
            dists[v] -= edge_weights[pairs_graph.edge(v, w)]
    # print(ver_names[v] + " is in " + polarity[part[v]] + " -> " + str(dists[v]))
    if part[v] == pos and dists[v] < 0:
        bad_vertices[v] = dists[v]
    elif part[v] == neg and dists[v] > 0:
        bad_vertices[v] = -dists[v]
    else:
        bad_vertices[v] = 0

worst_vertex = min(bad_vertices, key=bad_vertices.get)

max_iter = 1000
i = 0
while bad_vertices[worst_vertex] != 0 and i < max_iter:
    i += 1
    if (i % 10 == 0):
        print(i)
    # print(bad_vertices)
    part[worst_vertex] = 1 - part[worst_vertex]
    bad_vertices[worst_vertex] = 0
    for v in worst_vertex.out_neighbours():
        dists[v] = 0
        for w in v.out_neighbours():
            if part[w] == pos:
                dists[v] += edge_weights[pairs_graph.edge(v, w)]
            else:
                dists[v] -= edge_weights[pairs_graph.edge(v, w)]
        if part[v] == pos and dists[v] < 0:
            bad_vertices[v] = dists[v]
        elif part[v] == neg and dists[v] > 0:
            bad_vertices[v] = -dists[v]
        else:
            bad_vertices[v] = 0
    worst_vertex = min(bad_vertices, key=bad_vertices.get)

cut_value = 0
for e in pairs_graph.edges():
    if part[e.source()] != part[e.target()]:
        cut_value += edge_weights[e]

print("New cut value = " + str(cut_value))

f1 = open('new4_first_part.txt', 'w', encoding="utf-8")
f2 = open('new4_sec_part.txt', 'w', encoding="utf-8")

count1 = 0
count2 = 0
for key in word_dict.keys():
    # print(key)
    # print(part[pairs_graph.vertex(word_dict[key])])
    v = pairs_graph.vertex(word_dict[key])
    if largest_label[v] == 1:  # if only in largest component
        if part[v] == 0:
            count1 += 1
            f1.write(key + '\n')
        else:
            count2 += 1
            f2.write(key + '\n')
f1.close()
f2.close()

#pos = arf_layout(pairs_graph, max_iter=3)
#graph_draw(pairs_graph, pos=pos, vertex_text=ver_names, edge_text=edge_weights, vertex_size=5,  vertex_font_size=10,
#           edge_font_size=15, vertex_fill_color=part)
