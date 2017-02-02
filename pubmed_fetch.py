# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 20:04:59 2017

@author: Chang-Eop
"""
import os
from Bio import Entrez

os.chdir('/Users/Chang-Eop/Desktop/GitHub/TextMining')


def search(query):
    Entrez.email = 'eopchang@gmail.com'
    
    #먼저 검색되는 총 문서 수 total_counts 구함.
    handle4counts = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax= '1',
                            retmode='xml',
                            term=query)
    total_counts = Entrez.read(handle4counts)['Count']
    
    #구해진 total_counts 정보 이용하여 한번에 다 추출(너무 많으면 에러 날수도???)
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax= total_counts,#str(no_max),
                            retmode='xml', 
                            term=query)
                            
    results = Entrez.read(handle)
    return results
    
    
    
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'eopchang@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results
    
    
 #본 함수. term에 쿼리를 넣으면 됨. 현재는 제목만 출력하도록. Abstract 출력은 더 손봐야 함    
def articles(term):   
    results = search(term)
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, j in enumerate(id_list):
        article = papers['PubmedArticle'][i]['MedlineCitation']['Article']
        Title = article['ArticleTitle']
        #Abstract = article['Abstract']['AbstractText']
        
        print("%d) %s" % (i+1, Title))