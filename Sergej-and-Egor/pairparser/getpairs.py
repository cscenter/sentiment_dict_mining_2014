__author__ = 'Egor Gorbunov'

import sys


def get_part_of_speech(string):
    d = {'SPRO': 'pronoun', 'PR': 'pretext', 'ADV': 'adverb', 'S': 'noun', 'V': 'verb', 'A': 'adjective'}
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
    spl_str = string.split('=')
    x = string.count("=A=")
    y = string.count("|") + 1
    if x == y:
        return spl_str[0]

    #if len(spl_str) > 1 and spl_str[1] == 'A':
    #    return spl_str[0]

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

    if spl_str[0] in ['и', ',']:
        return 1

    if spl_str[0] in ['a', 'но', 'зато'] or 'хотя=PART=' in string:
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
    spl_str = list(filter(''.__ne__, spl_str))
    if len(spl_str) > 0:
        if spl_str[0].count('.') or spl_str[0].count('!') or spl_str[0].count('?') \
                or spl_str[0].count(';') or spl_str[0] == "\\n\n":
            return True

    return False


def get_gender(string):
    # works for adjectives only
    # gender == 1 for masculine 2 for feminine 3 for neuter

    spl_str = (string.strip('\n ')).split("|")

    adj_info = spl_str[0].split(",")

    if adj_info[len(adj_info) - 1] == "муж":
        return 1
    elif adj_info[len(adj_info) - 1] == "жен":
        return 2
    elif adj_info[len(adj_info) - 1] == "сред":
        return 3

    return -1


