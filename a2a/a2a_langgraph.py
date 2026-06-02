'''
> 워크플로우 
    - 작성-리뷰-체크-수정-리뷰-체크-...
    - 엣지 구성 (규칙, 시작, 종료) 

> 구조 
    - Langgraph
    - State
    - Node - Coder Node / Reviewer Node

    - Edge - entry_point : Coder Node
           - code_dir : Coder Node -> Reviewer Node
           - Conditional Edge : Reviewer 판정에 따라 Coder Node / END 결정
'''
#----------------------------
# 패키지 호출
#----------------------------
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import Annotated, List, TypedDict
import operator 
import dotenv
import boto3
import os
dotenv.load_dotenv()


#----------------------------
# 상태 정의
#----------------------------
class AgentState(TypedDict):
    messages    : Annotated[List[BaseMessage], operator.add ]
    interations : int


#----------------------------
# LLM 구성
#----------------------------
llm = ChatBedrock( model_id = os.getenv('MODEL_ID'),
    client       = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION') ),
    model_kwargs = {"temperature":0.7}
)

#----------------------------
# Agent 
#----------------------------


#----------------------------
# 조건부 엣지
#----------------------------



#----------------------------
# 그래프 구성
#----------------------------


#----------------------------
# 실행
#----------------------------

if __name__ == '__main__':
    pass
