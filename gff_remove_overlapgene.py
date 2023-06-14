#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/5/23 3:25 PM
    @Usage: python3 remove_overlapgene.py raw.gff > new.gff
"""
import sys

gene_regions = (0, 0)
lines_block = ''
record_flag = 1

with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            continue
        else:
            temp = line.rstrip().split('\t')
            if temp[2] == 'gene':
                if lines_block != '':
                    if int(temp[3]) > gene_regions[1] or \
                    int(temp[4]) < gene_regions[0]:
                        print(lines_block.rstrip())
                        lines_block = ''
                        record_flag = 1
                    else:
                        if gene_regions[1] - gene_regions[0] >= int(temp[4]) - int(temp[3]):
                            record_flag = 0
                        else:
                            record_flag = 1
                            lines_block = ''
                gene_regions = (int(temp[3]), int(temp[4]))
            if record_flag == 1:
                lines_block += line
    # final
    if lines_block != '':
        print(lines_block.rstrip())






