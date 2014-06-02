rem mystem -ngci -e utf-8 <row>inp
rem python parser.py inp output
rem C:\MinGW\bin\g++ -Wall ..\..\GraphBuilder\main.cpp -o ..\..\GraphBuilder\main.exe
C:\MinGW\bin\g++ GraphAnalyzer.cpp -o GraphAnalyzer.exe

rem ..\..\GraphBuilder\main.exe ..\big_test\output graph0 0
rem python ..\..\GraphBuilder\convert.py graph0 edges0
rem GraphAnalyzer.exe ..\big_test\edges0 big_test\pos0.txt big_test\neg0.txt

rem ..\..\GraphBuilder\main.exe ..\big_test\output graph1 1
rem python ..\..\GraphBuilder\convert.py graph1 edges1
rem GraphAnalyzer.exe ..\big_test\edges1 big_test\pos1.txt big_test\neg1.txt

echo pos_recall =  > big_test\big_result0
python ..\..\testing\recall_testing.py big_test\pos0.txt ..\..\testing\big_pos.txt >> big_test\big_result0
echo neg_recall =  >> big_test\big_result0
python ..\..\testing\recall_testing.py big_test\neg0.txt ..\..\testing\big_neg.txt >> big_test\big_result0

echo pos_recall =  > big_test\500_result0
python ..\..\testing\recall_testing.py big_test\pos0.txt ..\..\testing\500_pos.txt >> big_test\500_result0
echo neg_recall =  >> big_test\500_result0
python ..\..\testing\recall_testing.py big_test\neg0.txt ..\..\testing\500_neg.txt >> big_test\500_result0


python ..\..\testing\precision_filter.py big_test\pos0.txt big_test\neg0.txt ..\..\testing\500_pos.txt ..\..\testing\500_neg.txt big_test\res_pos0.txt big_test\res_neg0.txt
rem echo pos_precision =  >> big_test\result0
rem python ..\..\testing\precision_testing.py big_test\pos0.txt ..\..\testing\500_pos.txt >> big_test\result0
rem echo neg_precision =  >> big_test\result0
rem python ..\..\testing\precision_testing.py big_test\neg0.txt ..\..\testing\500_neg.txt >> big_test\result0

echo pos_recall =  > big_test\big_result1
python ..\..\testing\recall_testing.py big_test\pos1.txt ..\..\testing\big_pos.txt >> big_test\big_result1
echo neg_recall =  >> big_test\big_result1
python ..\..\testing\recall_testing.py big_test\neg1.txt ..\..\testing\big_neg.txt >> big_test\big_result1

echo pos_recall =  > big_test\500_result1
python ..\..\testing\recall_testing.py big_test\pos1.txt ..\..\testing\500_pos.txt >> big_test\500_result1
echo neg_recall =  >> big_test\500_result1
python ..\..\testing\recall_testing.py big_test\neg1.txt ..\..\testing\500_neg.txt >> big_test\500_result1


python ..\..\testing\precision_filter.py big_test\pos1.txt big_test\neg1.txt ..\..\testing\500_pos.txt ..\..\testing\500_neg.txt big_test\res_pos1.txt big_test\res_neg1.txt
rem echo pos_precision =  >> big_test\result1
rem python ..\..\testing\precision_testing.py big_test\pos1.txt ..\..\testing\500_pos.txt >> big_test\result1
rem echo neg_precision =  >> big_test\result1                                                              
rem python ..\..\testing\precision_testing.py big_test\neg1.txt ..\..\testing\500_neg.txt >> big_test\result1

