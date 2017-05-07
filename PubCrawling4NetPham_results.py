#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 00:52:50 2017

@author: Chang-Eop
"""

import os
os.chdir('/Users/Chang-Eop/Desktop/GitHub/TextMining')


import pubmed_crawler as pc
import pandas as pd



#펍메드에서 검색할 본초
HOI = 'ginseng'#herb of interest
entry_terms_herb = pc.MeSH_terms_2(HOI) #관심본초의 유사어포함 목록 작성.

#HOI의 유사어들 모두에 대한 검색결과 (아이디) 수집
id_lists = []
for i, term in enumerate(entry_terms_herb):
    print(i+1, " of ", len(entry_terms_herb))
    results = pc.search(term)
    id_list = results['IdList']
    id_lists.extend(id_list)
    
id_lists = list(set(id_lists)) #중복 제거
    
    
###시간 오래 걸림
papers = pc.fetch_details(id_lists)
###

#++++++++++++++++++++++++++++++++++++++++++

D_info = pd.read_excel('05_Info_Diseases.xlsx')
Result = pd.DataFrame(columns = ['total counts of search results',
                        'occurences in titles of HOI papers', 
                        'occurences in abstracts of HOI papers', 
                        'fractions', 'entry terms'])

for I, J in enumerate(D_info['disease_name']):
    print('\n\n\n\n', I+1, " of ", len(D_info['disease_name']), 'in outmost loop', '\n\n\n\n')
    

    #본초로 검색돈 문서들의 제목, 초록에서 검색할 질병.  (경로 등의 표현형도 괜찮은지 아직 확인 X)
    terms_phenotypes = pc.MeSH_terms_2(J) #MeSH entry terms 리스트 구성
    
    #terms_phenotypes 등장한 title, abstract 갯수 초기값.
    N_title = 0
    N_abstract = 0
    
    IDsNotFound = [] #id_list에 있으나 실제 검색되지 않는 id들이 존재하여 확인.
    for i, j in enumerate(id_lists):
        print('\t',i+1, ' of ', len(id_lists))
        
        try:
            article = papers['PubmedArticle'][i]['MedlineCitation']['Article']
        except IndexError:
            IDsNotFound.append(j)
                
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
    print ('\r', N_abstract,' out of',len(id_lists),HOI,\
           '-related article(s) include(s)', "'",J,"'",'and its entry terms')
    
    
    if not N_abstract== 0 & N_title == 0:
        
        #본초 관련하여 검색할 질병 자체(와 관련 MeSH의 entry terms)를 포함하는 article 갯수 조사.
        total_ids = []
        for i, q in enumerate(terms_phenotypes):
            print('\t',i+1,"out of", len(terms_phenotypes), 'Entry terms')
            
            results_2 = pc.search(q)
            id_list_2 = results_2['IdList']
            total_ids.extend(id_list_2)
        
        total_counts = len(list(set(total_ids)))
        print('\r',"Total counts of articles with","'",J,"'",'and its entry terms:',total_counts)
        
        #질병 관련 총 문서중 몇프로가 해당 본초 관련된것인지. (%)
        if total_counts == 0: #검색어에 대한 subject heading이 없는 경우 terms_phenotype이 공리스트가 되고, total counts=0될수 있음.
            fraction = '-' 
            print('\n','fraction: ', fraction)
            Result.ix[J,:] = [total_counts, N_title, N_abstract,
                 fraction, '-']
        else:
           fraction =  N_abstract/total_counts*100
           print('\n','fraction: ', fraction, "%")
           Result.ix[J,:] = [total_counts, N_title, N_abstract,
                 fraction, str(terms_phenotypes)] 
           
    else:#HOI 논문들에 해당질병 없는 경우 시간절약 위해 해당질병 포함 논문 카운트 하지 않음.
           Result.ix[J,:] = ['Not counted', N_title, N_abstract,
                 '-', str(terms_phenotypes)] 

    
    
    





