import pandas as pd
import numpy as np
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


# 노드 클릭 콜백 함수
def on_node_click(event):
    if event["type"] == "Node":
        selected_node.write(f"You clicked node {event['data']['id']}")
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
    #side_df_D= 

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

        #""" 선택한 학년의 대주제(A) 코드 및 코드 설명 데이터 생성 과정 start """
        # 대주제 sheet와 매핑 가능한 데이터를 생성하는 과정
        # select_grade_df 에서 학교급(E)+학년(4)+교과(MATH)+대주제(A03) 스트링 데이터를 합하여 A_code를 생성
        # A_code = 'E4MATHA03' 
        select_grade_df['A_code'] = select_grade_df['학교급'].map(str)+select_grade_df['학년'].map(str)+select_grade_df['교과'].map(str)+select_grade_df['대주제'].map(str)

        # 생성한 A_code의 중복된 데이터를 제거하는 과정
        # A_code_unique = A_code 고유값
        A_code_unique = pd.DataFrame(select_grade_df['A_code'].unique(), columns=['대주제'])
        
        # A_code_unique와 side_df_A(대주제 sheet)를 merge하는 과정 
        # A_code_merge = 대주제 코드, 대주제 코드 설명 구조
        A_code_merge = pd.merge(A_code_unique,  side_df_A, on="대주제", how='left') 
        #""" 선택한 학년의 대주제(A) 코드 및 코드 설명 데이터 생성 과정 end """


        #""" 선택한 학년의 중주제(B) 코드 및 코드 설명 데이터 생성 과정 start """
        # 대주제(A) sheet와 중주제(B) sheet의 매핑 가능한 데이터를 생성하는 과정
        # 'E4MATHA03B01' → 'E4MATHA03' 
        # side_df_B['대주제'] = 'E4MATHA03'         
        side_df_B['대주제'] = side_df_B['중주제'].str.slice(start=0, stop=8)
        
        # A_code_merge(대주제 코드)와 side_df_B(중주제 코드)를 merge하는 과정 
        # B_code_merge = 대주제 코드, 대주제 코드 설명, 
        #                중주제 코드, 중주제 코드 설명 구조      
        B_code_merge = pd.merge(A_code_merge,  side_df_B, on="대주제", how='left') 
        #st.write(B_code_merge)
        #""" 선택한 학년의 중주제(B) 코드 및 코드 설명 데이터 생성 과정 end """

        #""" 선택한 학년의 소주제(C) 코드 및 코드 설명 데이터 생성 과정 start """        
        side_df_C['중주제'] = side_df_C['소주제'].str.slice(start=0, stop=11)
        C_code_merge = pd.merge(B_code_merge,  side_df_C, on="중주제", how='left') 
        #""" 선택한 학년의 소주제(C) 코드 및 코드 설명 데이터 생성 과정 end """
        
        # with mid_layout[i]: 
        #     st.dataframe(select_grade_df.head())
        #     for j in range(len(A_code_merge)):
        #         st.button(A_code_merge['설명'].iloc[j])
    nodes = []
    edges = []
    
    C_code_merge_drop = C_code_merge.dropna(axis=0)
    for i in range(len(C_code_merge_drop)):
        
        node_id = C_code_merge_drop.iloc[i]['소주제']
        node_label = C_code_merge_drop.iloc[i]['설명']    

        nodes.append(Node(
            id=node_id, 
            label=node_label, 
            size=10, 
            shape="dot",
            color= '#eee',
            border= '#000',
        ))
    # st.write(C_code_merge_drop)
    # st.write(B_code_merge)
    # st.write(A_code_merge)
    for i in range(len(B_code_merge)):
        node_id = B_code_merge.iloc[i]['중주제']
        node_label = B_code_merge.iloc[i]['설명_y']        
        nodes.append(Node(
            id=node_id, 
            label=node_label, 
            size=15, 
            shape="square",
            color= '#fB7CE9',
            border= '#000',
        ))
        C_node = C_code_merge_drop[C_code_merge_drop['중주제'] == node_id]
        for j in range(len(C_node)):
            if isinstance(C_node.iloc[j]['소주제'], type(None)):
                continue
            edges.append(Edge(source=C_node.iloc[j]['중주제'], 
                #label="friend_of", 
                target=C_node.iloc[j]['소주제'], 
                # **kwargs
            )) 
                      
    for i in range(len(A_code_merge)):

        node_id = A_code_merge.iloc[i]['대주제']
        node_label = A_code_merge.iloc[i]['설명']
        nodes.append(Node(id=node_id, 
                   label=node_label, 
                   size=30, 
                   shape="dot",
                   font={'color': 'red'},
        )) 
        
        B_node = B_code_merge[B_code_merge['대주제'] == node_id]
        for j in range(len(B_node)):
                edges.append(Edge(source=B_node.iloc[j]['대주제'], 
                    #label="friend_of", 
                    target=B_node.iloc[j]['중주제'], 
                    # **kwargs
                )) 
             
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



    graph_col1, graph_col2 = st.columns([2, 1])
    with graph_col1:    
        graph = agraph(nodes=nodes, 
                            edges=edges, 
                            config=config)
    
    with graph_col2: 
        st.write(graph)
        st.write(side_df_D)
else :
    st.text('')    





# import streamlit as st
# from streamlit_agraph import agraph, Node, Config

# # 그래프 데이터 생성
# nodes = [
#     Node(id='A1', size=100),
#     Node(id='B1', size=200),
#     Node(id='C1', size=300)
# ]

# edges = []
# config = Config(width=1400,
#                 height=1500,
#                 directed=True, 
#                 physics=True, 
#                 #hierarchical=True,
#                 color="#eeeeee",
#                 )
# # 그래프 출력

# graph = agraph(nodes, edges, config)
# st.write(graph)


