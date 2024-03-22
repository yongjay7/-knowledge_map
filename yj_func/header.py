import pandas as pd
import streamlit as st

from data import curriculum_info as curri_info

main_code = pd.DataFrame() # 코드 정보
subA_code = pd.DataFrame() # 대주제 정보
subB_code = pd.DataFrame() # 중주제 정보
subC_code = pd.DataFrame() # 소주제 정보
achi_code = pd.DataFrame() # 성취기준 정보

def get_subjects_code(subject):
# 선택된 메뉴에 따라 다른 데이터 표시 ***헤더 뷰 정보***
    if subject == "수학":

        st.markdown("##### 수학 데이터를 표시합니다.")
        main_code = curri_info.get_data_math(0)
        subA_code = curri_info.get_data_math('A')
        subB_code = curri_info.get_data_math('B')
        subC_code = curri_info.get_data_math('C')
        achi_code = curri_info.get_data_math('ACH')

        label_text = "수학과목 코드 정보"
        with st.expander(label=label_text, expanded=True):
            st.dataframe(main_code) 
        
        return main_code, subA_code, subB_code, subC_code, achi_code
        
    elif subject == "영어":
        st.write("영어 데이터를 표시합니다.")
        df = curri_info.get_data_english(0)
        st.dataframe(df.head()) 

        return 0
    
    else:
        st.write("정보 데이터를 표시합니다.")
        st.dataframe(df_s.head()) 
        
        return 0