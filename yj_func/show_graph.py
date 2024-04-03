
import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore

from yj_func import preprocess as yj_pre
from yj_func import content_choice as yj_cont_cho
from data import curriculum_info as curri_info

import math

#def graw_nodes(data):
SCH_LV_COLOR = {
    'E':['','','wheat', 'orange', 'tan', 'darkorange'] ,
    'M':['lightgreen', 'seagreen', 'darkgreen']  ,
    'H':['royalblue'] ,
}
    
SUBJECT_LIST = ['수학', '영어', '정보']

def graw_hierarchy_nodes(nodes, node_data, math_hry, unique_code):

    for i in range(len(node_data)):
        
        pre_code_list = node_data.iloc[i][0].split(',')   

        for j in range(len(pre_code_list)):
            
            node_id = pre_code_list[j]
            node_id = node_id.replace(" ", "")

            node_label = math_hry[math_hry['코드'] == node_id]['개념'].values[0]
            node_level = math_hry[math_hry['코드'] == node_id]['학교급'].values[0]
            node_grade = math_hry[math_hry['코드'] == node_id]['학년'].values[0]
            node_grade = int(node_grade)-1

            node_concept = math_hry[math_hry['코드'] == node_id]['핵심개념'].values[0]
            if node_id not in unique_code:
                nodes.append(Node(
                    id=node_id, 
                    label=node_label+'\n['+node_concept+']', 
                    size=25, 
                    shape="hexagon",
                    color= SCH_LV_COLOR[node_level][node_grade]
                    #font={'color': },
                ))      

    return nodes

def get_math_graph_info(math_hry, math_lv_gr):
    
    shapes ={
        0: 'diamond', 
        1: 'dot', 
        2: 'star', 
        3: 'triangle', 
        4: 'triangleDown', 
        5: 'square', 
        6: 'hexagon',
        7: 'icon'
    }
    
    nodes = []  
    edges = []
    
    node_pre = pd.DataFrame(math_lv_gr['선수 학습'].unique()).dropna()
    node_aft = pd.DataFrame(math_lv_gr['후속 학습'].unique()).dropna()


    # 핵심 개념별 for 문 
    
    concept_unique = math_lv_gr['핵심개념'].unique()
    concept_unique_code = math_lv_gr['코드'].unique().tolist()

    for n, name in enumerate(concept_unique):
        data_concept = math_lv_gr[math_lv_gr['핵심개념'] == name]

        for i in reversed(range(len(data_concept))):

            node_id = data_concept.iloc[i]['코드']
            node_label = data_concept.iloc[i]['개념']

            node_level = data_concept.iloc[i]['학교급']        
            node_grade = data_concept.iloc[i]['학년']
            node_grade = int(node_grade) - 1


            nodes.append(Node(
                id=node_id, 
                label=node_label+'\n['+name+']', 
                size=25, 
                shape=shapes[n],
                color= SCH_LV_COLOR[node_level][node_grade]
                #font={'color': '#B0B0B0'}
            ))

             
        for j in range(len(data_concept)-1, 0, -1):     

            edges.append(Edge(
                source=data_concept.iloc[j]['코드'], 
                target=data_concept.iloc[j-1]['코드'], 
                color='#000'
                ) 
            ) 
            
    nodes = graw_hierarchy_nodes(nodes, node_pre, math_hry, concept_unique_code)
    nodes = graw_hierarchy_nodes(nodes, node_aft, math_hry, concept_unique_code) 
    
    for n, name in enumerate(concept_unique):
        data_concept = math_lv_gr[math_lv_gr['핵심개념'] == name]
        
        for i in reversed(range(len(data_concept))):

            node_id = data_concept.iloc[i]['코드']       
            node_pre = data_concept.iloc[i]['선수 학습']    
            node_aft = data_concept.iloc[i]['후속 학습']  

            if pd.notna(node_pre):
                
                pre_code_list = node_pre.split(',')
                for p, code in enumerate(pre_code_list):
                    
                    edges.append( Edge(source=code, 
                    #label="friend_of",
                    target=node_id, 
                    color = 'red',
                    width = 2
                    ) 
                )
                
            if pd.notna(node_aft):

                aft_code_list = node_aft.split(',')

                for q, code in enumerate(aft_code_list):
                    edges.append( Edge(source=node_id, 
                    #label="friend_of",
                    target=code, 
                    color = 'red',
                    width = 2
                    ) 
                )   
      
    # 그래프 설정
    config = Config(width=1200,
            height=800,
            directed=True,  
            node={
                    'labelProperty': 'label',
                    'style': {"color": {'border': '#2B7CE9',}},
                    'renderLabel': True
                },        
            highlightColor="#F7A7A6"   
            )

    return nodes, edges, config
    
