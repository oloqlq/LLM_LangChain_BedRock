# LLM 기반 서비스 구성
## **식사 메뉴 해결사 (메뉴 추천)**

> 상세 구현 목표<br>

RAG<br>
vectorDB<br>
MCP<br>
chain -> graph 파이프라인 마이그레이션<br>
Agent<br>
A2A<br>


> 주요 기능<br>

`BedRock 사용`
- LLM 호출 담당

`LLM 모델`
- claude, openai, google 등

`웹 프론트`
- streamlit 활용
- 파이썬으로만 구성 (html, css, js, x)
- 챗봇 스타일

`백엔드`
- api 담당 -> BedRock과 통신 역할 (fastapi 구성)
- 화면 X

`langchain`
- 프롬프트 엔지니어링 담당


## 세팅

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

> .gitignore 
```
    ...
    #가상환경제외
    llm_venv
```

> 패키지 설치
```
   (llm_venv) > pip install -r requirements.txt
```


> requirements.txt
```
    fastapi         # 백엔드 구성, bedrock 호출
    uvicorn         # fastapi 구동
    streamlit       # 프론트 구성
    requests        # 프론트 -> 백엔드 요청
    boto3           # AWWS SDK
    langchain-aws   # AWS 전용 랭체인
    langchain-core  # 랭체인 코어 라이브러리
    python-dotenv   # 환경변수, .env 로드
```


## 환경변수
> .env

```
    AWS_REGION
    MODEL_ID
    AWS_BEDROCK_CLAUDE_API_KEY
```


## 구동
> 백엔드 : server.py
```
    uvicorn server:app --reload --port 8000
```
- 테스트
    - http://127.0.0.1:8000/chat
    - post 방식 요청

> 프론트 : app.py

<br>
<br>
<br>
<br>
<br>



# RAG; 검색 증강

데이터에 대한 보안 이슈 등 학습에 동원되지 않았던 데이터를 추론하기에는 한계가 있다.
- 파인튜닝 -> 신규 학습 -> 모델 공개 : 신뢰하기 힘들고 진행하기 어렵다. 비용도 많이 발생
<br>
<br>

**LLM이 한번도 접하지 못했던 데이터를 활용하는 전략**
- 사내 데이터, 개인 데이터, LLM 생성 이후로 발생한 데이터 등

> **RAG : 사내 데이터를 노출하지 않으면서 LLM을 활용하기 위한 도구**<br>
LLM이 훈련하지 않은 최신 정보나, 기업 내부 데이터에 대해서 정확하고 신뢰성 있는 답변을 생성할 수 있게끔.
- 파인튜닝에 비해서 비용이 효율적이다. 
- 벡터 DB만 업데이트해주면 되기 때문

`최근 방식`<br>
엣지 - 사내 구축 (클라우드 중심) <br>
: 온프레미스, 디바이스 AI모델에서 이동하는 추세.

>> 추가 설치 패키지
```
    langchain-community
    faiss-cpu
    langchain
```

<br>
<br>
<br>

## vector DB 

> **장기 기억, RAG를 위한 저장소/검색/유사도 기능을 제공하는 데이터베이스**<br>

`자연어 -> 토크나이저 (제품 선정) -> 벡터화 -> 적재`

>> 토크나이저 종류<br>
- Pinecone
- Milvus
- Qdrant
- aws

- 메모리 기반 : Chroma, FAISS (Meta)


<br>
<br>
<br>

# LangGraph 

> LLM을 활용하여 복잡한 다중 에이전트 시스템, 워크플로우 빌드를 도와주는 오픈소스 프레임워크<br>
랭체인에서 만든 라이브러리.

워크플로우 일직선 : langchain<br>
워크플로우 그래프 : langgraph

>> **구성**
- `노드 (node)` : 실제 수행할 작업(task, 액션) 단위
    - 프롬프트 실행, 파이썬 코드 실행, api호출, ...
    - 특정 수행 목적을 가진 에이전트 (어떠한 작업을 수행하는 단위. 규모는 제각각)

- `엣지 (edge)` : 노드와 노드를 연결하는 경로
    - A 노드의 작업이 끝나면, B노드로 이동하여 작업 시작 -> 규칙
    - 조건에 따라 특정 노드로 이동하여 작업 진행 -> **조건부 엣지**

- `상태관리(state)` : 그래프 전체를 관통하는 공유메모리
    - 노드에서 작업이 완료되고 특정한 값이나 상태를 공유 메모리에 업데이트하면, <br>
    다른 노드가 이에 접근하여 진행.

- `사용 이유`
1. **단방향 chain의 단점**
    - looping(되돌아가기)이 어렵다.
    - 문제 발생 시 다시 이전 노드로 돌아가는 구조를 작성하기 어려움.
    - 사람의 개입 시 일시정지, 재개 등을 구현하기 어려움.

2. **역할 분담**
    - 에이전트 규모에 따라서 협업이 필요함.
    - 단방향은 절차적으로 진행하기 때문에 협업하는 구조가 수직적이다.
    - 반복 루프, 사람의 개입, 다중 에이전트(A2A) 협업에 수월하다!


>> **설치**
```
    #requirements.txt
    langgraph
    pip install -r requirements.txt
```