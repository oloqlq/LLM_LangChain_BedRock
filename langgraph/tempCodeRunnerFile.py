'''
- TOOL 사용, LLM 적용
'''

#----------------------------------------
# 패키지 호출
#----------------------------------------
from langgraph.graph import StateGraph, END, MessagesState, START
from typing import TypedDict
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage 
from langchain_aws import ChatBedrock, ChatBedrockConverse
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import os
import boto3

# 환경변수 로드
load_dotenv()


#----------------------------------------
# LLM 추론용 객체 생성 - 전역변수
#----------------------------------------
llm = ChatBedrock(model   = os.getenv('MODEL_ID'),
            client  = boto3.client('bedrock-runtime', region_name = os.getenv('AWS_REGION'))
        )

#----------------------------------------
# Tool 준비
#----------------------------------------
@tool
def multiply(a: int, b: int) -> int:
    """두 정수 a와 b를 곱한 결과를 반환합니다."""
    print(f'        [Tool 실행] {a} x {b} 계산중..')
    return a * b




#----------------------------------------
# LLM - Tool 등록
#----------------------------------------
tools = [multiply]
llm_with_tools = llm.bind_tools(tools) 



#----------------------------------------
# Node 구성
#----------------------------------------

def chatbot_node(state:MessagesState):
    print('[chatbot node 호출 전]', state)
    res = llm_with_tools.invoke(state['messages'])
    new_state = {"messages": [res]}

    print('[chatbot node 호출 후 상태 값]', state)
    return new_state


#----------------------------------------
# langgraph 구성
#----------------------------------------

# 1. 그래프 생성
workflow = StateGraph(MessagesState)

# 2. 노드 추가 
workflow.add_node('chatbot', chatbot_node)
workflow.add_node('tools', ToolNode(tools))

# 3. 시작점 
workflow.add_edge(START, 'chatbot')

# 4. 조건에 따라 행동을 다르게 수행 구성
workflow.add_conditional_edges(
    'chatbot',
    tools_condition
)

# 도구 사용 -> 결과 획득 -> 챗봇 전달 -> ...
workflow.add_edge('tools', 'chatbot')
app = workflow.compile()


if __name__ == '__main__':
    while True:
        user_input = input('\n유저: ').lower()

        if user_input == 'q': break
        prompt = {"messages": [ HumanMessage(content=user_input)]}
        print(prompt)
        for evt in app.stream(prompt, stream_mode='values'):
            msg = evt['messages'][-1]
            print("Agent", msg.content)

