'''
MCP 1.27.2
외부 도구를 구현한 MCP 서버. FastMCP를 이용하여 간결하게 구성
'''


#--------------------------------
# 패키지 호출
#--------------------------------
import sys
import logging
from datetime import datetime
from mcp.server.fastmcp import FastMCP



#--------------------------------
# Logging 설정
#--------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='[MCP Server] %(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)
logger.info('MCP Server 구성 중 ...')




#--------------------------------
# MCP 서버 설정 
#--------------------------------

mcp = FastMCP('6ToolsMCPServer')
logger.info('MCPServer 구성(초기화) 중 ...')



#--------------------------------
# 인메모리
#--------------------------------
note_memory = dict()



#--------------------------------
# Tool 구현 
#--------------------------------
# 외부 리소스
# 간단한 기능 구현 (6개)

def add(a:float, b:float) -> str:
    '''
    두 수를 더하는 계산기
    Args : 
        a : 첫 번째 수치
        b : 두 번째 수치
    
    Returns
        계산 결과
    '''
    result = a + b
    logger.info(f'Tool 1 add 호출: {a} + {b} = {result}')
    return f'계산 결과 : {a}+{b}={result}'

#--------------------------------
# 서버 가동
#--------------------------------