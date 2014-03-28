# -*- coding: cp1251- -*-
__author__ = 'Egor Gorbunov'

import sys

pairs_dict = {} #dictionary of dictionaries for pairs of adjectives

def add_pair(adj1, adj2, polarity):
    """Adds pair of two adjectives into dictionary

    :param adj1: adjective 1
    :param adj2: adjective 2
    :param polarity: = 1 if adjectives conjunct positively
                     = -1 if adj. conjunct negatively
    """

    global pairs_dict
    if adj1 in pairs_dict:
        if adj2 in pairs_dict[adj1]:
            pairs_dict[adj1][adj2] += polarity
        else:
            pairs_dict[adj1][adj2] = polarity
    elif adj2 in pairs_dict:
        if adj1 in pairs_dict[adj2]:
            pairs_dict[adj2][adj1] += polarity
        else:
            pairs_dict[adj2][adj1] = polarity
    else:
        pairs_dict[adj1] = {}
        pairs_dict[adj1][adj2] = polarity

def print_dict(filename):
    """Prints pairs_dict into file with given name - filename
    every pair in dictionary is printed in separate line
    %(polarity of pair relation) * frequency% %first adjective% %second adjective%

    :param filename:  name of the file to print in
    """
    global  pairs_dict
    f = open(filename, 'w')
    for a1 in pairs_dict.keys():
        for a2 in pairs_dict[a1].keys():
            f.write(' '.join([str(pairs_dict[a1][a2]), a1, a2, '\n']))
            #print(pairs_dict[a1][a2])

def get_part_of_speech(string):
    d = {'SPRO': 'pronoun', 'PR': 'pretext', 'ADV': 'adverb', 'S': 'noun', 'V': 'verb'}
    spl_str = string.split('=')
    if len(spl_str) > 1 and spl_str[1] in d:
        return d[spl_str[1]]
    else:
        return ''

def get_adjective(string):
    """Checks, if given string stands for adjective

    :param string: line from file, which was processed by mystem.
    :return: if string conforms to pattern: "%word%=A=|..." it return adjective (%word%),
             if string does not, function returns empty str. ("")
    """
    x = string.count("=A=")
    y = string.count("|") + 1
    spl_str = string.split('=')
    if x == y:
        return spl_str[0]
    return ""

def is_neg_part(string):
    """Checks, if given string stands for negative particle

    :param string: line from file, which was processed by mystem.
    :return: if string conforms to pattern: "%word%=PART=|..." and %word% is negative particle func. return True
             if not, function return False
    """
    spl_str = string.split('=')
    if len(spl_str) >= 2:
        if spl_str[0] == 'не':
            return True
    return False

def get_conjunction_polarity(string):
    """
    If string describes conjunction, function return it's polarity
    :param string:
    :return:
    """

    spl_str = string.split('=')

    if spl_str[0] in ['и']:
        return 1

    if spl_str[0] in ['a', 'но', 'зато']:
        return -1

    return 0

def is_separator(string):
    spl_str = string.split('=')
    if len(spl_str) == 1:
        return True
    else:
        return False

def is_end_of_sentence(string):
    spl_str = string.split('_')
    spl_str = list(filter(('').__ne__, spl_str))
    if len(spl_str) > 0:
        if spl_str[0].count('.') or spl_str[0].count('!') or spl_str[0].count('?')\
            or spl_str[0].count(';') or spl_str[0] == "\\n\n":
            return True

    return False

def read_next_adjective(file):
    """Input - file, which was processed by mystem.
    Function search for adjective in text file

    :rtype : big tuple
    :return: (adjective,
              -1 if negative particle was found near adjective 1 if not,
              line index,
              number of verbs before adjective,
              number of nouns before adjective,
              polarity of nearest to adjective conjunction
              )
    """
    neg_factor = 1
    neg_index = -1 #index (from current file pos) of negative particle (such as 'не')
    i = -1
    adj = ""
    verb_count = 0
    noun_count = 0
    while True:
        i += 1
        my_str = file.readline()
        if not my_str:
            break

        part = get_part_of_speech(my_str)
        if is_end_of_sentence(my_str):
            neg_factor = 0
            i += 1000 #just a big distance
        elif is_neg_part(my_str):
            neg_index = i
        elif part == 'verb':
            verb_count += 1
        elif part == 'noun':
            noun_count += 1
        elif part in ['adverb', 'pretext', 'pronoun'] or is_separator(my_str):
            if i - neg_index  == 1 and neg_index != -1:
                neg_index += 1
        else:
            adj = get_adjective(my_str)
            if adj != "":
                break

    if i - neg_index  == 1 and neg_index != -1:
        neg_factor = -1

    return adj, neg_factor, i, verb_count, noun_count

