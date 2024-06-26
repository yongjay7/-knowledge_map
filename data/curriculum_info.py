import pandas as pd
import streamlit as st



SHEET_L = '대주제(A)'
SHEET_M = '중주제(B)'
SHEET_S = '소주제(C)'
SHEET_ACH = '관련성취기준'

@st.cache_data
def get_data_math(sheet):
    SHEET_CODE = '최종 코딩 양식'
    file_name = './data/math_code_2022.xlsx'
    
    if sheet == 0:
        data = pd.read_excel(file_name, dtype='object', sheet_name=SHEET_CODE)
    elif sheet == 'A':
        data = pd.read_excel(file_name, sheet_name=SHEET_L)
    elif sheet == 'B':
        data = pd.read_excel(file_name, sheet_name=SHEET_M)       
    elif sheet == 'C':
        data = pd.read_excel(file_name, sheet_name=SHEET_S)        
    elif sheet == 'ACH':
        data = pd.read_excel(file_name, sheet_name=SHEET_ACH)   

    return data

@st.cache_data
def get_data_math_learning_hierarchy():

    file_name = './data/math_rank_2022.xlsx'

    data = pd.read_excel(file_name)

    return data


@st.cache_data
def get_data_english(sheet):
    SHEET_CODE = '코딩맵'
    file_name = './data/english_code_2022.xlsx'
    if sheet == 0:
        data = pd.read_excel(file_name, sheet_name=SHEET_CODE)
    elif sheet == 'A':
        data = pd.read_excel(file_name, sheet_name=SHEET_L)
    elif sheet == 'B':
        data = pd.read_excel(file_name, sheet_name=SHEET_M)       
    elif sheet == 'C':
        data = pd.read_excel(file_name, sheet_name=SHEET_S)        

    return data