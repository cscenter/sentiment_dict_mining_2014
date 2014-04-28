spl = strsplit(getwd(), '/')
nwd = paste(spl[[1]][1:length(spl[[1]]) - 1], collapse = '/')
nwd = paste(nwd, "pairparser/results", sep = "/")

#n2 and en2 - pairs, where "," is not a separator
#n3 and en3 - pairs, where "," is a positive separator
#n - pairs, where prefix "не" exists
#en - no "не" prefix

l <- list(n2 = read.table(paste(nwd, "all_pairs_no_neg(2).txt", sep = "/"), skip = 1, stringsAsFactors=FALSE),
          en2 = read.table(paste(nwd, "en_pairs_no_neg(2).txt", sep = "/"), skip = 1, stringsAsFactors=FALSE),
          n4 = read.table(paste(nwd, "pairs_no_neg(4).txt", sep = "/"), skip = 1, stringsAsFactors=FALSE),
          en4 = read.table(paste(nwd, "en_pairs(4).txt", sep = "/"), skip = 1, stringsAsFactors=FALSE))
for (i in (1:length(l))) {
  colnames(l[[i]]) <- c("pos", "neg", "a1", "a2")
}

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

#degree of node "хороший"
for (i in (1:length(l))) {
  print(get_degree("хороший", l[[i]]))
}

#degree of node "плохой"
for (i in (1:length(l))) {
  print(get_degree("плохой", l[[i]]))
}

dict_list = list()
#dictionaries
for (i in (1:length(l))) {
  dict_list[i] = list(unique(append(unique(l[[i]][['a1']]), unique(l[[i]][['a2']]))))
  print(length(dict_list[[i]]))
}

degrees_list = list()
for (i in (1:length(l))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_degree(w, l[[i]])
  }
  degrees_list[i] = list(cur_deg)
}

pos_deg_list = list()
for (i in (1:length(l))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_sum_pos_deg(w, l[[i]])
  }
  pos_deg_list[i] = list(cur_deg)
}

neg_deg_list = list()
for (i in (1:length(l))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_sum_neg_deg(w, l[[i]])
  }
  neg_deg_list[i] = list(cur_deg)
}

#histograms for degrees
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  hist(degrees_list[[i]], breaks=100, main = names(l)[i], xlab = "nodes degrees")
}

min = 30
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  h <- hist(degrees_list[[i]][c(which(degrees_list[[i]] > min))], breaks=100, main = names(l)[i], 
       xlab = paste("nodes degrees >", as.character(min)))
}

# edges with a big mass
min_abs_big_mass = 100
big_mass_list = list()
for (i in (1:length(l))) {
  big_mass_list[i] = list(l[[i]][ l[[i]]$neg < -min_abs_big_mass | l[[i]]$pos > min_abs_big_mass, ])
  big_mass_list[i] = list(big_mass_list[[i]][order(big_mass_list[[i]]$pos, decreasing=TRUE), ])
  print(big_mass_list[[i]])
  print("---------------------------------------------------------------")
}

# ratio btw absolute values of pos and neg
ratios_list = list()
for (i in (1:length(l))) {
  cur_rat = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_rat [j] = get_pos_val(w, l[[i]]) / get_neg_val(w, l[[i]])
  }
  ratios_list[i] = list(cur_rat)
}

#not inf. ratios
max = Inf
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  h <- hist(ratios_list[[i]][c(which(ratios_list[[i]] < max))], breaks=130, main = names(l)[i], 
            xlab = paste("pos/neg ratio <", as.character(max)))
}

#degree on pos degree
max = Inf
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  plot(degrees_list[[i]], pos_deg_list[[i]], main = names(l)[i], xlab = "full degree", ylab= "positive sum degree")
}

#degree on neg degree
max = Inf
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  plot(degrees_list[[i]], neg_deg_list[[i]], main = names(l)[i], xlab = "full degree", ylab= "negative sum degree")
}

#pos on neg degree
max = Inf
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  fit <- glm(neg_deg_list[[i]] ~ pos_deg_list[[i]])
  b <- fit$coefficients[1]
  a <- fit$coefficients[2]
  plot(pos_deg_list[[i]], neg_deg_list[[i]], main = names(l)[i], xlab = "pos degree", ylab= "negative sum degree",
       ylim = c(0, 300),
       xlim = c(0, 450))
  sq <- seq(0, max(pos_deg_list[[i]] + 30), 30)
  lines(sq, a * sq + b, col = 'red')
}

#normalizing weights
nl = l

