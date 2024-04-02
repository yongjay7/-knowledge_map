import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

from data import curriculum_info as curri_info
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore

from yj_func import sidebar as yj_side
from yj_func import header as yj_head
from yj_func import content_choice as yj_cont_cho
from yj_func import preprocess as yj_pre
from yj_func import show_graph as yj_grap

st.set_page_config(layout="wide")


main_df = pd.DataFrame() # 코드 정보
side_df_A = pd.DataFrame() # 대주제 정보
side_df_B = pd.DataFrame() # 중주제 정보
side_df_C = pd.DataFrame() # 소주제 정보
side_df_D = pd.DataFrame() # 성취기준 정보

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

# -------------------- 사이드바 영역 -------------------- #
selected_menu = yj_side.get_sidebar()


# --------------------   헤더 영역   -------------------- #
subject_data = yj_head.get_subjects_code(selected_menu)

tab1, tab2 = st.tabs(['대주제, 중주제, 소주제 관계보기', '학습위계로 보기'])


with tab2:
    # 학교급, 학년 데이터 가져오기 ex: ('초등학생', '3')
    school_grade2 = yj_cont_cho.get_selected_school_garde(2)
    
    # 학습 위계 데이터 가져오기 
    #Learning_hierarchy_data = 
    yj_grap.get_subject_hierarchy_info(selected_menu, school_grade2)
    

    # graph_col1, graph_col2 = st.columns([2, 1])


    # #with st.container(border=True):
    # math_rank = pd.read_excel('./data/math_rank_2022.xlsx')
    # #math_rank['학년'] =  math_rank['코드'].str.slice(start=1, stop=2)
    # #math_rank_df = math_rank[math_rank['학년'] == str(select_grade) ]

    # math_rank_num = math_rank['영역'].nunique()
    # col_num = [1] * math_rank_num
    # col_list = math_rank['영역'].unique()

    
    # btn_col_list = st.columns(col_num)
    
    
    # with btn_col_list[0]:
    #     st.button(col_list[0])
    # with btn_col_list[1]:
    #     st.button(col_list[1])   

    # st.write(math_rank)                     
    # st.write(col_list)                     
    # for i, name in enumerate(col_list):

    #     st.write(name)
    #     with st.container(border=True):
    #         math_rank_df_2 = math_rank[math_rank['영역'] == name]

    #         unique_unit = math_rank_df_2['핵심개념'].unique()
    #         for j, unit in enumerate(unique_unit):
    #             with st.container(border=True):
    #                 yj_grap.show_graph_2(math_rank_df_2[math_rank_df_2['핵심개념'] == unit])
    #                 #agraph(nodes=ddd[0], 
    #                 #edges=ddd[1],
    #                 #config=ddd[2])



    
    # # st.write("어떻게 보이나요1")
    # # st.write(math_rank_df)
    # # with st.container(border=True):

    # #     yj_grap.show_graph_2(math_rank_df[math_rank_df['핵심개념'] == '수의 체계'])

        
    # # with st.container(border=True):    

    #     yj_grap.show_graph_2(math_rank_df[math_rank_df['핵심개념'] == '수의 연산'])


    st.write("끝")    
with tab1:

    # -------------------- 콘텐츠 영역1 -------------------- #
    school_grade = yj_cont_cho.get_selected_school_garde(1)
    if len(school_grade[1]) != 0:
        
        # 선택한 학년의 개수를 저장합니다.
        list_len = len(school_grade[1]) 

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

            SCHOOL_COL = ['학교급']
            GRADE_COL = ['학년']

            # 메인코드 -- 매개변수 
            main_code = subject_data[0]
            archive_code = subject_data[4]

            select_school = school_data_info[school_grade[0]] # 00학교
            select_grade = int(school_grade[1])               # 3 

            # 학교급, 학년 데이터 추출하고 대주제 코드 생성하기
            MAP_COL = ['학교급','학년','교과','대주제']
            select_school_grade_df = yj_pre.set_shcool_grade_preprocess(main_code, select_school,  select_grade)
            select_school_grade_df['A_code'] = yj_pre.set_create_A_code(select_school_grade_df, MAP_COL)

            # 생성한 대주제 코드 중복 제거하고 대주제 코드와 merge 하기
            A_code_unique = yj_pre.get_col_unique_value(select_school_grade_df['A_code'], '대주제')
            A_code_merge = pd.merge(A_code_unique,  subject_data[1], on="대주제", how='left') 
            
            # 하위코드로부터 상위코드 추출하기        
            subject_data[2]['대주제'] = subject_data[2]['중주제'].str.slice(start=0, stop=8)
            subject_data[3]['중주제'] = subject_data[3]['소주제'].str.slice(start=0, stop=11)

            # 하위코드로부터 상위코드 추출하기
            A_code_merge = pd.merge(A_code_unique,  subject_data[1], on="대주제", how='left') 
            B_code_merge = pd.merge(A_code_merge,  subject_data[2], on="대주제", how='left') 
            C_code_merge = pd.merge(B_code_merge,  subject_data[3], on="중주제", how='left') 

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
            with st.container(border=True):
                graph = agraph(nodes=nodes, 
                                    edges=edges, 
                                    config=config)
        
        with graph_col2:
            with st.container(border=True):
                if graph:
                    code_id_length = len(graph)

                    A_length = 8
                    B_length = 11
                    C_length = 14

                    achievement_standards_df = pd.DataFrame()
                    ACH_STANDARD_COL = ['ID', 'A_성취기준', 'B_성취기준', 'C_성취기준']

                    #st.write(side_df_D)

                    if code_id_length == A_length:
                        st.markdown("##### 클릭한 코드의 성취기준")
                        st.write(A_code_merge[A_code_merge['대주제'] == graph])

                        # 선택한 graph의 대주제 데이터 가져오기  
                        separate_df = get_learning_separate_data(main_code, graph, "A")
                        show_achieve_standards_info(separate_df, archive_code)


                    elif code_id_length == B_length:
                        st.markdown("##### 클릭한 코드의 성취기준")
                        st.write(B_code_merge[B_code_merge['중주제'] == graph])

                        # 선택한 graph의 대주제 데이터 가져오기  
                        separate_df = get_learning_separate_data(main_code, graph, "B")
                        show_achieve_standards_info(separate_df, archive_code)

                    elif code_id_length == C_length:
                        st.markdown("##### 클릭한 코드의 성취기준")
                        st.write(C_code_merge[C_code_merge['소주제'] == graph])

                        # 선택한 graph의 대주제 데이터 가져오기  
                        separate_df = get_learning_separate_data(main_code, graph, "C")
                        show_achieve_standards_info(separate_df, archive_code)

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


