#encoding=utf-8
from graph_tool.all import Graph, label_components, graph_draw, label_largest_component, arf_layout
from graph_tool.flow import min_cut

filename = '../pairparser/results/en_pairs(7).txt'
print(filename)
coefficient = 3


word_dict = {}
add_dict = {}

f = open('bad.txt', 'r', encoding="utf-8")
for s in f:
    print(s.split(' ')[0])
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

    e = pairs_graph.add_edge(v1, v2)
    edge_weights[e] = cur_weight

components_label = label_components(pairs_graph)
largest_label = label_largest_component(pairs_graph)
#print(components_label[0].a)
#print(largest_label.a)

mc, part = min_cut(pairs_graph, edge_weights)

print(mc)
print(part)

f1 = open('first_part.txt', 'w', encoding="utf-8")
f2 = open('sec_part.txt', 'w', encoding="utf-8")
f3 = open('add_comp.txt', 'w', encoding="utf-8")
for key in word_dict.keys():
    # print(key)
    # print(part[pairs_graph.vertex(word_dict[key])])
    v = pairs_graph.vertex(word_dict[key])
    if largest_label[v] == 1:
        if part[v] == 0:
            f1.write(key + '\n')
        else:
            f2.write(key + '\n')
    else:
        f3.write(key + ' ' + str(components_label[0][v]) + ' ' + str(part[v]) + '\n')

f1.close()
f2.close()
f3.close()

v = pairs_graph.vertex(word_dict['отвратительный'])
topos = 0
toneg = 0
for w in v.out_neighbours():
    if part[w] == 0:
        topos += edge_weights[pairs_graph.edge(v, w)]
    else:
        toneg += edge_weights[pairs_graph.edge(v, w)]

print(topos)
print(toneg)

#pos = arf_layout(pairs_graph, max_iter=3)
#graph_draw(pairs_graph, pos=pos, vertex_text=ver_names, edge_text=edge_weights, vertex_size=1, vertex_font_size=2,
#           edge_font_size=4, output="gr.pdf", vertex_fill_color=part)







