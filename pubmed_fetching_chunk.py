#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 09:34:24 2017

parameter: query (str), size (int)
output: results_2 (list)

query에 대한 문헌정보 결과들을 results_2(list)에 담음.
수천-수십만건의 정보를 fetching하는 동안 반복적으로 네트워크 에러 발생
스크립트의 문제가 아니라 NCBI 서버에서 제한하는 것으로 시간대, 접속자의  IP 등 여러가지가 영향을 미침
에러로 중단시 지속적으로 다시 시도해야 하므로 전체  fetching할 문서들을 size의 chunk로 나눈후 chunk 단위로 루프 돌려 패칭
에러 발생시 ###FETCHING###이하의 for loop 에서 range의 시작점(최초 시작시엔 0으로 셋팅)만 에러 당시의 i 값으로 변경하여
다시 수행하면 됨. 
"""

query = 'pain[majr]' # [majr]:to search a MeSH heading that is a major topic of an article
size = 1000


from Bio import Entrez
import numpy as np

Entrez.email = 'eopchang@gmail.com'
handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax= '10000000',#str(no_max),
                            retmode='xml', 
                            term=query)                            
results = Entrez.read(handle)
id_list = results['IdList']

#chunk 로 쪼개기
n_id = len(id_list)
n_groups = int(np.ceil(n_id/size))
id_list_new =  np.zeros((n_groups,size), dtype = int)
for i in range(n_groups):
   for j in range(size):
       try: #마지막 행(그룹)은 pop할 남은 ID 없어 에러 발생 가능.
            id_list_new[i,j] = id_list.pop(0)
       except IndexError: 
            pass
              
        
results_2 = []#패칭 결과 담을 리스트     

            
            
########FETCHING##############
for i in range(87, n_groups): #네트워크 에러로 끈길 경우 0을 끊긴 시점의 i 값으로 대체하고 for 구문 다시 수행
    print(i+1, ' of ', n_groups)
    chunk = id_list_new[i,:]
    chunk = list(chunk[chunk > 0]) # 마지막 그룹은 ID자리에 0 이 있을수 있으므로.
    chunk = str(chunk)[1:-1] 
    
    handle = Entrez.efetch(db='pubmed',
                       retmode='xml',
                       id=chunk)
    res = Entrez.read(handle)
    res_articles = res['PubmedArticle']
    results_2.extend(res_articles)