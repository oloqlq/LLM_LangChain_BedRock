'''
백엔드 프로그램

1) 클라이언트 채팅 입력
2) ~/chat 요청
3) 프롬프트 구성
4) bedrock 호출
5) 응답
6) 처리
7) 프론트
'''


#-------------------------------------
# 1. 패키지 호출
#-------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel
import llm



#-------------------------------------
# 2. FastAPI 객체 생성
#-------------------------------------
app = FastAPI(title='식사 메뉴 추천 AI')


#-------------------------------------
# 3. 요청 데이터 구조 정의
#-------------------------------------
class UserRequest(BaseModel):
    query:str

#-------------------------------------
# 4. API 구성
#-------------------------------------
@app.post('/chat')
async def chat(req:UserRequest):
    # LLM 호출

    return f"돈까스 {req.query}"
