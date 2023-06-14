#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/6/10 10:55 AM
    @Usage: python3 gff_gene_mapName.py raw.gff map.gff > new.gff
"""
import sys


def overlap(a, b, min_overlap_len=1):
    if a[1] < b[0] + min_overlap_len or a[0] > b[1] - min_overlap_len:
        return 0
    else:
        return 1


def find_overlap(chrn, region, strand, region_gene_dict, gene_strand_dict):
    if chrn not in region_gene_dict:
        return ''
    current_loc = 0
    for rg in region_gene_dict[chrn]:
        if current_loc > region[0]:
            return ''
        if overlap(region, rg) == 0:
            current_loc = rg[1]
        else:
            if strand == gene_strand_dict[region_gene_dict[chrn][rg]]:
                return region_gene_dict[chrn][rg]


def dict2string(long_dict, sep=';', eq='='):
    long_string = ''
    for i in long_dict:
        key, value = i, long_dict[i]
        long_string += str(key) + eq + str(value) + sep
    return long_string


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


region_gene_dict = dict() #{'chr':{(1,200):'dd'}}
gene_strand_dict = dict()
with open(sys.argv[2]) as f:
    for line in f:
        if line.startswith('#'):
            #print(line.rstrip())
            continue
        else:
            temp = line.rstrip().split('\t')
            strand = temp[6]
            attr = string2dict(temp[8])
            if temp[2] == 'gene':
                if temp[0] not in region_gene_dict:
                    region_gene_dict[temp[0]] = dict()
                region_gene_dict[temp[0]][(int(temp[3]), int(temp[4]))] = attr['ID']
                gene_strand_dict[attr['ID']] = strand


novel_gene_id = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
            continue
        else:
            temp = line.rstrip().split('\t')
            strand = temp[6]
            attr = string2dict(temp[8])
            if temp[2] == 'gene':
                chrn = temp[0]
                region = (int(temp[3]), int(temp[4]))
                newname = find_overlap(chrn, region, strand, region_gene_dict, gene_strand_dict)
                if newname == '':
                    novel_gene_id += 1
                    newname = 'NovelGene' + str(novel_gene_id)
                attr['Name'] = newname
                temp[8] = dict2string(attr)
                print('\t'.join(temp))
            else:
                print(line.rstrip())
