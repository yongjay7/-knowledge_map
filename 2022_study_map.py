import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from data import curriculum_info as curri_info
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore

st.set_page_config(layout="wide")


main_df = pd.DataFrame() # 코드 정보
side_df_A = pd.DataFrame() # 대주제 정보
side_df_B = pd.DataFrame() # 중주제 정보
side_df_C = pd.DataFrame() # 소주제 정보
side_df_D = pd.DataFrame() # 성취기준 정보

## 사이드바 코드 시작 ##
# 메뉴 항목 생성
with st.sidebar:
    selected_menu = option_menu("과목 선택", ["수학", "영어", "정보"],
                                icons=['bi bi-plus-slash-minus', 'bi bi-alphabet-uppercase', 'bi bi-laptop'],
                                menu_icon="bi bi-book", default_index=0,
                                styles={
                                    "container": {"padding": "4!important",  "background-color": "#fafafa", "font-weight": "bold"},
                                    "icon": {"color": "black", "font-size": "25px"},
                                    "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px",
                                                "--hover-color": "#fafafa"},
                                    "nav-link-selected": {"background-color": "#08c7b4"},
                                })

# 선택된 메뉴에 따라 다른 데이터 표시 ***헤더 뷰 정보***
if selected_menu == "수학":
    st.markdown("##### 수학 데이터를 표시합니다.")
    main_df = curri_info.get_data_math(0)
    side_df_A = curri_info.get_data_math('A')
    side_df_B = curri_info.get_data_math('B')
    side_df_C = curri_info.get_data_math('C')

    label_text = "수학과목 코드 정보"
    with st.expander(label=label_text, expanded=True):
        st.dataframe(main_df) 
    
elif selected_menu == "영어":
    st.write("영어 데이터를 표시합니다.")
    df = curri_info.get_data_english(0)
    st.dataframe(df.head()) 
else:
    st.write("정보 데이터를 표시합니다.")
    st.dataframe(df_s.head()) 
## 사이드바 코드 끝 ##


## *** 학교급 및 학년 뷰 정보***
es_grade = ['3학년','4학년','5학년','6학년']
ms_grade = ['1학년','2학년','3학년']
hs_grade = ['1학년'] 
school_info = {'초등학생': es_grade, 
               '중학생': ms_grade,
               '고등학생': hs_grade}   


st.markdown("##### 학교급, 학년도별 주제를 확인합니다.")
col1, col2 = st.columns([1, 3])
with col1:    
    school_lv = ["초등학생", "중학생", "고등학생"]
    school_lv_choice = st.radio(
        "학교급 선택",
        school_lv,
)
with col2: 
    selected_list = st.multiselect('학년선택', school_info[school_lv_choice])
## *** 학교급 및 학년 뷰 정보***


if len(selected_list) != 0:
    
    # 선택한 학년의 개수를 저장합니다.
    list_len = len(selected_list) 

    # 선택한 학년 개수에 따라 레이아웃 영역을 생성하기 위한 변수를 선언합니다. 
    mid_layout_col = [] 
    
    # 선택한 학년 개수에 따라 레이아웃을 그리기 위한 기본 정보를 셋팅합니다. 
    for i in range(list_len):
        mid_layout_col.append(1)

    #st.write(mid_layout_col)
    # 선택한 학년 개수에 따라 레이아웃을 그립니다.
    mid_layout = st.columns(mid_layout_col)

    # 학교급 정보를 가져오기 위해 선택한 학교급을 데이터 변수로 매핑하는 데이터를 생성합니다. 
    school_data_info = {
        '초등학생': 'E', 
        '중학생': 'M',
        '고등학생': 'H' 
    }

    ## 선택된 학년의 정보를 출력 
    for i in range(list_len):

        # 선택한 학교급 및 학년 정보에 해당하는 데이터를 가져옵니다. 
        select_grade_df = main_df[(main_df['학교급'] == school_data_info[school_lv_choice]) & (main_df['학년'] == int(selected_list[i][:1]))]

        # 주제에 대한 설명 데이터를 가져오기 위해 select_grade_df의 각 코드를 연결하는 작업을 진행합니다. 
        select_grade_df['A_code'] = select_grade_df['학교급'].map(str)+select_grade_df['학년'].map(str)+select_grade_df['교과'].map(str)+select_grade_df['대주제'].map(str)

        # 연결 작업 후 대주제만을 확인하기 위해 대주제 고유값만 추출하는 과정을 진행합니다. 
        A_code_unique = pd.DataFrame(select_grade_df['A_code'].unique(), columns=['대주제'])
        
        # 대주제의 설명이 있는 side_df_A 병합하여 학교급 및 학년에 해당하는 정보를 확인할 수 있는 데이터를 생성합니다. 
        A_code_merge = pd.merge(A_code_unique,  side_df_A, on="대주제", how='left') 
        

        side_df_B['대주제'] = side_df_B['중주제'].str.slice(start=0, stop=8)
        B_code_merge = pd.merge(A_code_merge,  side_df_B, on="대주제", how='left') 
        st.write(B_code_merge)
        #B_code_merge = pd.merge(A_code_merge,  side_df_B, on="대주제", how='left') 

        with mid_layout[i]: 
            st.dataframe(select_grade_df.head())
            for j in range(len(A_code_merge)):
                st.button(A_code_merge['설명'].iloc[j])

    nodes = []
    edges = []
    st.write(A_code_merge.iloc[1]['대주제'])

    for i in range(len(B_code_merge)):
        nodes.append( Node(
            id=B_code_merge.iloc[i]['중주제'], 
            label=B_code_merge.iloc[i]['설명_y'], 
            size=20, 
            shape="square",
            color= '#fB7CE9',
            border= '#000',
        ))
    
    #for i in range(3):
    for i in range(len(A_code_merge)):

        node_id = A_code_merge.iloc[i]['대주제']
        node_label = A_code_merge.iloc[i]['설명']
        nodes.append( Node(id=node_id, 
                   label=node_label, 
                   size=30, 
                   shape="dot",
                   font={'color': 'red'},)

            ) # includes **kwargs
        
        B_node = B_code_merge[B_code_merge['대주제'] == node_id]

        for j in range(len(B_node)):
                
                edges.append( Edge(source=B_node.iloc[j]['대주제'], 
                    #label="friend_of", 
                    target=B_node.iloc[j]['중주제'], 
                    # **kwargs
                    ) 
             ) 
    for i in range(len(A_code_merge)-1):
                
        edges.append( Edge(source=A_code_merge.iloc[i]['대주제'], 
            #label="friend_of",
            target=A_code_merge.iloc[i+1]['대주제'], 
            # **kwargs
            ) 
        )

        
        
    # config 와 함께
    config = Config(width=1400,
                    height=1500,
                    directed=True, 
                    physics=True, 
                    #hierarchical=True,
                    color="#eeeeee",
                    )

    # graph 를 그리면 끝!
    return_value = agraph(nodes=nodes, 
                        edges=edges, 
                        config=config)

else :
    st.text('')    


