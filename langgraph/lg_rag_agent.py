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

# 환경변수 호출
load_dotenv()


#---------------------------------------
# LLM 모델 구성
#---------------------------------------
llm = ChatBedrockConverse(model       = os.getenv('MODEL_ID'), 
                          max_tokens  = 1000,
                          temperature = 0.5,
                          region_name = os.getenv('AWS_REGION'))

tools = [rag_search]
llm_with_tools = llm.bind_tools(tools)

#---------------------------------------
# Few-Shot 프롬프트 구성
#---------------------------------------

examples        = [
    {"input":"비 오는 날엔 국물이 땡겨", "output":"국룰이죠. 칼국수나 잔치국수가 좋습니다."},
    {"input":"다이어트를 위해서 칼로리가 낮은 메뉴로", "output":"관리하시는군요. 닭가슴살 샐러드 드세요."}
]

example_prompt  = ChatPromptTemplate.from_messages([
    ('human', '{input}'  ),
    ('ai',    '{output}' ),
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples    = examples,
    example_prompt = example_prompt
)

final_prompt    = ChatPromptTemplate.from_messages([
    # 1. Persona
    ('system', '당신은 센스있는 식사 메뉴 추천 전문가입니다. 반드시 도구를 사용하여 실제 식당을 찾으세요.'), 
    # 2. Few-Shot Sample
    few_shot_prompt,
    # 3. User Question
    ('human', '{query}')
])


#---------------------------------------
# langgraph 구성 
#---------------------------------------

class AgentState(TypedDict):
    messages: List[ BaseMessage ]


# 노드 정의
def thinking_node( state:AgentState ):
    msg = state['messages'] 
    chain    = final_prompt | llm_with_tools
    res      = chain.invoke( {"query":msg})
    return {'messages':[ res ]}

def tool_node( state:AgentState ):
    last_msg = state['messages'][-1]
    print('tool_node 호출 : 툴 사용 LLM이 응답', last_msg.tool_calls)
    if last_msg.tool_calls:
        tool = last_msg.tool_calls[0]
        '''
        last_msg.tool_calls[
            {
                'name':'rag_search',
                'args':{'cate':'가벼운 식사'},
                'id':'toolsuse-aaldkjfaefb',
                'type':'tool_call'            
            }
        ]
        '''

        result = rag_search.invoke(tool['args'])
        print("RAG 호출 결과 : ", result)
        return {"messages":[
            HumanMessage(content=f'[사내데이터 검색결과]: {result}\n제공된 정보를 기반으로 최종 답변을 해줘.')
        ]}
    #보험용 return코드
    return {"messages":[]}

def final_answer_node( state:AgentState ):
    msg = state['messages']
    res = llm.invoke( msg ) 
    return {'messages':[ res ]}
    pass

# langgraph 연결
workflow = StateGraph(AgentState)
workflow.add_node('thinking',       thinking_node)
workflow.add_node('tool',           tool_node)
workflow.add_node('final_answer',   final_answer_node)
workflow.set_entry_point('thinking') 

def custom_check_tool_node(state:AgentState):
    last_msg = state['messages'][-1]
    if last_msg.tool_calls:
        print('툴 사용 필요')
        return 'tool'
    return END

workflow.add_conditional_edges('thinking', custom_check_tool_node)
workflow.add_edge('tool', 'final_answer')
workflow.add_edge('final_answer', END)

#---------------------------------------
# 
#---------------------------------------

랭그래프객체 = workflow.compile()
if __name__ == '__main__':
    res = 랭그래프객체.invoke( {"messages": "가벼운 식사"} )
    print( res )






