'''
Agent 개발
    - Langchain, 'langgraph' 구성
    - Bedrock 기반 llm 사용
    - MCP를 이용하여 tool 사용
'''


#-------------------------------------
# Package Import
#-------------------------------------
import os
import boto3
import asyncio
from dotenv import load_dotenv

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode

from mcp_tools_adapter import MCPClient


load_dotenv()

#-------------------------------------
# BedrockMCPAgent 클래스 구성
#-------------------------------------
class BedrockMCPAgent:
    # 생성자
    def __init__(self, server_script: str = 'server.py', use_bedrock:bool = True):
        self.server_script  = server_script
        self.use_bedrock    = use_bedrock
        self.llm            = None
        self.tools          = []
        self.graph          = None 
        self.mcp_adapter    = None # mcp_tools_adapter

    # 초기화
    async def initialize(self):
        # MCP Tool 로드
        print(f'MCP Server와 연결 중...')
        # mcp_tools_adapter.py와 작업 기술

        # LLM 생성
        print(f'LLM 초기화 중..')
        self._init_llm()

        # 랭그래프 기반 에이전트 구성
        print(f'langgraph agent 구성 중..')
        self._setup_graph()

        print(f'초기화 완료\n 프롬프트 입력 대기..')
        return self
    
    
    # LLM 생성
    async def _init_llm():
        try:
            self.llm = ChatBedrock(
                model_id     = os.getenv('MODEL_ID'),
                client       = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION') ),
                model_kwargs = {"temperature":0.7, "max_tokens":2000})
            print("Bedrock LLM 객체 생성 완료")
        except Exception as e:
            '''
            pip install anthropic openai ...
            from langchain_anthropic import ChatAnthropic
            '''
            print("Bedrock LLM 객체 생성 실패 {e}")
            pass
        pass

    # 그래프 구성
    def _setup_graph(self):
        llm_with_tools = self.llm.bind_tools(self.tools)
        workflow = StateGraph(MessagesState)
        def call_agent(state:MessagesState) -> dict:
            '''LLM 호출하여 Tool 선택, 응답 생성'''
            pass
        tool_node = ToolNode(self.tools)
        workflow.add_node('agent', call_agent)
        workflow.add_node('tools', tool_node)

        workflow.set_entry_point('agent')
        
        def 조건부함수() -> str:
            '''tool_calls 값 체크, 판단'''
            pass

        workflow.add_conditional_edges(
            'agent',
            조건부함수,
            {
                "tools" : 'tools',
                "end"   : END
            }
        )
        workflow.add_edge('tools', 'agent')
        self.graph = workflow.compile()

        pass

    # 사용자 요청 처리
    # 메모리 정리
    pass



#-------------------------------------
# main
#-------------------------------------
async def main():
    # BedrockMCPAgent 생성
    # 사용자 입력 대기
    # BedrockMCPAgent의 사용자 요청 처리 함수 호출
    pass

#-------------------------------------
# 서비스 가동
#-------------------------------------
if __name__ =='__main__':
    asyncio.run(main())
