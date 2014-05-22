#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <set>

using namespace std;

const int K = 1;
vector <vector <pair <int, int> > > w;
vector <vector <int> > g;
vector <string> words;
char *posFile, *negFile;


int get_index(string word)
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
	g.push_back(vector <int>());
	w.push_back(vector <pair <int, int> > ());
	return i;
}


void add_edge(string word1, string word2, int pos, int neg)
{
	int beg = get_index(word1);
	if (beg == -1)			
	{
		beg = create_vertex(word1);
	}

	int end = get_index(word2);
	if (end == -1)			
	{
		end = create_vertex(word2);
	}

    g[beg].push_back(end);
    w[beg].push_back(make_pair(pos, neg));
    g[end].push_back(beg);
    w[end].push_back(make_pair(pos, neg));
}


int the_most_heavy(set<int> Result, set<int> Opposite, int i)
{
	int res_pos = 0, res_neg = 0;
	for (int j = 0; j < g[i].size(); j++)
	{
		if (Result.count(g[i][j]) && w[i][j].first + w[i][j].second > res_pos)
		{
			res_pos = w[i][j].first + K * w[i][j].second;
		}
		if (Opposite.count(g[i][j]) && w[i][j].first + w[i][j].second > res_neg)
		{
			res_neg = w[i][j].first + K * w[i][j].second;
		}
	}
	return res_pos - res_neg;	
}


int the_sum(set<int> Result, set<int> Opposite, int i, int k)
{
	int res = 0;
	for (int j = 0; j < g[i].size(); j++)
	{
		if (Result.count(g[i][j]))
		{
			res += w[i][j].first + k * w[i][j].second;
		}
		if (Opposite.count(g[i][j]))
		{
			res -= w[i][j].first + k * w[i][j].second;
		}
	}
	return res;	
}

set<int> init(set<int> Result, set<int> Opposite)
{
    set<int> Candidate;
    for (set<int> :: iterator it = Result.begin(); it != Result.end(); it++)
	{
		if (*it < 0)
			continue;
		for (int i = 0; i < g[*it].size(); i++)
		{
			if (!Result.count(g[*it][i]) && !Opposite.count(g[*it][i]))
			{
				Candidate.insert(g[*it][i]);
			}
		}
	}
	
	return Candidate;
}

void add_vertex(set<int> *Result, set<int> *Opposite, set<int> *Candidate, int (*func)(set<int>, set<int>, int, int), int k)
{
	int best_index = -1, best_max = -1000000000;
	for (set<int> :: iterator it = Candidate->begin(); it != Candidate->end(); it++)
	{
		int res = (*func)(*Result, *Opposite, *it, k);
		if (res > best_max)
		{
			best_index = *it;
			best_max = res;
		}
	}
	
	if (best_index != -1 && !Opposite->count(best_index))
	{
		Result->insert(best_index);
		for (int i = 0; i < g[best_index].size(); i++)
		{
			if (!Result->count(g[best_index][i]) && !Opposite->count(g[best_index][i]))
			{
				Candidate->insert(g[best_index][i]);
			}
		}

		Candidate->erase(best_index);
		return;
	}

	if (best_index !=  -1)
	{
		cerr << words[best_index] << endl;
		Candidate->erase(best_index);
	}
}


void out(set<int> res, char* filename)
{
	freopen(filename, "w", stdout);
	for (set<int> :: iterator it = res.begin(); it != res.end(); it++)
    {
    	if (*it < 0)
    		continue;
    	cout << words[*it] << endl;
    }
    fclose(stdout);
}


void analyze(vector<string> seed_pos, vector<string> seed_neg, int (*func)(set<int>, set<int>, int, int))
{
	set<int> Result_pos, Result_neg;

	for (int i = 0; i < seed_pos.size(); i++)
	{          
		Result_pos.insert(get_index(seed_pos[i]));
	}

	for (int i = 0; i < seed_neg.size(); i++)
	{          
		Result_neg.insert(get_index(seed_neg[i]));
	}
	        
	set<int> Candidate_pos = init(Result_pos, Result_neg); 
	set<int> Candidate_neg = init(Result_neg, Result_pos); 
	       
	int step = 1;
    while (Candidate_pos.size() != 0 || Candidate_neg.size() != 0)
    {
    	if (step)
    	{
    		add_vertex(&Result_pos, &Result_neg, &Candidate_pos, (*func), K);
    	}
    	else
    	{
    		add_vertex(&Result_neg, &Result_pos, &Candidate_neg, (*func), 1);
    	}
    	step = 1 - step;
    }  

    out(Result_pos, posFile);
    out(Result_neg, negFile);
}


int main(int argc, char* argv[])
{
    if (argc != 4)
    {        
        cerr << "Usage: GraphAnalyzer.exe input_file pos_file neg_file" << endl;    
    	return 0;
    }

	posFile = argv[2];
	negFile = argv[3];

	freopen(argv[1], "r", stdin);
	while (!feof(stdin))
	{
		string begin, end;
		int pos, neg;
		cin >> begin >> end >> pos >> neg;
		//cout << begin << " " << end <<  " " << pos << " " << neg << endl;
		//if (begin != "" && end != "")
			add_edge(begin, end, pos, neg);   
	}
	fclose(stdin);

	vector <string> seed_pos;
	seed_pos.push_back("хороший");
	vector <string> seed_neg;
	seed_neg.push_back("плохой");
	
	freopen("neutral", "a", stderr);
	analyze(seed_pos, seed_neg, the_sum);
	fclose(stderr);

	return 0;
}