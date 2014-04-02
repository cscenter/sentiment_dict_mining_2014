#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <set>

using namespace std;


vector <vector <pair <int, int> > > weight;
vector <vector <int> > graph;
vector <string> words;


int find(string word)
{
	for (int i = 0; i < words.size(); i++)
	{
		if (words[i] == word)
		{
			return i;
		}	
	}
	return -1;
}


int create_vertex(string word)
{
	int i = words.size();
	words.push_back(word);
	graph.push_back(vector <int>());
	weight.push_back(vector <pair <int, int> > ());
	return i;
}


void add_edge(string word1, string word2, int pos, int neg)
{
	int beg = find(word1);
	if (beg == -1)			
	{
		beg = create_vertex(word1);
	}

	int end = find(word2);
	if (end == -1)			
	{
		end = create_vertex(word2);
	}

    graph[beg].push_back(end);
    weight[beg].push_back(make_pair(pos, neg));
    graph[end].push_back(beg);
    weight[end].push_back(make_pair(pos, neg));
}


int the_most_heavy(set<int> Result, int i)
{
	int res = 0;
	for (int j = 0; j < graph[i].size(); j++)
	{
		if (Result.count(graph[i][j]) && weight[i][j].first > res)
		{
			res = weight[i][j].first;
		}
	}
	return res;	
}


int the_sum(set<int> Result, int i)
{
	int res = 0;
	for (int j = 0; j < graph[i].size(); j++)
	{
		if (Result.count(graph[i][j]))
		{
			res += weight[i][j].first;
		}
	}
	return res;	
}


set<int> analyze(vector<string> seed, int (*func)(set<int>, int))
{
	set<int> Result, Candidate;
	for (int i = 0; i < seed.size(); i++)
	{          
		Result.insert(find(seed[i]));
	}

	for (set<int> :: iterator it = Result.begin(); it != Result.end(); it++)
	{
		for (int i = 0; i < graph[*it].size(); i++)
		{
			if (!Result.count(graph[*it][i]))
			{
				Candidate.insert(graph[*it][i]);
			}
		}
	}

    while (true)
    {
    	int best_index = -1, best_max = 0;
    	for (set<int> :: iterator it = Candidate.begin(); it != Candidate.end(); it++)
    	{
    		int res = (*func)(Result, *it);
    		if (res > best_max)
    		{
    			best_index = *it;
    			best_max = res;
    		}
    	}
    	
    	if (best_index != -1)
    	{
    		Result.insert(best_index);
    		for (int i = 0; i < graph[best_index].size(); i++)
    		{
    			if (!Result.count(graph[best_index][i]))
    			{
    				Candidate.insert(graph[best_index][i]);
    			}
    		}
    		Candidate.erase(best_index);
    	}
    	else
    	{
    		break;
    	}
    }  
    return Result;
}

int main(int argc, char* argv[])
{
    if (argc != 3)
    {        
        cerr << "Usage: GraphAnalyzer.exe input_file output_file" << endl;    
    	return 0;
    }

	freopen(argv[1], "r", stdin);
	freopen(argv[2], "w", stdout);

	while (!feof(stdin))
	{
		string begin, end;
		int pos, neg;
		cin >> begin >> end >> pos >> neg; 
		add_edge(begin, end, pos, neg);   
	}

	vector <string> seed;
	seed.push_back("хороший");
	
	set <int> res = analyze(seed, the_most_heavy);
    for (set<int> :: iterator it = res.begin(); it != res.end(); it++)
    {
    	cout << words[*it] << endl;
    }

	return 0;
}