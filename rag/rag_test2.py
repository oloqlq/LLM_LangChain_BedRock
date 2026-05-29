'''
vectorDB 데이터 구축
: RAG, vectorDB에 자연어를 토큰화하여 저장, 유사도기반 검색 실행
'''

from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
import boto3
from dotenv import load_dotenv
import os

# 대량 문서 처리 기능 제공
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

# Textloader를 통해 ./data/*.txt 경로에 있는 7개의 텍스트 파일을 [Document, ..., Document] 로 올림
import glob
files = glob.glob('./rag/data/*.txt')
raw_docs = [TextLoader(file, encoding='utf-8').load()[0] for file in files]
print(len(raw_docs), type(raw_docs[0]))


# 4. 텍스트 분할
splitter = RecursiveCharacterTextSplitter(  chunk_size      = 512,
                                            chunk_overlap   = 100
)
splites = splitter.split_documents(raw_docs)
#print(f"총 정크수 : {len(splites)}")
#print(f"내용 : {splites[0]}")
#print(f"내용 : {splites[1]}")


# 임베딩
tokenizer = BedrockEmbeddings(  model_id="amazon.titan-embed-text-v2:0",
                    region_name=os.getenv('AWS_REGION'))

# vectorDB에 토큰화된 벡터 데이터 입력
vector_db = FAISS.from_documents(splites, tokenizer)

# vectorDB에 세팅된 내용을 저장 
vector_db.save_local('harrypotter-story') # DAG기반 스케줄단위 갱신 가능

docs = vector_db.similarity_search("해리포터의 친구")
print(docs[0].page_content)

