'''
저장된 vectorDB Load
LLM 이용 추론 -> 프롬프트에 RAG이용 검색 증강용 데이터 추가하여 추론 진행
    - 프롬프트 : 질의 + RAG검색결과
랭체인의 체인 구성
'''


#----------------------------------------
# 패키지 호출
#----------------------------------------

from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import boto3
from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv()


#----------------------------------------
# 임베딩 모델 로드
#----------------------------------------
tokenizer = BedrockEmbeddings(  model_id="amazon.titan-embed-text-v2:0",
                                region_name=os.getenv('AWS_REGION'))





#----------------------------------------
# DB파일 기반 로드
#----------------------------------------
vector_DB = FAISS.load_local('harrypotter-story', tokenizer, allow_dangerous_deserialization=True)




bedrock_client = boto3.client(
    service_name = 'bedrock-runtime',
    region_name = os.getenv('AWS_REGION')
)

llm = ChatBedrock(
    client = bedrock_client,
    model_id = 'openai.gpt-oss-120b-1:0',
    model_kwargs = {
        "max_tokens" : 512,
        "temperature": 0.7
    }
)





#----------------------------------------
# 프롬프트 구성
#----------------------------------------

prompt = ChatPromptTemplate.from_template('''
다음의 제공된 context(문맥, 참고)를 사용하여 질문에 답변해 주세요.
만약 문맥에서 답을 찾을 수 없다면 "잘 모르겠음"으로 답변해 주세요.                        
<context>
{context}
<context> 
                                                    
질문 : {user_input}                             
''')

#----------------------------------------
# 체인 구성
#----------------------------------------

retriever = vector_DB.as_retriever(search_kwargs={"k":3})

def format_docs(docs):
    '''
    청크 1 -> 유사도 1등

    청크 2 -> 유사도 2등

    청크 3 -> 유사도 3등
    '''
    return "\n\n".join( doc.page_content for doc in docs)

rag_chain = (
    {"context":retriever | format_docs, "user_input":RunnablePassthrough()}
    | prompt 
    | llm 
    | StrOutputParser()
)




# 실행
query = "해리포터의 가장 친한 친구 2명은?"
res = rag_chain.invoke(query)

print('==AI답변==')
print( res )