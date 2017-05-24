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

count_abstract = 0
count_date = 0

for i in range(no_papers):
    print(i+1, " of", no_papers)
    f.write('\n\n\n\n')
    
    data_0 = results_2[i]
    data_M1 = data_0['MedlineCitation'] #제목, 초록 데이터는 MedlineCitation을 참고해야 함
    data_M2 = data_M1['Article']
    
    
    data_P1 = data_0['PubmedData'] #article date 데이터를 누락 없이 확인하기 위해서는 pubmedData를 참고해야 함
    data_P2 = data_P1['History']
    data_P3 = data_P2[1]
    
    #초록이 없는 논문은 제외. 어차피 제목이 아닌 초록을 검색할 것이므로, 제목 자리에 출판연도 기재
    if 'Abstract' in list(data_M2.keys()):
        Title = data_M2['ArticleTitle']
        Abstract = data_M2['Abstract']['AbstractText'][0]   
        Date = data_P3['Year']
        
        f.write(Date)
        f.write('\n')
        f.write(Abstract[:])
        
    else:
        print('!!!!!!!!!!!!!!!!!! no ABSTACT!!!!!!!!!') #초록 없는 경우
        
f.close()
        
             


        
    
