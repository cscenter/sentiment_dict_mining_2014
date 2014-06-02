get_degree <- function(word, df) {
  return(nrow(df[ df$a1 == word| df$a2 == word, ]))
}

get_sum_pos_deg <- function(word, df) {
  return(nrow(df[ (df$a1 == word| df$a2 == word) & df$pos + df$neg > 0, ]))
}

get_sum_neg_deg <- function(word, df) {
  return(nrow(df[ (df$a1 == word| df$a2 == word) & df$pos + df$neg < 0, ]))
}

get_pos_val <- function(word, df) {
  return(sum(df[ df$a1 == word| df$a2 == word, "pos"]))
}

get_neg_val <- function(word, df) {
  return(-sum(df[ df$a1 == word| df$a2 == word, "neg"]))
}

fpre = '7_5p'

spl = strsplit(getwd(), '/')
nwd = paste(spl[[1]][1:(length(spl[[1]]) - 2)], collapse = '/')
nwd = paste(nwd, "results", sep = "/")

fname = paste(c("pos", fpre, ".txt"), collapse='')
pos_dict = scan(paste(nwd, fname, sep = "/"), what=character())
fname = paste(c("neg", fpre, ".txt"), collapse='')
neg_dict = scan(paste(nwd, fname, sep = "/"), what=character())

sums = read.table(paste(c("sums", fpre, ".txt"), collapse=''), stringsAsFactors=FALSE, col.names = c('word', 's'))
sums = sums[order(sums[[2]], decreasing=TRUE), c('word', 's')]

upper.bound = 3
lower.bound = -2

new_neu = sums[ sums$s <= upper.bound & sums$s >= lower.bound, 'word']
new_neg = sums[ sums$s < lower.bound, 'word' ]
new_pos = sums[ sums$s > upper.bound, 'word' ]

pname = paste(c('pos', fpre, 'l(', as.character(lower.bound), ')u(', as.character(upper.bound), ').txt'), collapse='')
negname = paste(c('neg', fpre, 'l(', as.character(lower.bound), ')u(', as.character(upper.bound), ').txt'), collapse='')
neuname = paste(c('neu', fpre, 'l(', as.character(lower.bound), ')u(', as.character(upper.bound), ').txt'), collapse='')
fpos =  paste('../results/neutral_cut/', pname, sep='/')
fneg = paste('../results/neutral_cut/', negname, sep='/')
fneu = paste('../results/neutral_cut/', neuname, sep='/')
write.table(new_pos, file = fpos, sep = ' ',  col.names = FALSE, quote = FALSE, row.names = FALSE)
write.table(new_neg, file = fneg, sep = ' ',  col.names = FALSE, quote = FALSE, row.names = FALSE)
write.table(new_neu, file = fneu, sep = ' ',  col.names = FALSE, quote = FALSE, row.names = FALSE)

# finding max quality
big_neg = read.table('../../testing/big_neg.txt', stringsAsFactors=FALSE, col.names = c('word'))
big_neg = big_neg[,'word']
big_pos = read.table('../../testing/big_pos.txt', stringsAsFactors=FALSE, col.names = c('word'))
big_pos = big_pos[,'word']
big_neu = read.table('../../testing/big_neu.txt', stringsAsFactors=FALSE, col.names = c('word'))
big_neu = big_neu[,'word']

big_len = length(big_neg) + length(big_pos) + length(big_neu)

get_quality <- function(pos, neg, neu)
{
  neg_ok = length(intersect(big_neg, neg))
  pos_ok = length(intersect(big_pos, pos))
  neu_ok = length(intersect(big_neu, neu))
  
  return((neg_ok + pos_ok + neu_ok) * 100 / big_len)
}

# Q for s(+) - s(-)

sums = read.table(paste(c("../analysis/resanalysis/weights/sums", fpre, ".txt"), collapse=''), stringsAsFactors=FALSE, col.names = c('word', 's'))
sums = sums[order(sums[[2]], decreasing=TRUE), c('word', 's')]

borders = sort(unique(sums[, 's']))

cur_q = 0
max_q_l = 0
max_q_u = 0
for (i in 1:length(borders)) {
  for (j in 1:i) {
    up = borders[i]
    lo = borders[j]
    # str = paste(c('[', as.character(lo), ', ', as.character(up), ']'), collapse='')
    # print(str)
    new_neu = sums[ sums$s <= up & sums$s >= lo, 'word']
    new_neg = sums[ sums$s < lo, 'word' ]
    new_pos = sums[ sums$s > up, 'word' ]
    q = get_quality(new_pos, new_neg, new_neu)
    if (q > cur_q) {
      cur_q = q
      max_q_l = lo
      max_q_u = up
      str = paste(c('[', as.character(lo), ', ', as.character(up), '] ', 'quality = ', as.character(q)), collapse='')
      print(str)
    }
  }
}
str = paste(c('[', as.character(max_q_l), ', ', as.character(max_q_u), '] ', 'quality = ', as.character(cur_q)), collapse='')
print(str)

lower.bound = max_q_l
upper.bound = max_q_u

new_neu = sums[ sums$s <= upper.bound & sums$s >= lower.bound, 'word']
new_neg = sums[ sums$s < lower.bound, 'word' ]
new_pos = sums[ sums$s > upper.bound, 'word' ]


pname = paste(c('pos', fpre, 'l(', as.character(lower.bound), ')u(', as.character(upper.bound), ').txt'), collapse='')
negname = paste(c('neg', fpre, 'l(', as.character(lower.bound), ')u(', as.character(upper.bound), ').txt'), collapse='')
neuname = paste(c('neu', fpre, 'l(', as.character(lower.bound), ')u(', as.character(upper.bound), ').txt'), collapse='')
fpos =  paste('../results/neutral_cut/', pname, sep='/')
fneg = paste('../results/neutral_cut/', negname, sep='/')
fneu = paste('../results/neutral_cut/', neuname, sep='/')
write.table(new_pos, file = fpos, sep = ' ',  col.names = FALSE, quote = FALSE, row.names = FALSE)
write.table(new_neg, file = fneg, sep = ' ',  col.names = FALSE, quote = FALSE, row.names = FALSE)
write.table(new_neu, file = fneu, sep = ' ',  col.names = FALSE, quote = FALSE, row.names = FALSE)