def show_math_graph(data):
    nodes = []  
    edges = []

    colors = {
        'E':['','','wheat', 'orange', 'tan', 'darkorange'] ,
        'M':['lightgreen', 'seagreen', 'darkgreen']  ,
        'H':['royalblue'] ,
    }

    config = Config(width=2100,
            height=1000,
            directed=True, 
            #physics=True, 
            hierarchical="shakeTowards",
            color="#eeeeee",
            )
    
    concept_unique = data['핵심개념'].unique()
    
    
    data=data[data['학교급'] == 'M']
    # 핵심 개념별 for 문 
    for n, name in enumerate(concept_unique):
        data_concept = data[data['핵심개념'] == name]

        for i in reversed(range(len(data_concept))):

            node_id = data_concept.iloc[i]['코드']
            node_label = data_concept.iloc[i]['개념']

            node_level = data_concept.iloc[i]['학교급']        
            node_grade = data_concept.iloc[i]['학년']
            node_grade = int(node_grade)

            if node_level == 'E':
                node_grade = node_grade-1
            elif node_level == 'M':
                node_grade = node_grade-1
            elif node_level == 'H':
                node_grade = node_grade-1



            nodes.append(Node(id=node_id, 
                    label=node_label, 
                    size=30, 
                    shape="dot",
                    color= colors[node_level][node_grade]
                    #font={'color': },
            )) 

        for j in range(len(data_concept)-1, 0, -1):     

            edges.append( Edge(source=data_concept.iloc[j]['코드'], 
                #label="friend_of",
                target=data_concept.iloc[j-1]['코드'], 
                # **kwargs
                ) 
            )

    for n, name in enumerate(concept_unique):
        data_concept = data[data['핵심개념'] == name]
        for i in reversed(range(len(data_concept))):

            node_id = data_concept.iloc[i]['코드']       
            node_pre = data_concept.iloc[i]['선수 학습']    
            node_aft = data_concept.iloc[i]['후속 학습']  

    
            st.write(node_pre, node_aft)
            #st.write('data is', pre_code, aft_code)
            if pd.notna(node_pre):
                
                pre_code_list = node_pre.split(',')
                for p, code in enumerate(pre_code_list):
                    
                    edges.append( Edge(source=code, 
                    #label="friend_of",
                    target=node_id, 
                    # **kwargs
                    ) 
                )
                
            if pd.notna(node_aft):

                aft_code_list = node_aft.split(',')

                for q, code in enumerate(aft_code_list):
                    edges.append( Edge(source=node_id, 
                    #label="friend_of",
                    target=code, 
                    # **kwargs
                    ) 
                )   


    return nodes, edges, config


   
def get_school_grade_df(data, schlv_grade):
    
    school_level_to_code ={ 
        "초등학생":"E",
        "중학생":"M",
        "고등학생":"H"                   
    }
    
    schlv_col = '학교급'
    grade_col = '학년'
        
    sc_lv = school_level_to_code[schlv_grade[0]]
    sc_gr = schlv_grade[1]    

    result_data = data[(data[schlv_col]== sc_lv) & (data[grade_col]== sc_gr)]
    
    return result_data


