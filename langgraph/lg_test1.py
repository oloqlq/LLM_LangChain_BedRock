#----------------------------------------
# 패키지 호출
#----------------------------------------
from langgraph.graph import StateGraph, END
from typing import TypedDict # 공유 메모리의 형태 규정에 활용


#----------------------------------------
# 상태 정의 - 공유 메모리
#----------------------------------------
'''
[
    {"msg": "....."},
    {"msg": "....."},
    {"msg": "....."},

]
'''

class CustomState(TypedDict):
    msg:str


#----------------------------------------
# 노드 준비 - 단순한 함수로 구성
#----------------------------------------
def add_prefix(state:CustomState):
    '''
    기존 상태값에 특정 내용 추가
    parameters:
        - state : 공유 메모리, 전역 상태, 랭그래프에서 관리되는 상태
    '''
    return {'msg': "hello" + state['msg']}

    pass

def add_suffix(state:CustomState):
    return {'msg': state['msg'] + "!!"}
    pass





#----------------------------------------
# 그래프 연결/구성
#----------------------------------------

# 1. 그래프를 연결할 타겟. (기본 구성)
workflow = StateGraph(CustomState)

# 2. 노드(task, tool, agent)등을 추가.
workflow.add_node("T1", add_prefix)
workflow.add_node("T2", add_suffix)

# 3. 시작점 설정
workflow.set_entry_point("T1") 
workflow.add_edge('T1', 'T2')

# 4. 끝 점 설정
workflow.add_edge('T2', END)


#----------------------------------단방향성.

