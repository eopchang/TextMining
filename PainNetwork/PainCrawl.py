#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 15:34:18 2017

@author: Chang-Eop
"""

import pubmed_crawler as pc
from Bio import Entrez
import pandas as pd
import numpy as np

Entrez.email = 'eopchang@gmail.com'

query = 'pain[majr]' # [majr]:to search a MeSH heading that is a major topic of an article
size = 1000

handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax= '10000000',#str(no_max),
                            retmode='xml', 
                            term=query)
                            
results = Entrez.read(handle)

id_list = results['IdList']

n_id = len(id_list)
n_groups = int(np.ceil(n_id/size))
id_list_new =  np.zeros((n_groups,size), dtype = int)
for i in range(n_groups):
   for j in range(size):
       try: #마지막 행(그룹)은 pop할 남은 ID 없어 에러 발생 가능.
            id_list_new[i,j] = id_list.pop(0)
       except IndexError: 
            pass
                
results_2 = []        


for i in range(0, n_groups): #네트워크 에러로 끈길 경우 0을 끊긴 시점의 i 값으로 대체하고 for 구문 다시 수행
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