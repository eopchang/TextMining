#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:17:15 2017

@author: Chang-Eop
"""


import os
os.chdir('/Users/Chang-Eop/Desktop/GitHub/TextMining/PainNetwork')



import numpy as np
import pandas as pd
import codecs
import csv


data = pd.read_excel('NIFSTD.xlsx')
data_1 = data.ix[:,['Preferred Label','Synonyms', 'has_obo_namespace']]

#data_1.ix[data_1.ix[:,0] == 'amygdala',:]

data_2 = data_1[data_1.ix[:,2] == 'uberon']
data_2.index = range(data_2.shape[0])



#NIFSTD의 동의어 정리
terms = [] #nested list 형식으로 동의어들 묶어넣을것
for i in range(data_2.shape[0]):
    term_prefer = data_2.ix[i,0]
    try: #동의어 없는 경우(nan) 대비.
        term_synonym = data_2.ix[i,1].split("|")
    except AttributeError:
        term_synonym = []
    
    temp = [term_prefer]
    temp.extend(term_synonym) #제일 앞이 prefer, 이어서 동의어들.
    terms.append(temp)


        
    
        
    
candi_terms = pd.read_excel('ROI_Brede.xlsx')#'170525_RPO_Brede(except_Broadmann_Economo_Monkey)_1107.xlsx')
#오지홍 정리 


#candidate terms 모으기    (nan 빼고, 그냥 다 리스트로 만든것)
candi_total = []
for i in range(candi_terms.shape[0]):
    for j in range(candi_terms.shape[1]):
        if type(candi_terms.ix[i,j]) == str: 
            candi_total.append([candi_terms.ix[i,j]])
        else:
            pass
        
        
# candidate terms 중에 NIFSTD 동의어 목록에서 찾아지는 수
count = 0        
for candi in candi_total:
    
    for t in range(len(terms)):
        if candi[0].lower() in terms[t]:
            count += 1
            
            

#text_total = pd.read_excel('pain_papers.txt')

f = codecs.open('pain_papers.txt','r',"utf-8")
texts = f.readlines() #초록 하나가 리스트의 요소 하나로 들어감.

#전체 소문자로 변환
for i,line in enumerate(texts):
    texts[i] = line.lower()



freq_of_candis = {}
for candi in candi_total:
    counts = 0
    
    #동의어 포함한 쿼리 구성
    for t in range(len(terms)):
        if candi[0].lower() in terms[t]: #동의어 목록에 있으면 
            query = terms[t] #동의어 리스트를 쿼리로
        else: #동의어 목록에 없으면 
            query = [candi[0].lower()] #그냥 그 자체만 리스트 형태로
    
    #전체 텍스트에서 쿼리(동의어 포함) 등장 빈도 카운트(문서당 최대 1회 카운트)
    for qs in query:
        for i, text in enumerate(texts):
            if " "+qs+" " in text: #해당 단어 앞뒤로 한칸씩 떨어져있을때만 카운트
                counts += 1

            
                
    freq_of_candis[candi[0]] = counts
    print(counts)
        

f2 = open('FreqCandis_ROI_Brede.csv', 'w')
w = csv.writer(f2)
for row in freq_of_candis.items():
    w.writerow(row)
f2.close()



 
         

        
        
 


    

    
    
    
            

            
    
    

        
        
  
        








data_2[data_2['Preferred Label'] == 'hypophysis']['Synonyms']
#data_2.to_excel('neural_nodes_candidates.xlsx')