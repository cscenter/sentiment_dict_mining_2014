#coding: utf-8
import sys


def get_variants(line):
    res = list()
    variant = ""
    expr = False
    for ch in line:
        if ch == "|" and not expr:
            res.append(variant)
            variant = ""
            continue
        if ch == "(":
            expr = True
        if ch == ")":
            expr = False
        variant += ch
    res.append(variant)
    return res


def is_end(str):
	for symbol in [".", "!", "?", "!!!", "..."]:
		if str.count(symbol):
			return True
	return False


def parse(s):
    res = list()
    s = s.split("{")
    if len(s) < 2:
        res.append(s[0])
        print(s[0])
        return res
    s = s[1].split("}")[0]
    for s in get_variants(s):
        if s.count("=") != 2:
            continue
        word, POS, info = s.split("=")
        for form in get_variants(info.split("(")[0].split(")")[0]):
            res.append((word, POS, form))
    return res


if len(sys.argv) < 3:
    print("File names are required")
    exit(0)

TextFile = open(sys.argv[2], "w", encoding = "utf-8")
inFile = open(sys.argv[1], "r", encoding = "utf-8")


def print_result(word, result):
    for item in result:
        print(word, item)
        TextFile.write(word + " " + item[0] + " " + item[1] + "\n")


def find_related(pos, info, polarity):
	result = set()
	j = pos
    
	print(pos)
	while j + 2 < n:
		print(annotations[j], annotations[j + 1], annotations[j + 2])
		if j + 3 < n and annotations[j + 1].count(Comma) and annotations[j + 2].count(But):
			#j += 3
			print(", но")
			res_list = get_adjective(j + 3)
			for res in res_list:
				new_word, new_pol, new_info, new_pos = res
				if new_info == info:
					result.add((new_word, repr(-new_pol * polarity)))
				j = new_pos
		elif j + 3 < n and annotations[j + 1].count(Comma) and annotations[j + 2].count(And):
			#j += 3
			print(", и")
			res_list = get_adjective(j + 3)
			for res in res_list:
				new_word, new_pol, new_info, new_pos = res
				if new_info == info:
					result.add((new_word, repr(new_pol * polarity)))
				j = new_pos
		elif annotations[j + 1].count(But):
			#j += 2
			print(" но")
			res_list = get_adjective(j + 2)
			for res in res_list:
				new_word, new_pol, new_info, new_pos = res
				if new_info == info:
					result.add((new_word, repr(-new_pol * polarity)))
				j = new_pos
		elif j + 2 < n and annotations[j + 1].count(And):
			#j += 2
			print(", | и")
			res_list = get_adjective(j + 2)
			for res in res_list:
				new_word, new_pol, new_info, new_pos = res
				if new_info == info:
					result.add((new_word, repr(new_pol * polarity)))
				j = new_pos

		elif j + 2 < n and annotations[j + 1].count(Comma):
			print(annotations[j], annotations[j + 1], annotations[j + 2])
			#j += 1
			print("_")
			res_list = get_adjective(j + 2)
			for res in res_list:
				new_word, new_pol, new_info, new_pos = res
				#TextFile.write(new_pol)
				#TextFile.write(polarity)
				print(info, new_info)
				if new_info == info:
					result.add((new_word, repr(new_pol * polarity)))
				j = new_pos
		else: 
			print(annotations[j], annotations[j + 1], annotations[j + 2])
			#j += 1
			print("_")
			res_list = get_adjective(j + 1)
			if not res_list:
				j += 1
			for res in res_list:
				new_word, new_pol, new_info, new_pos = res
				#TextFile.write(new_pol)
				#TextFile.write(polarity)
				if new_info == info:
					result.add((new_word, repr(new_pol * polarity)))
				if j != new_pos
					j = new_pos
				else:
					j += 1
	return result

	
def is_negation(pos):
	if pos < 0 or pos >= n:
		return 0

	return 1 if len(set(annotations[pos]).intersection(Negations)) > 0 else 0


def is_adverb(pos):
	if pos < 0 or pos >= n:
		return False

	return True if len(set(annotations[pos]).intersection(set(Adverbs))) > 0 else False


def get_adjective(pos):
	res = list()
	if pos < 0 or pos >= n:
		return res

	while is_adverb(pos):
		#polarity *= is_adverb(pos)
		pos += 1

	polarity = 1 - 2 * is_negation(pos)
	if polarity == -1:
		pos += 1

	while is_adverb(pos):
		#polarity *= is_adverb(pos)
		pos += 1
		                
	if pos >= n:
		return res

	#polarity = 1
	
	for annotation in annotations[pos]:
			if len(annotation) != 3:
				continue
			word, POS, info = annotation
			if POS == "a":
				 res.append((word, polarity, info, pos))	

	return res


Comma = (",") #запятая
And = ("и", "conj", "") #и
But = ("но", "conj", "") #но

Negations = set(("не","part", ""))
Adverbs = [("очень", "adv", ""), ("совсем", "adv", ""), ("слишком", "adv", ""), ("вполне", "adv", ""), ("идеально", "adv", "")]

str = "start"
while len(str) > 0:
	line = list()

	while True:
		str = inFile.readline()
		if not len(str) or is_end(str):
			break
		line.append(str[ : -1].replace("_", ""))

	line = [x.replace("_", "") for x in line]
	
	annotations = [parse(x.lower()) for x in line if len(x) > 0]
	annotations = [x for x in annotations if len(x) > 0]

	#print(annotations)
	n = len(annotations)

	for i in range(n):
		#for annotation in annotations[i]:
		#	if len(annotation) != 3:
		#		continue
		#	word, POS, info = annotation
		#	if POS == "a":
		res_list = get_adjective(i)
		for res in res_list:		
			word, polarity, info, pos = res
			print_result(word, find_related(pos, info, polarity))