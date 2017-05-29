#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:17:15 2017

@author: Chang-Eop
"""


import os
os.chdir('/Users/Chang-Eop/Desktop/GitHub/TextMining/PainNetwork')



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import codecs
import csv
import re




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



#candidate terms의 동의어들로 쿼리 구성하고, 문서 전체에서의 등장 빈도 카운트
freq_of_candis = {}

n = 0
for candi in candi_total:
    counts = 0
    n += 1
    
    #단어 앞뒤 공백 제거
    candi = [candi[0].strip()]
    #동의어 포함한 쿼리 구성
    for t in range(len(terms)):
        if candi[0].lower() in terms[t]: #동의어 목록에 있으면 
            query = terms[t] #동의어 리스트를 쿼리로
            break #찾아으면 다음 루프로
        else: #동의어 목록에 없으면 
            query = [candi[0].lower()] #그냥 그 자체만 리스트 형태로
    
    #전체 텍스트에서 쿼리(동의어 포함) 등장 빈도 카운트(문서당 최대 1회 카운트)
    for qs in query:
        for i, text in enumerate(texts):
            if qs in text: #해당 용어 발견했을때
                
                pattern_0 = re.compile(qs) #용어 존재    
                pattern_1 = re.compile('[a-z]'+qs)#용어 앞에 다른 문자 연결되어있거나
                pattern_2 = re.compile(qs+'[a-z]')#용어 뒤에 다른 문자 연결된 경우라면
                
                iters = pattern_0.finditer(text) #용어 존재하는 경우를  iterable 객체로 반환
                
                for it in iters: #용어 존재 경우 하나씩 돌아가면서
                    start = it.span()[0] #텍스트 상에서의 시작위치
                    end = it.span()[1] #텍스트 상에서의 용어 종료 위치
                    test_phrase = text[start-1:end+1] #용어 앞뒤로 한칸 추가하여 따냄
                    if not (pattern_1.search(test_phrase)) and not (pattern_2.search(test_phrase)):
                        # 앞뒤로 알파벳 있지 않은 경우만 카운트
                        counts += 1
                        print(text)
                        break #하나라도 찾아서 카운트했으면 다음 텍스트로 넘어감
       
                
    freq_of_candis[candi[0]] = counts
    print(counts, ", ", n, " of ", len(candi_total))
        

#결과 csv 포맷으로 저장
f2 = open('FreqCandis_ROI_Brede.csv', 'w')
w = csv.writer(f2)
for row in freq_of_candis.items():
    w.writerow(row)
f2.close()



         

        
 #이하 작업중 시험 코드       
 


    

    
    
pattern = re.compile('[a-z]')
pattern.se            

            
    
    

        
        
for i in texts:
    print(i, len(texts))
    if i == '\n':
        texts.remove(i)
        
for i in texts:
    if 'after 2 h the animals were perfused. paraffin embedded brain sections immunoreacted with an antibody selective for' in i:
        break







results_2[0].keys()
results_2[0]['MedlineCitation']['Article']['Abstract']





data_2[data_2['Preferred Label'] == 'hypophysis']['Synonyms']
#data_2.to_excel('neural_nodes_candidates.xlsx')




flag = 0
for i, j  in enumerate(texts):
    print(i, len(texts))
    if text in j:
        flag = 1
        print(1000000000)
        
    
    