class PairParser:
    pairs_dict = {}  # dictionary of dictionaries for pairs of adjectives
    pairs_no_neg = {}
    pairs_neg = {}

    def add_pair(self, dict_to_add, adj1, adj2, polarity):
        """Adds pair of two adjectives into dictionary

     :param dict_to_add: dictionary to precess
     :param adj1: adjective 1
     :param adj2: adjective 2
     :param polarity: = 1 if adjectives conjunct positively
                      = -1 if adj. conjunct negatively
     """

        if adj1 in dict_to_add and adj2 in dict_to_add[adj1]:
            dict_to_add[adj1][adj2] += polarity
        elif adj2 in dict_to_add and adj1 in dict_to_add[adj2]:
            dict_to_add[adj2][adj1] += polarity
        elif adj1 in dict_to_add:
            dict_to_add[adj1][adj2] = polarity
        elif adj2 in dict_to_add:
            dict_to_add[adj2][adj1] = polarity
        else:
            dict_to_add[adj1] = {}
            dict_to_add[adj1][adj2] = polarity

    def print_dict(self, dict_to_print, filename):
        """Prints pairs_dict into file with given name - filename
     every pair in dictionary is printed in separate line
     %(polarity of pair relation) * frequency% %first adjective% %second adjective%

     :param filename:  name of the file to print in
     """
        f = open(filename, 'w')
        for a1 in dict_to_print.keys():
            for a2 in dict_to_print[a1].keys():
                f.write(' '.join([str(dict_to_print[a1][a2]), a1, a2, '\n']))
                # print(dict_to_print[a1][a2])

        f.close()

    def print_pairs_neg(self, filename):
        self.print_dict(self.pairs_neg, filename)

    def print_pairs_no_neg(self, filename):
        self.print_dict(self.pairs_no_neg, filename)

    def read_next_adjective(self, file):
        """Input - file, which was processed by mystem.
     Function search for adjective in text file

     :rtype : big tuple
     :return: (adjective,
               -1 if negative particle was found near adjective 1 if not,
               line index,
               number of verbs before adjective,
               number of nouns before adjective,
               polarity of nearest to adjective conjunction
               gender - ajective gender
               )
     """
        adj_info = {'adj': "", 'verb_count': 0, 'noun_count': 0, 'neg': 1, 'dist': -1, 'gender': -1}
        neg_index = -1  # index (from current file pos) of negative particle (such as 'не')
        i = -1
        while True:
            i += 1
            my_str = file.readline()
            if not my_str:
                break

            part = get_part_of_speech(my_str)
            if is_end_of_sentence(my_str):
                adj_info['neg'] = 1
                i += 1000  # just a big distance
            elif is_neg_part(my_str):
                neg_index = i
            elif part == 'verb':
                adj_info['verb_count'] += 1
            elif part == 'noun':
                adj_info['noun_count'] += 1
            elif part in ['adverb', 'pretext', 'pronoun'] or is_separator(my_str):
                if i - neg_index == 1 and neg_index != -1:
                    neg_index += 1
            else:
                adj_info['adj'] = get_adjective(my_str)
                if adj_info['adj'] != "":
                    adj_info['gender'] = get_gender(my_str)
                    break

        if i - neg_index == 1 and neg_index != -1:
            adj_info['neg'] = -1
        adj_info['dist'] = i

        return adj_info

    def read_conjunction(self, file):
        """
     :param file: mystemmed file to read from
     :return:
     """

        conj_info = {'verb_count': 0, 'noun_count': 0, 'dist': 0, 'adj': "", 'gender': -1, 'polarity': 1, 'neg': 1}
        distance = 0
        neg_index = -1
        while True:
            distance += 1
            s = file.readline()
            if not s:
                break

            part = get_part_of_speech(s)
            if is_end_of_sentence(s):
                distance += 1000  # just a big distance
                break
            elif is_neg_part(s):
                neg_index = distance
            elif part == 'verb':
                conj_info['verb_count'] += 1
            elif part == 'noun':
                conj_info['noun_count'] += 1
            elif part in ['adverb', 'pretext', 'pronoun'] or is_separator(s):
                if neg_index != -1:
                    neg_index += 1

            conj_info['adj'] = get_adjective(s)
            if conj_info['adj'] != "":
                conj_info['gender'] = get_gender(s)
                if distance - neg_index == 1 and neg_index != -1:
                    conj_info['neg'] = -1
                break

            p = get_conjunction_polarity(s)
            if p != 0:
                conj_info['polarity'] = p
            if p < 0:
                break

        conj_info['dist'] = distance
        return conj_info

    def get_pairs(self, in_filename):
        """that function parse file and
     get pairs of adjectives with polarity

     :param in_filename: file, preprocessed with mystem with "-icln" options
     """
        # opening mystemmed file to parse
        try:
            f = open(in_filename, 'r')
        except IOError:
            print('cannot open file ' + in_filename)

        adj1_info = {'adj': ""}

        while True:
            #getting first adjective
            if adj1_info['adj'] == "":
                adj1_info = self.read_next_adjective(f)

            # trying to find conjunction and maybe second adjective if they adjectives go without negative conjunction
            # (between them can be space, comma, "и")
            conj_info = self.read_conjunction(f)

            # getting next adjective (second adjective) if it was not found in previous step
            if conj_info['adj'] == "":
                adj2_info = self.read_next_adjective(f)
            else:
                adj2_info = {'adj': conj_info['adj'],
                             'verb_count': 0,
                             'noun_count': 0,
                             'neg': conj_info['neg'],
                             'dist': 0,
                             'gender': conj_info['gender']}

            if adj1_info['adj'] == "" or adj2_info['adj'] == "":
                break

            # here we have 2 adjectives, which go successive, but the distance between them can be big.
            # I think, that only number of verbs and nouns matter, and there can only be 2 nouns and verbs btw.
            # adjectives ('Прекрасное времяпрепровождение - гулять по пляжу, но песок слишком твердый')
            # adverbs, pronouns, pretext does not matter too. ('Плохое питание, зато, по-моему, очень хороший номер')
            if adj2_info['verb_count'] + conj_info['verb_count'] == 0 \
                    and adj2_info['noun_count'] + conj_info['noun_count'] <= 1 \
                    and adj2_info['dist'] + conj_info['dist'] <= 7 \
                    and adj1_info['gender'] == adj2_info['gender'] \
                    and adj1_info != -1:
                na1 = ""
                na2 = ""
                if adj1_info['neg'] == -1:
                    na1 = "не"
                if adj2_info['neg'] == -1:
                    na2 = "не"
                self.add_pair(self.pairs_dict, ' '.join([na1, adj1_info['adj']]).strip(),
                              # strip is used to delete first space
                              ' '.join([na2, adj2_info['adj']]).strip(),
                              conj_info['polarity'])

                self.add_pair(self.pairs_neg, ''.join([na1, adj1_info['adj']]),
                              ''.join([na2, adj2_info['adj']]), conj_info['polarity'])

                self.add_pair(self.pairs_no_neg, adj1_info['adj'], adj2_info['adj'],
                              adj2_info['neg'] * adj1_info['neg'] * conj_info['polarity'])

            adj1_info = adj2_info

        f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write('ERROR: Bad arguments')
        sys.exit(1)

    pparser = PairParser()
    pparser.get_pairs(sys.argv[1])

    name1 = 'out_pairs_no_neg/' + sys.argv[1].split('.')[0] + '_noneg.txt'
    name2 = 'out_pairs_neg/' + sys.argv[1].split('.')[0] + '_neg.txt'
    pparser.print_pairs_neg(name1)
    pparser.print_pairs_no_neg(name2)