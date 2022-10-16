import pandas as pd
import numpy as np
import plotly.express as px  # pip install plotly-express
import streamlit as st # pip install streamlit
import openpyxl

st.set_page_config(page_title="People Analytics Twitter Influencers", page_icon=":chart_with_upwards_trend:", layout="wide")

header = st.container()
summary = st.container()
graph = st.container()

with header:
    st.title(":chart_with_upwards_trend: People Analytics Twitter Influencers")
    st.markdown("##")
    st.markdown("""---""")

with summary:
    user_activity = pd.read_excel('User activity.xlsx')
    users = round(user_activity['User name'].count(), 0)
    tweets = round(user_activity['Nº of Tweets'].sum(), 0)
    followers = round(user_activity['Followers'].mean(), 0)

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader(":mega: Nº of Users:")
        st.subheader(f"{users}")
        st.markdown("##")
        st.subheader(":dart: Total Nº of Tweets:")
        st.subheader(f"{ tweets}")
        st.markdown("##")
        st.markdown("""---""")

with graph:
    top_influencers = px.bar(user_activity[user_activity['Followers']>user_activity['Followers'].mean()].sort_values(by='Followers'), x='Followers', y='User name', orientation='h')
    left_column, middle_column, right_column = st.columns(3)
    with left_column:    
        st.subheader("Top Followed Users:")        
        st.plotly_chart(top_influencers)

st.markdown("""---""")

passive_audience = px.bar(user_activity[user_activity['Retweets received']>user_activity['Retweets received'].mean()].sort_values(by='Retweets received'), x='Retweets received', y='User name', orientation='h')

relevance_matrix = px.scatter(
    user_activity, y='Retweets received', x='Followers', hover_data=['User name'])

network = px.scatter(
    user_activity, y='Active network', x='Passive network', hover_data=['User name'])

left_column, right_column = st.columns(2)
with left_column:
    st.subheader('User Relevance Matrix')
    st.plotly_chart(relevance_matrix, use_container_width=True)

with right_column:
    st.subheader('User Network Analysis')
    st.plotly_chart(network, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
