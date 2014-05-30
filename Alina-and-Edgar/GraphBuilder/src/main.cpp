#include <iostream>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <utility>
#include <string>
#include <algorithm>

void clean_string(std :: string& s) {
	for (std :: string :: iterator i = s.begin(); i != s.end(); ++i) {
		if ( *i == '(' || *i == ')' || *i == '\'' || *i == ',' || *i == ']' || *i == '[' ) {
			i = s.erase(i);
			--i;
		}
	}
}

void merge_words(std :: map<std:: string, std :: map<std :: string, std :: pair<int, int> > >& graph, std :: string a, std :: string b) {
	if (graph.find(a) != graph.end() && graph.find(b) != graph.end()) {
		std :: map<std :: string, std :: pair<int, int> > temp = graph[b];
		std :: map<std :: string, std :: pair<int, int> > :: iterator it;
		for (it = temp.begin(); it != temp.end(); ++it) {
			it->second.first *=(-1);
			it->second.second *= (-1);
			std :: swap(it->second.first, it->second.second);
			if (graph[a].find(it->first) != graph[a].end()) {
				graph[a][it->first].first += it->second.first;
				graph[a][it->first].second += it->second.second;
			} else {
				graph[a][it->first] = it->second;
			}
		}
		std :: map<std:: string, std :: map<std :: string, std :: pair<int, int> > > :: iterator i;
		for (i = graph.begin(); i != graph.end(); ++i) {
            if (i->second.find(b) != i->second.end()) {
                i->second.erase(b);
            }
		}
		graph.erase(b);
	}
}

void add_edge(std :: map<std:: string, std :: map<std :: string, std :: pair<int, int> > >& graph, std :: string first_adj, std :: string second_adj, int polarity) {
        if (graph.find(first_adj) == graph.end()) {
				if (polarity > 0) {
					graph[first_adj][second_adj] = std :: make_pair(polarity, 0);
				} else {
					graph[first_adj][second_adj] = std :: make_pair(0, polarity);
				}
			} else {
				if (graph[first_adj].find(second_adj) == graph[first_adj].end()) {
					if (polarity > 0) {
						graph[first_adj][second_adj] = std :: make_pair(polarity, 0);
					} else {
						graph[first_adj][second_adj] = std :: make_pair(0, polarity);
					}
				} else {
					int pos_polarity = graph[first_adj][second_adj].first;
					int neg_polarity = graph[first_adj][second_adj].second;
					if (polarity > 0) {
						graph[first_adj][second_adj] = std :: make_pair(pos_polarity + polarity, neg_polarity);
					} else {
						graph[first_adj][second_adj] = std :: make_pair(pos_polarity, neg_polarity + polarity);
					}
				}
			}
}

int main(int argc, char** argv) {
	if (argc != 4) {
		std :: cerr << "Usage: GraphBuilder.exe input_file output_file enable_merge(1/0)" << std :: endl;
	} else {
		const char* input_file = argv[1];
		const char* output_file = argv[2];
		std :: ifstream ifs(input_file, std :: ifstream :: in);
		std :: ofstream ofs(output_file, std :: ifstream :: out);
		std :: map<std:: string, std :: map<std :: string, std :: pair<int, int> > > graph;
		while (!ifs.eof()) {
			std :: string first_adj, second_adj, num;
			ifs >> first_adj >> second_adj >> num;
			clean_string(first_adj);
			clean_string(second_adj);
			clean_string(num);
			int polarity = atoi(num.c_str());
			add_edge(graph, first_adj, second_adj, polarity);
			add_edge(graph, second_adj, first_adj, polarity);
		}

		if (atoi(argv[3]) == 1) {
			std :: map<std :: string, std :: map<std :: string, std :: pair<int, int> > > :: iterator it;
			for (it = graph.begin(); it != graph.end(); ++it) {
				std :: string word = it->first;
				std :: string anti_word = "не" + word;
				if (graph.find(anti_word) != graph.end()) {
					merge_words(graph, word, anti_word);
				}
			}
		}

		std :: map<std :: string, std :: map<std :: string, std :: pair<int, int> > > :: iterator it;
		for (it = graph.begin(); it != graph.end(); ++it) {
            if (!it->second.empty()) {
                    std :: map<std :: string, std :: pair<int, int> > :: iterator v_it;
                    ofs << it->first << ": ";
                    for (v_it = it->second.begin(); v_it != it->second.end(); ++v_it) {
                        ofs << v_it->first << " " << v_it->second.first << " " << v_it->second.second << "; ";
                    }
                    ofs << std :: endl;
            }
		}
		ifs.close();
		ofs.close();
	}

	return 0;
}
