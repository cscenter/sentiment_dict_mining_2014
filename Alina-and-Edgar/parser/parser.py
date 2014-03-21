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

def parse(s):
    res = list()
    s = s.split("{")
    if len(s) < 2:
        res.append(s[0])
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

line = inFile.read().split("\n")
line = [x.replace("_", "") for x in line]
annotations = [parse(x.lower()) for x in line if len(x) > 0]
annotations = [x for x in annotations if len(x) > 0]
    
def print_result(word, res):
    for item in res:
        print(word, item)
        TextFile.write(str(word) + " " + item[0] + " " + item[1] + "\n")

Comma = (",") #запятая
And = ("\u0438", "conj", "") #и
But = ("\u043D\u043E", "conj", "") #но

def find_related(pos, info):
    res = set()
    j = pos
    while j + 2 < n:
        if annotations[j + 1].count(Comma) > 0 or annotations[j + 1].count(And) > 0:
            j += 2
            for candidate in annotations[j]:
                if len(candidate) < 3:
                    continue
                if candidate[1] == "a" and candidate[2] == info:
                    res.add((candidate[0], "1"))
        elif annotations[j + 1].count(But) > 0:
            j += 2
            for candidate in annotations[j]:
                if len(candidate) < 3:
                    continue
                if candidate[1] == "a" and candidate[2] == info:
                    res.add((candidate[0], "-1"))
        else:
            break
    return res

n = len(annotations)

for i in range(n):
    for annotation in annotations[i]:
        if len(annotation) != 3:
            continue
        word, POS, info = annotation
        if POS == "a":
            print_result(word, find_related(i, info))