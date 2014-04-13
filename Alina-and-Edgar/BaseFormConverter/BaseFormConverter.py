__author__ = 'Edgar'

import os
import sys
import random


if (len(sys.argv) != 3):
    print("Usage: BaseFormConverter.py input_file output_file")
else:
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")

    hash = random.getrandbits(128)

    mystem_output_file = open(str(hash), "w+")
    print(str(hash))

    command = 'mystem -n -e utf-8 ' + sys.argv[1] + " " + str(hash)
    print(command)
    os.system(command)

    lines = mystem_output_file.readlines()

    for line in lines:
        temp = line.replace('{', ' ').replace('}', ' ').replace('|', ' ').replace('\n', ' ')
        output_file.write(temp.split()[-1] + "\n")

    input_file.close()
    output_file.close()
    mystem_output_file.close()
    os.remove(str(hash))

