#!/usr/bin/env python3 gff_revcom.py raw.gff chrlen > fix.gff
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2022/10/29 11:11 AM
    @Usage:
"""
import sys

chrlen = int(sys.argv[2])

with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            continue
        temp = line.rstrip().split('\t')
        start = int(temp[3])
        end = int(temp[4])
        strand = temp[6]
        newstart = chrlen - end + 1
        newend = chrlen - start + 1
        newstrand = '+' if strand == '-' else '-'

        # update
        temp[3] = str(newstart)
        temp[4] = str(newend)
        temp[6] = newstrand
        print('\t'.join(temp))
        



