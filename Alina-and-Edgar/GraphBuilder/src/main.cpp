#include <iostream>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <vector>
#include <string>

void clean_string(std :: string& s){
    for (std :: string :: iterator i = s.begin(); i != s.end(); ++i){
        if ( *i == '(' || *i == ')' || *i == '\'' || *i == ',' || *i == ']' || *i == '[' ){
            i = s.erase(i);
            --i;
        }
    }
}

int main(int argc, char** argv)
{
    if (argc != 3){
        std :: cerr << "Usage: build.exe input_file output_file" << std :: endl;
    } else {
        const char* input_file = argv[1];
        const char* output_file = argv[2];

        std :: ifstream ifs(input_file, std :: ifstream :: in);
        std :: ofstream ofs(output_file, std :: ifstream :: out);

        //std :: map<std :: string, std :: vector<std :: pair<std :: string, int> > > graph;
        std :: map<std:: string, std :: map<std :: string, int > > graph;


        while (!ifs.eof()){
            std :: string first_adj, second_adj, num;
            ifs >> first_adj >> second_adj >> num;

            clean_string(first_adj);
            clean_string(second_adj);
            clean_string(num);

            graph[first_adj][second_adj] = atoi(num.c_str());

            //graph[first_adj].push_back(std :: make_pair(second_adj, atoi(num.c_str())));

        }


        //std :: map<std :: string, std :: vector<std :: pair<std :: string, int> > > :: iterator it;

        std :: map<std:: string, std :: map<std :: string, int > > :: iterator it;

        for (it = graph.begin(); it != graph.end(); ++it){
            //std :: vector<std :: pair<std :: string, int> > :: iterator v_it;
            std :: map<std :: string, int > :: iterator v_it;

            ofs << it->first << ": ";
            for (v_it = it->second.begin(); v_it != it->second.end(); ++v_it){
                ofs << v_it->first << " ";
            }
            ofs << std :: endl;
        }

        ifs.close();
        ofs.close();
    }




    return 0;
}
