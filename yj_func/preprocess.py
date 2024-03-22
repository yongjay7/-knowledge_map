
import pandas as pd 
import streamlit as st

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
