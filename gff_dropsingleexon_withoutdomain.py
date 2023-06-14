#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/5/20 8:49 PM
    @Usage: python3 gff_dropsingleexon_withoutdomain.py raw.gff  > new.gff
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

temp_gene_record = ''

gene_print = dict()
pass_flag = 1

with open(gff) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
        temp = line.rstrip().split('\t')
        if temp[2] == 'gene':
            temp_gene_record = line.rstrip()
        elif temp[2] == 'mRNA':
            attr = string2dict(temp[8])
            mrna = attr['ID']
            gene = attr['Parent']
            exonn = attr['Exon_num']
            if exonn != '1' or 'Function' in attr:
                if gene not in gene_print:
                    print(temp_gene_record)
                    gene_print[gene] = 1
                print(line.rstrip())
                pass_flag = 1
            else:
                pass_flag = 0
        else:
            if pass_flag:
                print(line.rstrip())

