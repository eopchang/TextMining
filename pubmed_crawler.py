#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 00:51:32 2017

@author: Chang-Eop
"""

from Bio import Entrez



def search(query):
    Entrez.email = 'eopchang@gmail.com'

    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax= '10000000',#str(no_max),
                            retmode='xml', 
                            term=query)
                            
    results = Entrez.read(handle)
    return results
    


    
def fetch_details(id_list, size):
    '''
    size만큼의 chunk로 나누어 fetch하고 결과를 합침. 
    결과는 efetch로 얻은 handle을 read한 후
    'PubmedArticle' key의 value(list 구조)임
    '''
    import numpy as np
    
    Entrez.email = 'eopchang@gmail.com'
    n_id = len(id_list)
    n_groups = int(np.ceil(n_id/size))
    id_list_new =  np.zeros((n_groups,size), dtype = int)
    for i in range(n_groups):
        for j in range(size):
            try: #마지막 행(그룹)은 pop할 남은 ID 없어 에러 발생 가능.
                id_list_new[i,j] = id_list.pop(0)
            except IndexError: 
                pass
                
    results = []        
    for i in range(n_groups):
        chunk = id_list_new[i,:]
        chunk = list(chunk[chunk > 0]) # 마지막 그룹은 ID자리에 0 이 있을수 있으므로.
        chunk = str(chunk)[1:-1] 
                    
        handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=chunk)
        res = Entrez.read(handle)
        res_articles = res['PubmedArticle']
        results.extend(res_articles)
        
    return results
    


#================================================================
def space_remover(string_term):
    """ 문자열 인수로 받아 앞뒤로 공백이 있다면 몇개든 제거.
    문자열 중간의 공백은 제거하지 않음."""
    while string_term[0].isspace():
        string_term = string_term[1:]
        
    while string_term[-1].isspace():
        string_term = string_term[:-1]
    
    return string_term


def MeSH_terms(query):
    
    """https://www.ncbi.nlm.nih.gov/에서 DB를 MeSH로 설정하고 query를 날렸을때 나오는 검색결과(search results)
    의 items 각각에 대하여, 클릭했을때 확인할 수 있는  유사어(Entry terms)를 모아  인풋 query, 검색결과 items의 각 제목들과
    모아 리스트로 만들어 반환.
    즉, 검색어, 검색어에 의한 검색결과들 제목들, 각 제목들에 대한 entry terms를 모두 모아 반환.
    *중복된 term은 제거되어있음.
    *모든 term은 소문자로 일괄 변환되어있음.
    *모든 term은 앞뒤 공백이 없도록 다듬어져있음."""

    Entrez.email = 'eopchang@gmail.com'
    
    handle = Entrez.esearch(db="MeSH", term= query)
    search_results = Entrez.read(handle) #query에 대한 search results로 items의 정보들. (id 갯수가 검색결과수)
    #검색결과에 query와 동일한 term이 있을수도 있고 없을수도 있음.
    #각 item별로 Entry terms 제시됨. 

    terms_phenotypes = [query] #query가 초기 연구자가 넣은 값
    for m in range(int(search_results['Count'])-1):#m 순서가 웹에서 보여지는 순서 아님. 주의.
        handle_2 = Entrez.efetch(db="MeSH", retmode='xml',id =  search_results['IdList'][m])# 몇번째 취할지가 문제
        EachItem = handle_2.read()
        
        title = EachItem.split(":")[1].split("\n")[0].split("[")[0]#항목들 제목 부분.  
       
        title = space_remover(title) #제목은 한칸 뛰고 시작함.
        entryterms = EachItem.split("\nEntry Terms:\n")[1].split("\n\n")[0]
        entryterms = entryterms.split("\n")
        entryterms = [space_remover(term) for term in entryterms] #텀마다 앞에 공백 4칸
        entryterms.append(title)
        EnryTermsforEachItem = [term.lower() for term in entryterms] # 소문자로 일괄 변경
        
        terms_phenotypes.extend(EnryTermsforEachItem)
    return list(set(terms_phenotypes)) #중복 있는 경우 제거.
    




def MeSH_terms_2(query):
    
    """MeSH_term와 달리 search results 중 제일 상단, 첫번째 item만의 entry term을 수집
    """

    Entrez.email = 'eopchang@gmail.com'
    
    handle = Entrez.esearch(db="MeSH", term= query)
    search_results = Entrez.read(handle) #query에 대한 search results로 items의 정보들. (id 갯수가 검색결과수)
    #검색결과에 query와 동일한 term이 있을수도 있고 없을수도 있음.
    #각 item별로 Entry terms 제시됨. 
    
    #쿼리의 subject heading을 취함.
    if len(search_results['TranslationSet']) > 0: #보통은 검색어와 subject heading이 불일치하여 전환됨. 
        sub_heading = search_results['QueryTranslation'].split("[MeSH")[0].split('"')[1] 
        sub_heading = sub_heading.lower()
        terms_phenotypes = [query.lower(), sub_heading]#query와 query의 MeSH term을 리스트에 추가
    else: #검색 쿼리가 정확히 subject heading인 경우
        sub_heading = query.lower()
        terms_phenotypes = [sub_heading]
        #query가 곧 MeSH term이므로 이를 리스트에 추가
     
    
    #MeSH term(subject heading의 entry terms 추가하기)
    handle = Entrez.efetch(db="MeSH", retmode='xml',id =  search_results['IdList'])# 일단 검색된 item들 다 모으고
    try:
        Item = handle.read() 
    except UnicodeDecodeError: #알수 없는 디코딩 에러가 발생하는 경우가 있음. 
        return [] #일단 공리스트 반환하는걸로 처리. 나중에 이런 에러 몇개나 나는지 일괄확인 필요.
    
    Item = Item.lower() #소문자로 변환.
    
    try:
        entryterms = Item.split(": " + sub_heading + '\n')[1].split("entry terms:\n")[1].split("\n\n")[0]
        #query에 대한 search results가 없는데 subject heading 찾는 과정에서 
        #부분 term(띄어쓰기 포함 term에서 일부분)으로 엉뚱하게 translaton되어 그걸
        #subject heading으로 잡고 여기까지 왔다면, search results의 IDList가 비어있으므로
        #handle도 비고, Itemㄷ 비어서 여기서 에러나게되어있음. 
    except IndexError:
        return [query.lower()]
    
    entryterms = entryterms.split("\n")
    entryterms = [space_remover(term) for term in entryterms] #텀마다 앞에 공백 4칸
     
    terms_phenotypes.extend(entryterms)
    return terms_phenotypes 