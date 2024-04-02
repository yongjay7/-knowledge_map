
import pandas as pd 
import streamlit as st

from data import curriculum_info as curri_info

def set_shcool_grade_preprocess(data, school, grade):

    SCHOOL_COL = '학교급'
    GRADE_COL = '학년'

    df = data[(data[SCHOOL_COL] == school) & (data[GRADE_COL] == grade)]
    
    #print(school+' '+grade+'학년 데이터를 추출합니다.')
    return df

def set_create_A_code(data, col_list):

    #""" 선택한 학년의 대주제(A) 코드 및 코드 설명 데이터 생성 과정 start """
    # 대주제 sheet와 매핑 가능한 데이터를 생성하는 과정
    # select_grade_df 에서 학교급(E)+학년(4)+교과(MATH)+대주제(A03) 스트링 데이터를 합하여 A_code를 생성
    # A_code = 'E4MATHA03' 

    # 초기 변수 셋팅 
    df = data[col_list[0]].map(str)
    for i, col_name in enumerate(col_list):
        if i == 0:
            continue
        df = df+data[col_name].map(str)

    print('대주제(A)코드를 생성합니다.')
    return df

def get_col_unique_value(data, col_name):

    df = pd.DataFrame(data.unique(), columns=[col_name])

    return df

def get_learning_separate_data(data, value, div):
    result_df = pd.DataFrame()
    DIV_COL = 'ID'
    if div == 'A':
        result_df = data[data[DIV_COL].str.slice(start=0, stop=8) == value]
    elif div == 'B':
        result_df = data[data[DIV_COL].str.slice(start=0, stop=11) == value]
    elif div == 'C':
        result_df = data[data[DIV_COL] == value]        
    
    return result_df

def show_achieve_standards_info(data, achieve_data):
    
    ACH_STANDARD_COL = ['ID', 'A_성취기준', 'B_성취기준', 'C_성취기준']
    ACH_STANDARD_COL_NAME = ['성취기준']
    
    pre_df = pd.DataFrame(data[ACH_STANDARD_COL].dropna(axis=1).iloc[:, 1].unique(), columns=ACH_STANDARD_COL_NAME)
    pre_df['성취기준'] = pre_df['성취기준'].str.strip()

    MERGE_COL = '성취기준'

    pre_ach_merge = pd.merge(pre_df, achieve_data, on=MERGE_COL)

    for ach_i in range(len(pre_ach_merge)):
        #st.write(ach_std_merge.iloc[ach_i]['성취기준'])
        st.markdown("###### "+pre_ach_merge.iloc[ach_i]['성취기준'])
        st.write(pre_ach_merge.iloc[ach_i]['설명'])
        st.write("")   


def get_math_achievement_standards(graph_code):

    main_code = curri_info.get_data_math(0)
    subA_code = curri_info.get_data_math('A')
    subB_code = curri_info.get_data_math('B')
    subC_code = curri_info.get_data_math('C')
    achi_code = curri_info.get_data_math('ACH')

    code_id_length = len(graph_code)

    A_length = 8
    B_length = 11
    C_length = 14

    achievement_standards_df = pd.DataFrame()
    ACH_STANDARD_COL = ['ID', 'A_성취기준', 'B_성취기준', 'C_성취기준']

    #st.write(side_df_D)

    if code_id_length == A_length:
        st.markdown("##### 클릭한 코드의 성취기준")
        #st.write(A_code_merge[A_code_merge['대주제'] == graph])

        # 선택한 graph의 대주제 데이터 가져오기  
        separate_df = get_learning_separate_data(main_code, graph_code, "A")
        show_achieve_standards_info(separate_df, achi_code)


    elif code_id_length == B_length:
        st.markdown("##### 클릭한 코드의 성취기준")
        #st.write(B_code_merge[B_code_merge['중주제'] == graph])

        # 선택한 graph의 대주제 데이터 가져오기  
        separate_df = get_learning_separate_data(main_code, graph_code, "B")
        show_achieve_standards_info(separate_df, achi_code)

    elif code_id_length == C_length:
        st.markdown("##### 클릭한 코드의 성취기준")
        #st.write(C_code_merge[C_code_merge['소주제'] == graph])

        # 선택한 graph의 대주제 데이터 가져오기  
        separate_df = get_learning_separate_data(main_code, graph_code, "C")
        show_achieve_standards_info(separate_df, achi_code)