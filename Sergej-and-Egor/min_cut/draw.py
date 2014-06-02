#encoding=utf-8
from graph_tool.all import Graph, label_components, graph_draw, label_largest_component, arf_layout, sfdp_layout
from graph_tool.flow import min_cut

filename = 'buf.txt'
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

    e = pairs_graph.add_edge(v1, v2)
    edge_weights[e] = cur_weight

components_label = label_components(pairs_graph)
largest_label = label_largest_component(pairs_graph)
#print(components_label[0].a)
print(largest_label.a)

degr = pairs_graph.new_vertex_property("int")

for v in pairs_graph.vertices():
    degr[v] = v.out_degree()    


print("hihi")
posPlot = sfdp_layout(pairs_graph, gamma = 5, max_level = 50, vweight = degr, C = 0.5, K = 5, p = 7, theta = 0.1)
print("hi")
graph_draw(pairs_graph, pos=posPlot, vertex_text=ver_names, edge_text=edge_weights)

# position = arf_layout(pairs_graph, max_iter=3)
# graph_draw(pairs_graph, pos=position, vertex_text=ver_names, edge_text=edge_weights, vertex_size=5, vertex_font_size=10,
#          edge_font_size=15, vertex_fill_color=part)

mc, part = min_cut(pairs_graph, edge_weights)

print("Cut value = " + str(mc))


group_property = pairs_graph.new_vertex_property("int")
for v in pairs_graph.vertices():
    if part[v] == 0:
        group_property[v] = 0
    else:
        group_property[v] = 1
color = pairs_graph.new_vertex_property("vector<double>")
s = ""
for v in pairs_graph.vertices():
    if part[v] == 0:
        s += "g"
        color[v] = [0.2, 0.6, 0.2, 0.9]
    else:
        s += "r"
        color[v] = [1, 0, 0, 0.9]
    if ver_names[v] == "дешевый":
        color[v] = [0.1, 0.2, 0.7, 0.9]
print("hihi")
posPlot = sfdp_layout(pairs_graph, groups = group_property, gamma = 5, max_level = 50, vweight = degr, C = 0.5, K = 5, p = 7, theta = 0.1)
print("hi")
graph_draw(pairs_graph, pos=posPlot,  vertex_fill_color=color, vertex_text=ver_names, edge_text=edge_weights)



#pos = arf_layout(pairs_graph, max_iter=3)
#graph_draw(pairs_graph, pos=pos, vertex_text=ver_names, edge_text=edge_weights, vertex_size=5,  vertex_font_size=10,
#           edge_font_size=15, vertex_fill_color=part)







