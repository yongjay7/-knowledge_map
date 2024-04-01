
import streamlit as st

## *** 학교급 및 학년 뷰 정보***
es_grade = ['3학년','4학년','5학년','6학년']
ms_grade = ['1학년','2학년','3학년']
hs_grade = ['1학년'] 

school_lv = ["초등학생", "중학생", "고등학생"]
school_info = {
    '초등학생': es_grade, 
    '중학생': ms_grade,
    '고등학생': hs_grade
    }   


def get_selected_school_garde(key_value):
    st.markdown("##### 학교급, 학년도별 주제를 확인합니다.")

    col1, col2 = st.columns([1, 3])
    with col1:    
        with st.container(border=True):
            school_lv_choice = st.radio(
                "학교급 선택",
                school_lv,
                 key=key_value,
    )
    with col2: 
        with st.container(border=True):
            selected_list = st.selectbox('학년선택', school_info[school_lv_choice],  key='select'+str(key_value))

    return school_lv_choice, selected_list[:1]