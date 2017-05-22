#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Created on Sat May 20 14:08:33 2017

@author: Chang-Eop

pubmed_fething_chunk.py의 fecting 결과인 
results_2:'Bio.Entrez.Parser.DictionaryElement'들의 list)를 txt파일로 저장
title과 abstract로 저장되며 띄어쓰는 줄 수로 구분됨. 
"""


import codecs

no_papers = len(results_2)

f = codecs.open('pain_papers.txt','w',"utf-8")

for i in range(no_papers):
    print(i+1, " of", no_papers)
    f.write('\n\n\n\n')
    
    data_0 = results_2[i]
    data_1 = data_0['MedlineCitation']
    data_2 = data_1['Article']
    Title = data_2['ArticleTitle']
    f.write(Title[:])
    f.write('\n\n')

    if 'Abstract' in list(data_2.keys()):
        Abstract = data_2['Abstract']['AbstractText'][0]   
        f.write(Abstract[:])
        
    else:
        print('!!!!!!!!!!!!!!!!!! no ABSTACT!!!!!!!!!') #초록 없는 경우
        
f.close()
        
             

