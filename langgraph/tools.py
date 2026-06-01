'''
각종 tool을 모아놓은 모듈
'''

from langchain_core.tools import tool
from rag_store import search_stores

@tool
def rag_search(cate:str)->str:
    '''
        성향, 메뉴, 카테고리 등을 입력받아서 
    '''
    res = search_stores(cate)
    return res if res else '관련 식당 정보를 찾을 수 없습니다.'
