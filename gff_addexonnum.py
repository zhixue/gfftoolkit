#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/5/20 7:05 PM
    @Usage: python3 gff_addexonnum.py raw.gff gff.stat.txt > new.gff
"""
import sys

def string2dict(long_string, sep=';', eq='=', rm_quote=False):
    if rm_quote:
        long_string = long_string.replace('"', '').replace("'", '')
    long_string = long_string.replace('; ', ';')
    out_dict = dict()
    tmp = long_string.rstrip(sep).split(sep)
    for i in tmp:
        if len(i.split(eq)) == 2:
            key, value = i.split(eq)
        else:
            key = i.split(eq)[0]
            value = eq.join(i.split(eq)[1:])
        out_dict[key] = value
    return out_dict


gff=sys.argv[1]
tsv=sys.argv[2]

exon_d = dict()
with open(tsv) as f:
    for line in f:
        temp = line.rstrip().split('\t')
        mrna = temp[1]
        exon_d[mrna] = temp[5]


with open(gff) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
            continue
        temp = line.rstrip().split('\t')
        if temp[2] != 'mRNA':
            print(line.rstrip())
        else:
            mrnaid = string2dict(temp[8])['ID']
            if mrnaid in exon_d:
                print(line.rstrip() + 'exon_num=' + exon_d[mrnaid] + ';')
