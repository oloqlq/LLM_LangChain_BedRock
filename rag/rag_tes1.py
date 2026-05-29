'''
vectorDB 데이터 구축
: RAG, vectorDB에 자연어를 토큰화하여 저장, 유사도기반 검색 실행
'''

from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

data = [
    "맥도널드 대표 제품은 빅맥이다.",
    "버거킹의 대표 제품은 와퍼이다.",
    "맘스터치의 대표 제품은 휠레버거이다.",
    "롯데리아의 대표 제품은 새우버거이다."
]

# 임베딩
tokenizer = BedrockEmbeddings(  model_id="amazon.titan-embed-text-v2:0",
                    region_name=os.getenv('AWS_REGION'))

vector_db = FAISS.from_texts(data, tokenizer)

docs = vector_db.similarity_search("버거킹의 대표 메뉴는?")

print(docs)
