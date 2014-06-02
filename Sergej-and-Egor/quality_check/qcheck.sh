find='7'
ftag='7_3imp'

bound1='l(-1)u(1)'
bound2='l(-2)u(3)'
bound3='l(-3)u(7)'
#bound4='l(-3)u(67)'
#bound5='l(-10)u(10)'


echo 'Без отделения нейтральных слов:'
python3 qualitycheck.py '../results/pos'$ftag'.txt' '../results/neg'$ftag'.txt' '../results/neu'$ftag'.txt' '../../testing/big_pos.txt' '../../testing/big_neu.txt' '../../testing/big_neg.txt'
echo '\nС отделением нейтральных слов по весу w_i = (s_+ - s_-) в отрезке: l(a)u(b) == [a, b]:'
echo $bound1
python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound1'.txt' '../results/neutral_cut/neg'$ftag$bound1'.txt' '../results/neutral_cut/neu'$ftag$bound1'.txt' '../../testing/big_pos.txt' '../../testing/big_neg.txt' '../../testing/big_neu.txt'
echo '\n'$bound2
python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound2'.txt' '../results/neutral_cut/neg'$ftag$bound2'.txt' '../results/neutral_cut/neu'$ftag$bound2'.txt' '../../testing/big_pos.txt' '../../testing/big_neg.txt' '../../testing/big_neu.txt'
echo '\n'$bound3
python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound3'.txt' '../results/neutral_cut/neg'$ftag$bound3'.txt' '../results/neutral_cut/neu'$ftag$bound3'.txt' '../../testing/big_pos.txt' '../../testing/big_neg.txt' '../../testing/big_neu.txt'
#echo '\n'$bound4' максимум для данного способа подсчёта веса w_i'
#python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound4'.txt' '../results/neutral_cut/neg'$ftag$bound4'.txt' '../results/neutral_cut/#neu'$ftag$bound4'.txt' '../../testing/big_pos.txt' '../../testing/big_neg.txt' '../../testing/big_neu.txt'

#echo '\n'$bound5' максимум для данного способа подсчёта веса w_i'
#python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound5'.txt' '../results/neutral_cut/neg'$ftag$bound5'.txt' '../results/neutral_cut/#neu'$ftag$bound5'.txt' '../../testing/big_pos.txt' '../../testing/big_neg.txt' '../../testing/big_neu.txt'

python3 qualitycheck.py 'pos.txt' 'neg.txt' 'neu.txt' '../../testing/big_pos.txt' '../../testing/big_neu.txt' '../../testing/big_neg.txt'
