find='7'
ftag='7_5p'

bound1='l(-1)u(1)'
bound2='l(-2)u(3)'
bound3='l(-3)u(7)'
#bound4='l(-6.112)u(82.224)'
#bound5='l(-10)u(10)'

echo 'Без отделения нейтральных слов:'
python3 completenesscheck.py '../results/pos'$ftag'.txt' '../results/neut'$ftag'.txt' '../results/neg'$ftag'.txt' '../../testing/500_pos.txt' '../../testing/500_neu.txt' '../../testing/500_neg.txt' '../results/transformed'$find'.txt'
echo '\nС отделением нейтральных слов по весу w_i = (s_+ - s_-) в отрезке: l(a)u(b) == [a, b]:'
echo $bound1
python3 completenesscheck.py '../results/neutral_cut/pos'$ftag$bound1'.txt' '../results/neutral_cut/neu'$ftag$bound1'.txt' '../results/neutral_cut/neg'$ftag$bound1'.txt' '../../testing/500_pos.txt' '../../testing/500_neu.txt' '../../testing/500_neg.txt' '../results/transformed'$find'.txt'
echo '\n'$bound2
python3 completenesscheck.py '../results/neutral_cut/pos'$ftag$bound2'.txt' '../results/neutral_cut/neu'$ftag$bound2'.txt' '../results/neutral_cut/neg'$ftag$bound2'.txt' '../../testing/500_pos.txt' '../../testing/500_neu.txt' '../../testing/500_neg.txt' '../results/transformed'$find'.txt'
echo '\n'$bound3
python3 completenesscheck.py '../results/neutral_cut/pos'$ftag$bound3'.txt' '../results/neutral_cut/neu'$ftag$bound3'.txt' '../results/neutral_cut/neg'$ftag$bound3'.txt' '../../testing/500_pos.txt' '../../testing/500_neu.txt' '../../testing/500_neg.txt' '../results/transformed'$find'.txt'
#echo '\n'$bound4' максимум для данного способа подсчёта веса w_i'
#python3 completenesscheck.py '../results/neutral_cut/pos'$ftag$bound4'.txt' '../results/neutral_cut/neu'$ftag$bound4'.txt' '../results/neutral_cut/#neg'$ftag$bound4'.txt' '../../testing/500_pos.txt' '../../testing/500_neu.txt' '../../testing/500_neg.txt' '../results/transformed'$find'.txt'
#echo '\n'$bound5' максимум для данного способа подсчёта веса w_i'
#python3 completenesscheck.py '../results/neutral_cut/pos'$ftag$bound5'.txt' '../results/neutral_cut/neu'$ftag$bound5'.txt' '../results/neutral_cut/#neg'$ftag$bound5'.txt' '../../testing/500_pos.txt' '../../testing/500_neu.txt' '../../testing/500_neg.txt' '../results/transformed'$find'.txt'
