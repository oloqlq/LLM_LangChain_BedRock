

#-------------------------------------
# 1. 패키지 호출
#-------------------------------------

import streamlit as st

#-------------------------------------
# 2. 
#-------------------------------------
st.set_page_config(page_title='식사 메뉴 해결사')
st.title('AI 식사 메뉴 해결사 -KING')
st.caption('점심/저녁 등 시점, 날씨, 기분, 단체 여부, 예산, MBTI 등을 알려주시면 메뉴를 추천해드립니다.')

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            'role':'assistant',
            'content':'안녕하세요! 오늘 식사는 어떤 메뉴를 추천해 드릴까요? 현재 상황, 기분 등을 알려주세요. '
        }
    ]


for msg in st.session_state.messages:
    with st.chat_message( msg['role']):
        st.markdown( msg['content'])



if prompt := st.chat_input('현재 상황을 자세하게 입력하세요.'):
    st.session_state.messages.append({
        'role':'user',
        'content': prompt

    })
    with st.chat_message( 'user '):
        st.markdown( prompt )
    
    with st.chat_message('assistant'):
        msg_holder = st.empty()
        msg_holder.markdown( '심각한 고민중 -,.-^..' )


#-------------------------------------
# 
#-------------------------------------


#-------------------------------------
# 
#-------------------------------------