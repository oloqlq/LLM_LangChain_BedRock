'''
MCP Server 와 통신
MCP에서 정의한 Tool을 Langchain/Langgraph용 Tool로 변환 처리
'''
# 1. 모듈 가져오기
import asyncio
import sys
from typing import Optional
from mcp import ClientSession, StdioServerParameters # 커넥션 담당
from mcp.client.stdio import stdio_client # 입력, 출력을 가진 클라이언트
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field, create_model

# 2. MCPClient 클레스 구성
class MCPToolAdapter:
    '''MCP Server와 통신하는 클레스(역활:클라이언트)'''
    # 생성자
    def __init__(self, server_script: str = 'server.py'):
        '''
        Args:
            server_script: 실행할 Server측 스크립트 경로
        '''
        self.server_script  = server_script
        self.mcp_tools      = []   # mcp tool
        self.tools          = []   # langchain/langgraph tool
        self.read_stream    = None # 입력 스트림
        self.write_strema   = None # 출력 스트림
        self.session: Optional[ClientSession] = None
        self._stdio_context = None
        pass


# 4. 비동기 함수 호출 -> MCP 서버 연동
if __name__ == '__main__':
    pass