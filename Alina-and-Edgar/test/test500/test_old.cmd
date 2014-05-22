rem mystem -ngci -e utf-8 <row>inp
rem C:\Python33\python parser.py inp output
C:\MinGW\bin\g++ -Wall main.cpp -o main.exe
C:\MinGW\bin\g++ GraphAnalyzer.cpp -o GraphAnalyzer.exe

main.exe output graph0 0
C:\Python33\python convert.py graph0 edges0
GraphAnalyzer.exe edges0 pos0.txt neg0.txt

main.exe output graph1 1
C:\Python33\python convert.py graph1 edges1
GraphAnalyzer.exe edges1 pos1.txt neg1.txt

echo pos_recall =  > result0
C:\Python33\python recall_testing.py pos0.txt 500_pos.txt >> result0
echo neg_recall =  >> result0
C:\Python33\python recall_testing.py neg0.txt 500_neg.txt >> result0

C:\Python33\python precision_filter.py pos0.txt neg0.txt 500_pos.txt 500_neg.txt res_pos0.txt res_neg0.txt
echo pos_precision =  >> result0
C:\Python33\python precision_testing.py pos0.txt 500_pos.txt >> result0
echo neg_precision =  >> result0
C:\Python33\python precision_testing.py neg0.txt 500_neg.txt >> result0

echo pos_recall =  > result1
C:\Python33\python recall_testing.py pos1.txt 500_pos.txt >> result1
echo neg_recall =  >> result1
C:\Python33\python recall_testing.py neg1.txt 500_neg.txt >> result1

C:\Python33\python precision_filter.py pos1.txt neg1.txt 500_pos.txt 500_neg.txt res_pos1.txt res_neg1.txt
echo pos_precision =  >> result1
C:\Python33\python precision_testing.py pos1.txt 500_pos.txt >> result1
echo neg_precision =  >> result1
C:\Python33\python precision_testing.py neg1.txt 500_neg.txt >> result1