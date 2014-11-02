#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>
#include <vector>
#include <set>

using namespace std;

const int K = 1;
vector <vector <pair <int, int> > > w;
vector <vector <int> > g;
vector <string> words;
vector <int> pos_dist, neg_dist;
char *posFile, *negFile;


//заменить на map
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
	pos_dist.push_back(0);
	neg_dist.push_back(0);
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
    w[beg].push_back(make_pair(pos, K * neg));
    //g[end].push_back(beg);
    //w[end].push_back(make_pair(pos, K * neg));
}


void push_vertex(set<int> &Result, set<int> &Opposite, set<int> &Candidate, int best_index, vector<int> &dist, ofstream& fres)
{
	if (Result.count(best_index) || Opposite.count(best_index))
		return;

	fres << words[best_index] << endl;
	Result.insert(best_index);
	for (int i = 0; i < g[best_index].size(); i++)
	{
		dist[g[best_index][i]] += (w[best_index][i].first + w[best_index][i].second);
		if (!Result.count(g[best_index][i]) && !Opposite.count(g[best_index][i]))
		{
			Candidate.insert(g[best_index][i]);
		}
	}
}


void compute_dist(set<int> &Result, set<int> &Opposite, vector<int> &dist, vector<int> &opp_dist)
{
	for (int i = 0; i < dist.size(); i++)
	{
		int res = 0, opp_res = 0;
		for (int j = 0; j < g[i].size(); j++)
		{
			if (Result.count(g[i][j]))
			{
				res += (w[i][j].first + w[i][j].second);
			}
			if (Opposite.count(g[i][j]))
			{
				opp_res += (w[i][j].first + w[i][j].second);
			}

		}	
		dist[i] = res;
		opp_dist[i] = opp_res;
	}
}

void add_vertex(set<int> &Result, set<int> &Opposite, set<int> &Candidate, ofstream& fres, vector<int> &dist, vector<int> &opp_dist)
{
	int best_index = -1, best_max = -1000000000;
	
	for (set<int> :: iterator it = Candidate.begin(); it != Candidate.end(); it++)
	{
		if (*it < 0)
			continue;

		if (dist[*it] - opp_dist[*it] > best_max)
		{
			best_index = *it;
			best_max = dist[*it] - opp_dist[*it];
		}
	}
	
	if (best_index == -1)
		return;

	if (!Opposite.count(best_index))
	{
		push_vertex(Result, Opposite, Candidate, best_index, dist, fres);
	}

	Candidate.erase(best_index);
}

void out(set<int>& res, char* filename)
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

void analyze(vector<string>& seed_pos, vector<string>& seed_neg, ofstream& fpos, ofstream& fneg)
{
	set<int> Result_pos, Result_neg;
	set <int> Candidate_pos;
	for (int i = 0; i < seed_pos.size(); i++)
	{
		if (get_index(seed_pos[i]) != -1)
			push_vertex(Result_pos, Result_neg, Candidate_pos, get_index(seed_pos[i]), pos_dist, fpos);
	}

	set <int> Candidate_neg;
	for (int i = 0; i < seed_neg.size(); i++)
	{
		if (get_index(seed_neg[i]) != -1)
			push_vertex(Result_neg, Result_pos, Candidate_neg, get_index(seed_neg[i]), neg_dist, fneg);
	}

	int step = 1;
    while (Candidate_pos.size() != 0 || Candidate_neg.size() != 0)
    {
    	if (step)
    	{
    		add_vertex(Result_pos, Result_neg, Candidate_pos, fpos, pos_dist, neg_dist);
    	}
    	else
    	{
    		add_vertex(Result_neg, Result_pos, Candidate_neg, fneg, neg_dist, pos_dist);
    	}
    	step = 1 - step;
    }  
    fpos.close();
    fneg.close();

    for (int t = 0; t < 0; t++)
    {
        compute_dist(Result_pos, Result_neg, pos_dist, neg_dist);
        Result_pos.clear();
        Result_neg.clear();
        for (int i = 0; i < pos_dist.size(); i++)
        {
        	if (pos_dist[i] - neg_dist[i] > 3)
        		Result_pos.insert(i);
        	if (pos_dist[i] - neg_dist[i] < 0)
        		Result_neg.insert(i);
        }
    
        //out(Result_pos, posFile);
        //out(Result_neg, negFile);   
    }

    compute_dist(Result_pos, Result_neg, pos_dist, neg_dist);

    ofstream fplot;
    fplot.open("big_test/plot.csv");

    for (int i = 0; i < pos_dist.size(); i++)
    {
    	fplot << words[i] << "," << pos_dist[i] - neg_dist[i] << endl;
    }
    fplot.close();
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
		add_edge(begin, end, pos, neg);   
	}
	fclose(stdin);

	ofstream fpos, fneg;
	fpos.open(posFile);	
	fneg.open(negFile);


	vector <string> seed_pos ;
	seed_pos.push_back("хороший");
	seed_pos.push_back("отличный");
	seed_pos.push_back("замечательный");
	seed_pos.push_back("прекрасный");
	seed_pos.push_back("лучший");

	vector <string> seed_neg ;
	seed_neg.push_back("плохой");
	seed_neg.push_back("ужасный");
	seed_neg.push_back("отвратительный");
	seed_neg.push_back("худший");
	seed_neg.push_back("отвратный");
	seed_neg.push_back("убогий");


	//freopen("neutral", "a", stderr);
	analyze(seed_pos, seed_neg, fpos, fneg);
	//fclose(stderr);
    //fpos.close();
    //fneg.close();

	return 0;
}