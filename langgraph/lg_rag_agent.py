'''
식사 추천
    - RAG 활용 : Tool로 차용하는 방식 
    - langgraph 활용
'''

#---------------------------------------
# 패키지 호출
#---------------------------------------
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.tools import tool 
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_aws import ChatBedrockConverse 
from langgraph.prebuilt import ToolNode, tools_condition   
from dotenv import load_dotenv
import os
import boto3

from tools import rag_search
print(rag_search)
# 환경변수 호출

#---------------------------------------
# 
#---------------------------------------



#---------------------------------------
# 
#---------------------------------------



#---------------------------------------
# 
#---------------------------------------




#---------------------------------------
# 
#---------------------------------------


