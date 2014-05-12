find='4'
ftag='4_3'

bound1='l(-1)u(1)'
bound2='l(-2)u(3)'
bound3='l(-3)u(7)'
bound4='l(-3)u(35)'
bound5='l(-1)u(14.2)'


echo 'Без отделения нейтральных слов:'
python3 qualitycheck.py '../results/pos'$ftag'.txt' '../results/neut'$ftag'.txt' '../results/neg'$ftag'.txt' '../../testing/big_pos.txt' '../../testing/big_neut.txt' '../../testing/big_neg.txt'
echo '\nС отделением нейтральных слов по весу w_i = (s_+ - s_-) в отрезке: l(a)u(b) == [a, b]:'
echo $bound1
python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound1'.txt' '../results/neutral_cut/neu'$ftag$bound1'.txt' '../results/neutral_cut/neg'$ftag$bound1'.txt' '../../testing/big_pos.txt' '../../testing/big_neut.txt' '../../testing/big_neg.txt'
echo '\n'$bound2
python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound2'.txt' '../results/neutral_cut/neu'$ftag$bound2'.txt' '../results/neutral_cut/neg'$ftag$bound2'.txt' '../../testing/big_pos.txt' '../../testing/big_neut.txt' '../../testing/big_neg.txt'
echo '\n'$bound3
python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound3'.txt' '../results/neutral_cut/neu'$ftag$bound3'.txt' '../results/neutral_cut/neg'$ftag$bound3'.txt' '../../testing/big_pos.txt' '../../testing/big_neut.txt' '../../testing/big_neg.txt'
echo '\n'$bound4' максимум для данного способа подсчёта веса w_i'
python3 qualitycheck.py '../results/neutral_cut/pos'$ftag$bound4'.txt' '../results/neutral_cut/neu'$ftag$bound4'.txt' '../results/neutral_cut/neg'$ftag$bound4'.txt' '../../testing/big_pos.txt' '../../testing/big_neut.txt' '../../testing/big_neg.txt'

echo '\n'$bound5' максимум для подсчёта вес как w_i = (s_+ - s_-) / deg_i'
python3 qualitycheck.py '../results/neutral_cut/posD'$ftag$bound5'.txt' '../results/neutral_cut/neuD'$ftag$bound5'.txt' '../results/neutral_cut/negD'$ftag$bound5'.txt' '../../testing/big_pos.txt' '../../testing/big_neut.txt' '../../testing/big_neg.txt'


