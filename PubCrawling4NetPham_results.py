#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 00:52:50 2017

@author: Chang-Eop
"""

import os
os.chdir('/Users/Chang-Eop/Desktop/GitHub/TextMining')

import pubmed_crawler as pc

#펍메드에서 검색할 본초
term_herb = 'ginseng' 
pheno_query = 'acute migraine'

results = pc.search(term_herb)
id_list = results['IdList']
papers = pc.fetch_details(id_list)

#본초로 검색돈 문서들의 제목, 초록에서 검색할 질병.  (경로 등의 표현형도 괜찮은지 아직 확인 X)
terms_phenotypes = pc.MeSH_terms_2(pheno_query) #MeSH entry terms 리스트 구성

#terms_phenotypes 등장한 title, abstract 갯수 초기값.
N_title = 0
N_abstract = 0

for i, j in enumerate(id_list):
    print(i+1, ' of ', len(id_list))
    
    article = papers['PubmedArticle'][i]['MedlineCitation']['Article']
    Title = article['ArticleTitle']
    
    if 'Abstract' in list(article.keys()):
        Abstract = article['Abstract']['AbstractText'][0]
    else:
        print('!!!!!!!!!!!!!!!!!! no ABSTACT!!!!!!!!!') #초록 없는 경우
    
    
    k = 0
    while k < len(terms_phenotypes): #하나라도 찾았거나, 끝까지 뒤졌는데 못찾은 경우
        term_pheno = terms_phenotypes[k]
        if Title.lower().find(term_pheno) == -1:#해당 단어가 없을시 -1 반환.
            k+=1
        else:
            N_title += 1
            k = len(terms_phenotypes) #찾은 경우 while 벗어나기 위해.
    k=0                 
    while k < len(terms_phenotypes): #하나라도 찾았거나, 끝까지 뒤졌는데 못찾은 경우
        term_pheno = terms_phenotypes[k]
        if Abstract.lower().find(term_pheno) == -1:#해당 단어가 없을시 -1 반환.
            k+=1
        else:
            N_abstract += 1
            k = len(terms_phenotypes) #찾은 경우 while 벗어나기 위해.        
            




print('N_title: ',N_title,'\n','N_abstract: ',N_abstract)
print ('\r', N_abstract,' out of',len(id_list),term_herb,\
       '-related article(s) include(s)', "'",pheno_query,"'",'and its entry terms')



#본초 관련하여 검색할 질병 자체(와 관련 MeSH의 entry terms)를 포함하는 article 갯수 조사.
total_ids = []
for i, q in enumerate(terms_phenotypes):
    print(i+1,"out of", len(terms_phenotypes), 'MeSH terms')
    
    results_2 = pc.search(q)
    id_list_2 = results_2['IdList']
    total_ids.extend(id_list_2)

total_counts = len(list(set(total_ids)))
print('\r',"Total counts of articles with","'",pheno_query,"'",'and its entry terms:',total_counts)

#질병 관련 총 문서중 몇프로가 해당 본초 관련된것인지. (%)
print(N_abstract/total_counts*100, "%")
