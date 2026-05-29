# 목표<br>
**LLM 기반 서비스 구성**

> 상세 구현 목표<br>

RAG<br>
vectorDB<br>
MCP<br>
chain -> graph 파이프라인 마이그레이션<br>
Agent<br>
A2A<br>


# 서비스 주제<br>
**식사 메뉴 해결사 (메뉴 추천)**

> 주요 기능<br>

`BedRock 사용`
- LLM 호출 담당

`LLM 모델`
- claude, openai, google 등

`웹 프론트 (챗봇)`
- streamlit 활용
- 파이썬으로만 구성 (html, css, js, x)

`백엔드`
- api 담당 -> BedRock과 통신 역할 (fastapi 구성)
- 화면 X

`langchain`
- 프롬프트 엔지니어링 담당


# 세팅

> 가상환경 구축

```
python -m venv llm_venv
```

> 활성화

```
#윈도우
.\llm_venv\Scripts\activate

#맥
source llm_venv/bin/activate
```

