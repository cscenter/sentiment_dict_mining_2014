mystem -ngci -e utf-8 <hotel_no_tags.txt>inp
python ..\..\parser\parser.py inp output > out2
C:\MinGW\bin\g++ -Wall ..\..\GraphBuilder\main.cpp -o ..\..\GraphBuilder\main.exe

..\..\GraphBuilder\main.exe output graph0 0
python ..\..\GraphBuilder\convert.py graph0 edges0

..\..\GraphBuilder\main.exe output graph1 1
python ..\..\GraphBuilder\convert.py graph1 edges1
