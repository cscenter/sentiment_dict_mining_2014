#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <set>

using namespace std;


vector <vector <pair <double, double> > > w;
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
	w.push_back(vector <pair <double, double> > ());
	return i;
}


void add_edge(string word1, string word2, double pos, double neg)
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


double the_most_heavy(set<int> Result, set<int> Opposite, int i)
{
	double res_pos = 0, res_neg = 0;
	for (int j = 0; j < g[i].size(); j++)
	{
		if (Result.count(g[i][j]) && w[i][j].first + w[i][j].second > res_pos)
		{
			res_pos = w[i][j].first + w[i][j].second;
		}
		if (Opposite.count(g[i][j]) && w[i][j].first + w[i][j].second > res_neg)
		{
			res_neg = w[i][j].first + w[i][j].second;
		}
	}
	return res_pos - res_neg;	
}


double the_sum(set<int> Result, set<int> Opposite, int i)
{
	int res = 0;
	for (int j = 0; j < g[i].size(); j++)
	{
		if (Result.count(g[i][j]))
		{
			res += w[i][j].first + w[i][j].second;
		}
		if (Opposite.count(g[i][j]))
		{
			res -= w[i][j].first + w[i][j].second;
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

bool add_vertex(set<int> *Result, set<int> *Opposite, set<int> *Candidate, double (*func)(set<int>, set<int>, int))
{
	int best_index = -1, best_max = -10000000;
	for (set<int> :: iterator it = Candidate->begin(); it != Candidate->end(); it++)
	{
		double res = (*func)(*Result, *Opposite, *it);
		if (res > best_max)
		{
			best_index = *it;
			best_max = res;
		}
	}
	
	//cerr << best_index << endl;
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
		return true;
	}

	freopen("err", "a", stderr);
	if (best_index !=  -1)
	{
		cerr << words[best_index] << endl;
	}
	fclose(stderr);
	
	return Opposite->count(best_index) ? false : true;
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


void analyze(vector<string> seed_pos, vector<string> seed_neg, double (*func)(set<int>, set<int>, int))
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
    while (true)
    {
    	if (step)
    	{
    		if (!add_vertex(&Result_pos, &Result_neg, &Candidate_pos, (*func)))
    			break;
    	}
    	else
    	{
    		if (!add_vertex(&Result_neg, &Result_pos, &Candidate_neg, (*func)))
    			break;
    	}
    	step = 1 - step;
    	if (Candidate_pos.size() == 0 && Candidate_neg.size() == 0)
    		break;
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
		double pos, neg;
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
	
	analyze(seed_pos, seed_neg, the_sum);

	return 0;
}