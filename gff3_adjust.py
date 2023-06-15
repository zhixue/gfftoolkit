#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/6/15 10:10 AM
    @Usage:
"""
import sys

# adjust under mrna

dic = dict()

last_line = ''
last_loc = []
loc = []
last_tp = ''
tp = ''
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            if last_line != '':
                print(last_line)
                last_line = ''
            print(line.rstrip())
            continue
        temp = line.rstrip().split('\t')
        if temp[2] == 'gene' or temp[2] == 'mRNA':
            if last_line != '':
                print(last_line)
                last_line = ''
            print(line.rstrip())
        else:
            loc = [temp[0], temp[3], temp[4]]
            tp = temp[2]
            if last_line != '':
                if loc == last_loc:
                    if tp == 'five_prime_UTR' and temp[6] == '+':
                        print(line.rstrip())
                        continue
                    elif tp == 'three_prime_UTR' and temp[6] == '-':
                        print(line.rstrip())
                        continue
                print(last_line)

            last_line = line.rstrip()
            last_loc = loc
    # last one
    if last_line != '':
        print(last_line)