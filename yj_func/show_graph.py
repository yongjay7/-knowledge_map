
import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore

from yj_func import preprocess as yj_pre
import math

#def graw_nodes(data):
SCH_LV_COLOR = {
    'E':['','','wheat', 'orange', 'tan', 'darkorange'] ,
    'M':['lightgreen', 'seagreen', 'darkgreen']  ,
    'H':['royalblue'] ,
}
    
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




    # for i in range(len(data)):     

    #     pre_code = data.iloc[i]['선수 학습']
    #     aft_code = data.iloc[i]['후속 학습']

    #     if pd.notna(pre_code):
            
    #         pre_code_list = pre_code.split(',')

    #         #st.write(pre_code_list)
    #         for j, code in enumerate(pre_code_list):
    #             st.write('--pre---')
    #             st.write('data is', data.iloc[j]['코드'])
    #             edges.append( Edge(source=code, 
    #             #label="friend_of",
    #             target=data.iloc[j]['코드'], 
    #             # **kwargs
    #             ) 
    #         )
            
    #     if pd.notna(aft_code):

    #         aft_code_list = aft_code.split(',')

    #         for j, code in enumerate(aft_code_list):
    #             st.write('--aft---')
    #             st.write('data is', data.iloc[j]['코드'])
    #             edges.append( Edge(source=data.iloc[j]['코드'], 
    #             #label="friend_of",
    #             target=code, 
    #             # **kwargs
    #             ) 
    #         )         








    # agraph(nodes=nodes, 
    #     edges=edges,
    #     config=config)
    
    return nodes, edges, config
    
    if agraph:
        st.write(agraph)
   # return nodes, edges, config


def say_hello(i):
   st.write('Hello, Streamlit!', i)
   
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


def get_subject_hierarchy_info(selected_menu, schlv_grade):

    if selected_menu == "수학":

        area_col = '영역'
        concept_col = '핵심개념'
        main_code_name = '코드'

        math_hry          = pd.read_excel('./data/math_rank_2022.xlsx')
        math_hry['학교급']  =  math_hry[main_code_name].str.slice(start=0, stop=1)
        math_hry['학년']  =  math_hry[main_code_name].str.slice(start=1, stop=2)

        math_lv_gr = get_school_grade_df(math_hry, schlv_grade)
        

        st.write(math_lv_gr)


        
        graph_info = get_math_graph_info(math_hry, math_lv_gr)

  
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
    
def get_subject_hierarchy_info_2(selected_menu, learning_area):
    st.write(learning_area)
    if selected_menu == "수학":

        area_col = '영역'
        concept_col = '핵심개념'
        main_code_name = '코드'

        math_hry           = pd.read_excel('./data/math_rank_2022.xlsx')
        math_hry['학교급']  =  math_hry[main_code_name].str.slice(start=0, stop=1)
        math_hry['학년']    =  math_hry[main_code_name].str.slice(start=1, stop=2)
        
        math_hry_area = math_hry[math_hry[area_col] == learning_area]
        
        graph_info = get_math_graph_info(math_hry, math_hry_area)

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


   
    elif selected_menu == "영어":
        st.write("영어 데이터를 표시합니다.")


        return 0
    
    else:
        st.write("정보 데이터를 표시합니다.")

        
        return 0
