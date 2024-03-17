import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


from streamlit_agraph import agraph, Node, Edge, Config, TripleStore



SHEET_CODE = '최종 코딩 양식'
SHEET_L = '대주제(A)'
SHEET_M = '중주제(B)'
SHEET_S = '소주제(C)'
#SHEET_SPE = '대주제(C)'

df_code = pd.read_excel('./math_code.xlsx', sheet_name=SHEET_CODE)
df_l = pd.read_excel('./math_code.xlsx', sheet_name=SHEET_L)
df_m = pd.read_excel('./math_code.xlsx', sheet_name=SHEET_M)
df_s = pd.read_excel('./math_code.xlsx', sheet_name=SHEET_S)



grades = ["초등학생", "중학생", "고등학생"]
# 가로로 정렬
# col1, col2, col3 = st.columns(3)  # 3개의 컬럼 생성
# with col1:
#     button1 = st.button(grades[0])
# with col2:
#     button2 = st.button(grades[1])
# with col3:
#     button3 = st.button(grades[2])
genre = st.radio(
    "What's your favorite movie genre",
    grades,

)

st.write("You selected:", genre)
 
 
lists_es = ['3학년','4학년','5학년','6학년']
lists_ms = ['1학년','2학년','3학년']
lists_hs = ['1학년'] 
tt = {'초등학생': lists_es, 
      '중학생': lists_ms,
      '고등학생': lists_hs}   
nodes = []
edges = []
# node 를 정의하고
nodes.append( Node(id="Spiderman", 
                   label="Peter Parker", 
                   size=25, 
                   shape="circularImage",
                   image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png") 
            ) # includes **kwargs
nodes.append( Node(id="Captain_Marvel", 
                   size=25,
                   shape="circularImage",
                   image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png") 
            )
# edge 를 정의해서
edges.append( Edge(source="Captain_Marvel", 
                   label="friend_of", 
                   target="Spiderman", 
                   # **kwargs
                   ) 
            ) 

# config 와 함께
config = Config(width=750,
                height=950,
                directed=True, 
                physics=True, 
                hierarchical=True,
                # **kwargs
                )

# graph 를 그리면 끝!
return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

#ll = lists_es

# if button1:
#     st.write("초등")
#     ll = lists_es
# if button2:
#     st.write("중등")
#     ll = lists_ms
# if button3:
#     st.write("중등")
#     ll = lists_hs
    

selected_list = st.multiselect('여러개 선택 가능', tt[genre])

if len(selected_list) != 0:
    st.write(int(selected_list[0][:1]))
    st.dataframe(df_code[df_code['학년'] == int(selected_list[0][:1])].head())
else :
    st.text('')    

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


# = st.radio("학년", ["2", "3", "4"])

# 선택된 메뉴에 따라 다른 데이터 표시
if selected_menu == "수학":
    

    st.write("수학 데이터를 표시합니다.")
    st.dataframe(df_l.head()) 
    
elif selected_menu == "영어":
    st.write("영어 데이터를 표시합니다.")
    st.dataframe(df_m.head()) 
else:
    st.write("정보 데이터를 표시합니다.")
    st.dataframe(df_s.head()) 
    


