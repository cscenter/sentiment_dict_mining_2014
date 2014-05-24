rem mystem -ngci -e utf-8 <row>inp
rem python parser.py inp output
C:\MinGW\bin\g++ -Wall ..\..\GraphBuilder\main.cpp -o ..\..\GraphBuilder\main.exe
C:\MinGW\bin\g++ GraphAnalyzer.cpp -o GraphAnalyzer.exe

..\..\GraphBuilder\main.exe ..\test500\output graph0 0
python ..\..\GraphBuilder\convert.py graph0 edges0
GraphAnalyzer.exe edges0 pos0.txt neg0.txt

..\..\GraphBuilder\main.exe ..\test500\output graph1 1
python ..\..\GraphBuilder\convert.py graph1 edges1
GraphAnalyzer.exe edges1 pos1.txt neg1.txt

echo pos_recall =  > result0
python ..\..\testing\recall_testing.py pos0.txt ..\..\testing\500_pos.txt >> result0
echo neg_recall =  >> result0
python ..\..\testing\recall_testing.py neg0.txt ..\..\testing\500_neg.txt >> result0

python ..\..\testing\precision_filter.py pos0.txt neg0.txt ..\..\testing\500_pos.txt ..\..\testing\500_neg.txt res_pos0.txt res_neg0.txt
echo pos_precision =  >> result0
python ..\..\testing\precision_testing.py pos0.txt ..\..\testing\500_pos.txt >> result0
echo neg_precision =  >> result0
python ..\..\testing\precision_testing.py neg0.txt ..\..\testing\500_neg.txt >> result0

echo pos_recall =  > result1
python ..\..\testing\recall_testing.py pos1.txt ..\..\testing\500_pos.txt >> result1
echo neg_recall =  >> result1
python ..\..\testing\recall_testing.py neg1.txt ..\..\testing\500_neg.txt >> result1

python ..\..\testing\precision_filter.py pos1.txt neg1.txt ..\..\testing\500_pos.txt ..\..\testing\500_neg.txt res_pos1.txt res_neg1.txt
echo pos_precision =  >> result1
python ..\..\testing\precision_testing.py pos1.txt ..\..\testing\500_pos.txt >> result1
echo neg_precision =  >> result1
python ..\..\testing\precision_testing.py neg1.txt ..\..\testing\500_neg.txt >> result1