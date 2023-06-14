#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/6/10 10:45 AM
    @Usage: python3 gff_remove_gene_without_mRNA.py raw.gff > new.gff
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

gene_mrna_dict = dict()
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            #print(line.rstrip())
            continue
        else:
            temp = line.rstrip().split('\t')
            attr = string2dict(temp[8])
            if temp[2] == 'gene':
                gene_mrna_dict[attr['ID']] = dict()
            elif temp[2] in ['mRNA', 'tRNA', 'transcript']:
                gene_mrna_dict[attr['Parent']][attr['ID']] = ''

with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
            continue
        else:
            temp = line.rstrip().split('\t')
            attr = string2dict(temp[8])
            if temp[2] == 'gene':
                if len(gene_mrna_dict[attr['ID']]) == 0:
                    continue
                else:
                    print(line.rstrip())
            else:
                print(line.rstrip())