for (i in (1:length(nl))) {
  max = max(l[[i]]$pos)
  amin = -min(l[[i]]$neg)
  nl[[i]]$neg = nl[[i]]$neg / amin
  nl[[i]]$pos = nl[[i]]$pos / max
}

ndeg_list = list()
for (i in (1:length(nl))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_degree(w, nl[[i]])
  }
  ndeg_list[i] = list(cur_deg)
}

npos_deg_list = list()
for (i in (1:length(nl))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_sum_pos_deg(w, nl[[i]])
  }
  npos_deg_list[i] = list(cur_deg)
}

nneg_deg_list = list()
for (i in (1:length(nl))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_sum_neg_deg(w, nl[[i]])
  }
  nneg_deg_list[i] = list(cur_deg)
}

#pos on neg degree for normalized weights
max = Inf
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  fit <- glm(nneg_deg_list[[i]] ~ npos_deg_list[[i]])
  b <- fit$coefficients[1]
  a <- fit$coefficients[2]
  plot(npos_deg_list[[i]], nneg_deg_list[[i]], main = names(l)[i], xlab = "pos degree", ylab= "negative sum degree", 
       ylim = c(0, 300),
       xlim = c(0, 450))
  sq <- seq(0, max(npos_deg_list[[i]] + 30), 30)
  lines(sq, a * sq + b, col = 'red')
}

#increasing neg weights by 50
nli = l
for (i in (1:length(nli))) {
  nli[[i]]$neg = nli[[i]]$neg * 50
}

nipos_deg_list = list()
for (i in (1:length(nli))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_sum_pos_deg(w, nli[[i]])
  }
  nipos_deg_list[i] = list(cur_deg)
}

nineg_deg_list = list()
for (i in (1:length(nl))) {
  cur_deg = rep(0, length(dict_list[[i]]))
  for (j in (1:length(dict_list[[i]]))) {
    w = dict_list[[i]][j]
    cur_deg[j] = get_sum_neg_deg(w, nli[[i]])
  }
  nineg_deg_list[i] = list(cur_deg)
}

#pos on neg degree for multiplied neg weights
max = Inf
par(mfrow = c(2, 2))
for (i in (1:length(l))) {
  fit <- glm(nineg_deg_list[[i]] ~ nipos_deg_list[[i]])
  b <- fit$coefficients[1]
  a <- fit$coefficients[2]
  plot(nipos_deg_list[[i]], nineg_deg_list[[i]], main = names(l)[i], xlab = "pos degree", ylab= "negative sum degree",
       ylim = c(0, 300),
       xlim = c(0, 450))
  sq <- seq(0, max(npos_deg_list[[i]] + 30), 30)
  lines(sq, a * sq + b, col = 'red')
}


fit1 <- glm(neg_deg_list[[4]] ~ pos_deg_list[[4]])
b <- fit1$coefficients[1]
a <- fit1$coefficients[2]
plot(pos_deg_list[[4]], neg_deg_list[[4]], col = 'green', xlab = "pos degree", ylab= "negative sum degree",
      ylim = c(0, 300),
      xlim = c(0, 450))
legend('topleft', c('|p| - |n| metric', '|p| - |n|*50 metric', '|p|/max(pos) - |n|/max(|neg|) metric'), 
       lty=1, col=c('green', 'blue', 'red'), bty='n', cex=.75)
sq <- seq(0, max(pos_deg_list[[i]] + 30), 30)
lines(sq, a * sq + b, col = 'green', lwd=2)
fit2 <- glm(nneg_deg_list[[4]] ~ npos_deg_list[[4]])
b <- fit2$coefficients[1]
a <- fit2$coefficients[2]
lines(npos_deg_list[[4]], nneg_deg_list[[4]], col = 'blue', xlab = "pos degree", ylab= "negative sum degree",
      ylim = c(0, 300),
      xlim = c(0, 450), type = 'p')
sq <- seq(0, max(npos_deg_list[[i]] + 30), 30)
lines(sq, a * sq + b, col = 'blue', lwd=2)
fit3 <- glm(nineg_deg_list[[4]] ~ nipos_deg_list[[4]])
b <- fit3$coefficients[1]
a <- fit3$coefficients[2]
lines(nipos_deg_list[[4]], nineg_deg_list[[4]], col = 'red', xlab = "pos degree", ylab= "negative sum degree",
     ylim = c(0, 300),
     xlim = c(0, 450), type = 'p')
sq <- seq(0, max(npos_deg_list[[i]] + 30), 30)
lines(sq, a * sq + b, col = 'red', lwd=2)