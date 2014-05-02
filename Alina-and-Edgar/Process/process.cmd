mystem -ngci -e utf-8 <row>input
cd ..\parser
C:\Python33\python parser.py ..\process\input ..\process\output
cd ..\GraphBuilder\src
C:\MinGW\bin\g++ -Wall main.cpp -o main.exe
main.exe ..\..\process\output ..\..\process\graph 0
cd ..\..\GraphAnalyzer
C:\Python33\python convert.py ..\process\graph ..\process\edges
C:\MinGW\bin\g++ GraphAnalyzer.cpp -o GraphAnalyzer.exe
GraphAnalyzer.exe ..\process\edges ..\Result\pos.txt ..\Result\neg.txt
