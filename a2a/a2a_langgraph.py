'''
워크플로우 
    - 작성-리뷰-체크-수정-리뷰-체크-...
    - 엣지 구성 (규칙, 시작, 종료) 

구조 
    - Langgraph
    - State
    - Node - Coder Node / Reviewer Node

    - Edge - entry_point : Coder Node
           - code_dir : Coder Node -> Reviewer Node
           - Conditional Edge : Reviewer 판정에 따라 Coder Node / END 결정
'''

