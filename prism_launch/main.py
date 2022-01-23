import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from constants import cols_dict
from charts import *
from data import tot_deposits,\
            n_users, n_txs,next_last_users, next_last_ust, next_last_txs

st.set_page_config(page_title="Prism Forge - Analytics",layout='wide')
alt.renderers.set_embed_options(theme='dark')
original_title = '<p style="font-size: 50px;">Prism Forge - Phase 1</p>'
st.markdown(original_title, unsafe_allow_html=True)
st.text('')

col1, col2, col3, col4, col5 = st.columns([1,2,2,2,2])

with col2:
    st.metric(label="Total UST deposited", value=f"${int(tot_deposits/1000)}k", delta=f"${int((tot_deposits-next_last_ust)/1000)}k")

with col3:
    st.metric(label="Unique users", value=n_users, delta=int(n_users-next_last_users),
     delta_color="off")
    
with col4:
    st.metric(label="Transactions", value=n_txs, delta=int(n_txs-next_last_txs),
     delta_color="off")

with col5:
    st.metric(label="Estimated price", value=f"${round(tot_deposits/70000000,2)}", delta=round(((tot_deposits-next_last_ust))/70000000,2),delta_color="off")
####
st.subheader('UST deposited over time')
st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
st.altair_chart(cum_ust_chart, use_container_width=True)
####
col1, col2 = st.columns(2)
with col1:
    st.subheader('Transactions over time')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    st.altair_chart(txs_over_time_chart, use_container_width=True)
with col2:
    st.subheader('Users over time')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    st.altair_chart(users_over_time_chart, use_container_width=True)
####
col1, col2 = st.columns(2)
with col1:
    st.subheader('User deposits distribution')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    st.altair_chart(users_dep_distr_chart, use_container_width=True)
with col2:
    st.subheader('N° of transactions per wallet')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    st.altair_chart(n_tx_wallet_chart, use_container_width=True)
####
st.subheader('User participation previous launches')
st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
st.altair_chart(user_part_prev_launches_chart, use_container_width=True)
####
st.subheader('Participants wallet age')
st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
st.altair_chart(wallet_age_chart, use_container_width=True)
####
st.subheader('Deposit distribution per balance')
st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
st.altair_chart(dep_dist_balance_chart, use_container_width=True)
###
st.markdown("Built with love for the 🌖 community by [IncioMan](https://twitter.com/IncioMan) and [sam](https://twitter.com/sem1d5) - with the support of [flipsidecrypto](https://flipsidecrypto.xyz/)")