def read_conjunction(file):
    """
    :param file: mystemmed file to read from
    :return:
    """
    verb_count = 0
    noun_count = 0
    polarity = 1
    distance = 0
    adjective = ""
    neg_index = -1
    neg_factor = 1
    while True:
        distance += 1
        s = file.readline()
        if not s:
            break

        part = get_part_of_speech(s)
        if is_end_of_sentence(s):
            polarity = 0
            distance += 1000 #just a big distance
            break
        elif is_neg_part(s):
            neg_index = distance
        elif part == 'verb':
            verb_count += 1
        elif part == 'noun':
            noun_count += 1
        elif part in ['adverb', 'pretext', 'pronoun'] or is_separator(s):
            if distance - neg_index  == 1 and neg_index != -1:
                neg_index += 1

        adjective = get_adjective(s)
        if adjective != "":
            if distance - neg_index  == 1 and neg_index != -1:
                neg_factor = -1
            break

        p = get_conjunction_polarity(s)
        if p != 0:
            polarity = p
        if p < 0:
            break

    return polarity, distance, verb_count, noun_count, adjective, neg_factor

def analyze_file(in_filename, out_filename):
    """that function parse file and
    get pairs of adjectives with polarity

    :param in_filename: file, preprocessed with mystem with "-icln" options
    :param out_filename: output file with pairs
    """
    #opening mystem'ed file to parse
    try:
        f = open(in_filename, 'r')
    except IOError:
        print('cannot open file ' + in_filename)

    neg_factor_1 = 1 #negative factor for first adjective
    neg_factor_2 = 1
    adj1 = "" #first adjective
    adj2 = "" #second adjective
    adj2_distance = 0 #distance between 2-nd adjective and conjunction of first adjective
    while True:
        #getting first adjective
        if adj1 == "":
            adj1, neg_factor_1, pos1, verb_count1, noun_count1  = read_next_adjective(f)

        if neg_factor_1 == 0:
            adj1 = ""
            adj2 = ""
            continue

        #trying to find conjunction and maybe second adjective if they adjectives go without negative conjunction
        # (between them can be space, comma, "и")
        polarity, conj_distance, verb_count2, noun_count2, adj2, neg_factor_2 = read_conjunction(f)
        if polarity == 0:
            adj1 = ""
            adj2 = ""
            continue

        verb_count3 = 0
        noun_count3 = 0

        #getting next adjective (second adjective) if it was not found in previous step
        if adj2 == "":
            adj2, neg_factor_2, adj2_distance, verb_count3, noun_count3 = read_next_adjective(f)

        if adj1 == "" or adj2 == "":
            break

        #here we have 2 adjectives, which go successive, but the distance between them can be big
        #I think, that only number of verbs and nouns matter, and there can only be 2 nouns and verbs btw.
        #adjectives ('Прекрасное времяпрепровождение - гулять по пляжу, но песок слишком твердый')
        #adverbs, pronouns, pretext does't matter too. ('Плохое питание, зато, по-моему, очень хороший номер')
        if verb_count2 <= 1 and noun_count2 == 0 and verb_count3 <= 1 and noun_count3 == 0\
            and conj_distance <= 5 and adj2_distance <= 5:
            a1 = adj1
            a2 = adj2
            if neg_factor_1 == -1:
                a1 = ' '.join(['не', adj1])
            if neg_factor_2 == -1:
                a2 = ' '.join(['не', adj2])
            add_pair(a1, a2, polarity)

        adj1 = adj2
        adj2 = ""
        polarity = neg_factor_2
        neg_factor_1 = neg_factor_2
        neg_factor_2 = 1

    f.close()
    print_dict(out_filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write('=(')
        sys.exit(1)
    analyze_file(sys.argv[1], sys.argv[2])
