__author__ = 'egor'

import linecache

f = open('bad_lines_numbers.txt', 'r')
out_file = open('bad_lines.txt', 'w')

filename = ''
for s in f:
    print(s)
    if len(s) > 8:
        filename = s.strip('\n ')
        linecache.clearcache()
        continue
    else:
        line_number = int(s)

    out_file.write('======================================================\n')
    for i in range(line_number - 8, line_number + 8):
        out_file.write(linecache.getline(filename, i))
    out_file.write('======================================================\n')


f.close()
out_file.close()