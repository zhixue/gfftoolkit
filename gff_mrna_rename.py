#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/6/13 4:02 PM
    @Usage:
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

def dict2string(long_dict, sep=';', eq='='):
    long_string = ''
    for i in long_dict:
        key, value = i, long_dict[i]
        long_string += str(key) + eq + str(value) + sep
    return long_string


gff=sys.argv[1]

mrna_replace_dict = dict()
gene_mrna_dict = dict()

# load
with open(gff) as f:
    for line in f:
        if line.startswith('#'):
            continue
        temp = line.rstrip().split('\t')
        if temp[2] == 'gene':
            attr = string2dict(temp[8])
            geneid = attr['ID']
            if geneid not in gene_mrna_dict:
                gene_mrna_dict[geneid] = dict()
        elif temp[2] == 'mRNA':
            attr = string2dict(temp[8])
            geneid = attr['Parent']
            mrnaid = attr['ID']
            if len(mrnaid.split('.')) == 2 and (geneid.startswith('Contig') or geneid.startswith('NDH')):
                gene_mrna_dict[geneid][mrnaid] = ''

with open(gff) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
        temp = line.rstrip().split('\t')
        if temp[2] == 'gene':
            print(line.rstrip())
            continue
        if temp[2] == 'mRNA':
            attr = string2dict(temp[8])
            geneid = attr['Parent']
            mrnaid = attr['ID']
            if mrnaid not in gene_mrna_dict[geneid]:
                mid = len(gene_mrna_dict[geneid]) + 1
                newmrnaid = geneid + '.' + str(mid)
                gene_mrna_dict[geneid][newmrnaid] = ''
                mrna_replace_dict[mrnaid] = newmrnaid
                attr['ID'] = newmrnaid
                temp[8] = dict2string(attr)
                print('\t'.join(temp))
            else:
                print(line.rstrip())
        else:
            attr = string2dict(temp[8])
            mrnaid = attr['Parent']
            if mrnaid in mrna_replace_dict:
                attr['Parent'] = mrna_replace_dict[mrnaid]
                attr['ID'] = attr['ID'].replace(mrnaid, mrna_replace_dict[mrnaid])
                temp[8] = dict2string(attr)
                print('\t'.join(temp))
            else:
                print(line.rstrip())



