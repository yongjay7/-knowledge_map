import streamlit as st
from streamlit_option_menu import option_menu

def get_sidebar():

    subjects = ["수학", "영어", "정보"]
    subjects_icons = ['bi bi-plus-slash-minus', 'bi bi-alphabet-uppercase', 'bi bi-laptop']
    with st.sidebar:
        selected_menu = option_menu("과목 선택", subjects,
                                    icons=subjects_icons,
                                    menu_icon="bi bi-book", default_index=0,
                                    styles={
                                        "container": {"padding": "4!important",  "background-color": "#fafafa", "font-weight": "bold"},
                                        "icon": {"color": "black", "font-size": "25px"},
                                        "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px",
                                                    "--hover-color": "#fafafa"},
                                        "nav-link-selected": {"background-color": "#08c7b4"},
                                    })

    return selected_menu