def show_subject_hierarchy_content_lv(selected_menu):
    # 학교급, 학년 데이터 가져오기 ex: ('초등학생', '3')
    schlv_grade = yj_cont_cho.get_selected_school_garde(2)


    if selected_menu == SUBJECT_LIST[0]:

        data_col_list = ['코드', '학교급', '학년', '영역']

        area_col = '영역'
        concept_col = '핵심개념'
        main_code_name = '코드'

        # 학습위계 데이터 가져오기
        math_learning_hierarchy_data = curri_info.get_data_math_learning_hierarchy()  
        math_learning_hierarchy_data[data_col_list[1]] =  math_learning_hierarchy_data[data_col_list[0]].str.slice(start=0, stop=1) #학교급 생성
        math_learning_hierarchy_data[data_col_list[2]] =  math_learning_hierarchy_data[data_col_list[0]].str.slice(start=1, stop=2) #학년 생성

        # 선택한 학교급 및 학년의 학습위계 데이터 가져오기
        math_learning_hierarchy_data_lv_gr = get_school_grade_df(math_learning_hierarchy_data, schlv_grade)
        
        # 그래프 정보 가져오기
        graph_info = get_math_graph_info(math_learning_hierarchy_data, math_learning_hierarchy_data_lv_gr)
  
        math_graph_col1, math_graph_col2 = st.columns([2, 1])
        with math_graph_col1:    
            with st.container(border=True):
                graph = agraph(nodes=graph_info[0], 
                        edges=graph_info[1], 
                        config=graph_info[2])  
        
        with math_graph_col2:
            with st.container(border=True):
                if graph:
                    st.write(graph)
                    yj_pre.get_math_achievement_standards(graph)

   
    elif selected_menu == "영어":
        st.write("영어 데이터를 표시합니다.")


        return 0
    
    else:
        st.write("정보 데이터를 표시합니다.")

        
        return 0
    

def show_subject_hierarchy_content_area(selected_subject):
   
    if selected_subject == SUBJECT_LIST[0]:

        data_col_list = ['코드', '학교급', '학년', '영역']
        
        # 학습위계 데이터 가져오기
        math_learning_hierarchy_data = curri_info.get_data_math_learning_hierarchy()  
        math_learning_hierarchy_data[data_col_list[1]] =  math_learning_hierarchy_data[data_col_list[0]].str.slice(start=0, stop=1) #학교급 생성
        math_learning_hierarchy_data[data_col_list[2]] =  math_learning_hierarchy_data[data_col_list[0]].str.slice(start=1, stop=2) #학년 생성     

        # 학습위계 데이터 영역(unique) 생성
        learning_area_list = math_learning_hierarchy_data[data_col_list[3]].unique() 

        # 학습위계 데이터 영역(unique) 선택
        with st.container(border=True):
            selected_learning_area = st.selectbox('영역선택', learning_area_list, key='learning_area')
       
        
        # 선택한 영역의 학습위계 데이터 추출
        math_learning_hierarchy_area = math_learning_hierarchy_data[math_learning_hierarchy_data[data_col_list[3]] == selected_learning_area]
        
        # 그래프 정보 가져오기
        graph_info = get_math_graph_info(math_learning_hierarchy_data, math_learning_hierarchy_area)

        math_graph2_col1, math_graph2_col2 = st.columns([2, 1])
        with math_graph2_col1:    
            with st.container(border=True):
                graph = agraph(nodes=graph_info[0], 
                        edges=graph_info[1], 
                        config=graph_info[2])  
        
        with math_graph2_col2:
            with st.container(border=True):
                if graph:
                    st.write(graph)
                    yj_pre.get_math_achievement_standards(graph)


   
    elif selected_subject == SUBJECT_LIST[1]:
        st.write("영어 데이터를 표시합니다.")


        return 0
    
    elif selected_subject == SUBJECT_LIST[2]:
        st.write("정보 데이터를 표시합니다.")

        
        return 0
