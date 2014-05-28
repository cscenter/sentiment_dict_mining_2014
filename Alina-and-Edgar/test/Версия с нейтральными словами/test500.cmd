rem mystem -ngci -e utf-8 <row>inp
rem python parser.py inp output
rem C:\MinGW\bin\g++ -Wall ..\..\GraphBuilder\main.cpp -o ..\..\GraphBuilder\main.exe
rem C:\MinGW\bin\g++ GraphAnalyzer.cpp -o GraphAnalyzer.exe

rem ..\..\GraphBuilder\main.exe ..\test500\output graph0 0
rem python ..\..\GraphBuilder\convert.py graph0 edges0
rem GraphAnalyzer.exe edges0 test500\pos0.txt test500\neg0.txt

rem ..\..\GraphBuilder\main.exe ..\test500\output graph1 1
rem python ..\..\GraphBuilder\convert.py graph1 edges1
rem GraphAnalyzer.exe edges1 test500\pos1.txt test500\neg1.txt

echo pos_recall =  > test500\result0
python ..\..\testing\recall_testing.py test500\pos0.txt ..\..\testing\500_pos.txt >> test500\result0
echo neg_recall =  >> test500\result0
python ..\..\testing\recall_testing.py test500\neg0.txt ..\..\testing\500_neg.txt >> test500\result0

python ..\..\testing\precision_filter.py test500\pos0.txt test500\neg0.txt ..\..\testing\500_pos.txt ..\..\testing\500_neg.txt test500\res_pos0.txt test500\res_neg0.txt
echo pos_precision =  >> test500\result0
python ..\..\testing\precision_testing.py test500\pos0.txt ..\..\testing\500_pos.txt >> test500\result0
echo neg_precision =  >> test500\result0
python ..\..\testing\precision_testing.py test500\neg0.txt ..\..\testing\500_neg.txt >> test500\result0

echo pos_recall =  > test500\result1
python ..\..\testing\recall_testing.py test500\pos1.txt ..\..\testing\500_pos.txt >> test500\result1
echo neg_recall =  >> test500\result1
python ..\..\testing\recall_testing.py test500\neg1.txt ..\..\testing\500_neg.txt >> test500\result1

python ..\..\testing\precision_filter.py test500\pos1.txt test500\neg1.txt ..\..\testing\500_pos.txt ..\..\testing\500_neg.txt test500\res_pos1.txt test500\res_neg1.txt
echo pos_precision =  >> test500\result1
python ..\..\testing\precision_testing.py test500\pos1.txt ..\..\testing\500_pos.txt >> test500\result1
echo neg_precision =  >> test500\result1                                                              
python ..\..\testing\precision_testing.py test500\neg1.txt ..\..\testing\500_neg.txt >> test500\result1

