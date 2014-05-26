rem mystem -ngci -e utf-8 <hotel_no_tags.txt>inp
rem C:\Python33\python parser.py inp output
rem C:\MinGW\bin\g++ -Wall main.cpp -o main.exe
rem main.exe output graph0 0
rem main.exe output graph1 1
C:\Python33\python convert.py graph0 edges0
C:\Python33\python convert.py graph1 edges1
C:\MinGW\bin\g++ GraphAnalyzer.cpp -o GraphAnalyzer.exe
GraphAnalyzer.exe edges0 sum_pos0.txt sum_neg0.txt
GraphAnalyzer.exe edges1 sum_pos1.txt sum_neg1.txt
rem GraphAnalyzer.exe edges0 heavy_pos0.txt heavy_neg0.txt
rem GraphAnalyzer.exe edges heavy_pos.txt heavy_neg.txt
rem echo pos_recall =  > result
rem C:\Python33\python recall_testing.py pos.txt 500_pos.txt >> result
rem echo neg_recall =  >> result
rem C:\Python33\python recall_testing.py neg.txt 500_neg.txt >> result
rem C:\Python33\python precision_filter.py pos.txt neg.txt 500_pos.txt 500_neg.txt res_pos.txt res_neg.txt
rem echo pos_precision =  >> result
rem C:\Python33\python precision_testing.py pos.txt 500_pos.txt >> result
rem echo neg_precision =  >> result
rem rem C:\Python33\python precision_testing.py neg.txt 500_neg.txt >> result