#!/usr/bin/env python ud3k_bed.py in.gff > out.bed(1-based)
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2022/8/18 9:45 PM
    @Usage:
"""
import sys

ws = 3000
with open(sys.argv[1]) as f:
    for line in f:
        temp = line.rstrip().split('\t')
        if temp[2] == 'gene':
            strand = temp[6]
            start = int(temp[3])
            end = int(temp[4])
            chrn = temp[0]
            geneid = temp[8].split(';')[0].split('=')[1]
            if strand == '+':
                us = max(1, start - ws)
                print('\t'.join([str(x) for x in [chrn, us, start - 1, geneid + '.u3k']]))
                de = end + ws
                print('\t'.join([str(x) for x in [chrn, end + 1, de, geneid + '.d3k']]))
            else:
                de = max(1, start - ws)
                print('\t'.join([str(x) for x in [chrn, de, start - 1, geneid + '.d3k']]))
                us = end + ws
                print('\t'.join([str(x) for x in [chrn, end + 1, us, geneid + '.u3k']]))
