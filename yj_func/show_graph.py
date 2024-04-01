
import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore

import math

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

def get_subject_hierarchy_info(selected_menu):
    if selected_menu == "수학":

        area_col = '영역'
        concept_col = '핵심개념'
        main_code_name = '코드'

        math_hry          = pd.read_excel('./data/math_rank_2022.xlsx')
        math_hry['학교급']  =  math_hry[main_code_name].str.slice(start=0, stop=1)
        math_hry['학년']  =  math_hry[main_code_name].str.slice(start=1, stop=2)

        math_hry_area     = math_hry[area_col].unique()
        math_hry_area_num = math_hry[area_col].nunique()

        col_num = [1] * math_hry_area_num
        col_list = st.columns(col_num)

        btn_name =''
        for i, name in enumerate(math_hry_area):
            with col_list[i]:
                if st.button(name):
                    btn_name = name
                    #say_hello(i)

        graph_info = show_math_graph(math_hry)
        graph = agraph(nodes=graph_info[0], 
                edges=graph_info[1], 
                config=graph_info[2])    
        # for i, name in enumerate(math_hry_area):

        #     if btn_name == math_hry_area[i]:
        #         st.write(math_hry_area[i])

        #         with st.container(border=True):
        #             math_hry_one = math_hry[math_hry[area_col] == name]
        #             concept_unique = math_hry_one[concept_col].unique()

        #             for j, concept in enumerate(concept_unique):    
        #                 st.write(concept)
        #                 with st.container(border=True):
        #                     graph_info = show_math_graph(math_hry_one[math_hry_one[concept_col] == concept])
        #                     graph = agraph(nodes=graph_info[0], 
        #                             edges=graph_info[1], 
        #                             config=graph_info[2])
        #                     st.write(graph)
        #                     if graph:
        #                         st.write(graph)

        #                 # graph = agraph(nodes=nodes, 
        #                 #             edges=edges, 
        #                 #             config=config)
        
    elif selected_menu == "영어":
        st.write("영어 데이터를 표시합니다.")


        return 0
    
    else:
        st.write("정보 데이터를 표시합니다.")

        
        return 0