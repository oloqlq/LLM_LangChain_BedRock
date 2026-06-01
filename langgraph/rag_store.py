'''
- RAG 기반 검색기능 제공
- 검색어 -> 벡터디비 검색(유사도 검색) -> 결과값 반환
'''

from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

#임베딩 모델 구성 - 토크나이저 획득
tokenizer = BedrockEmbeddings(  model_id="amazon.titan-embed-text-v2:0",
                                region_name=os.getenv('AWS_REGION'))

# 더미 데이터 구성(LLM이 모르는 사내 데이터 및 최신 데이터 등)
