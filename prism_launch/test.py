import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data

st.set_page_config(page_title="Prism Forge - Analytics",layout='wide')

cols_dict = {
    "DEPOSIT_AMOUNT":"Amount deposited",
    "DEPOSIT_TXS":"N° of deposit txs",
    "DEP_USERS":"N° of depositing users",
    "HR":"Time",
    "NET_AMOUNT":"Net amount deposited",
    "TOT_TXS":"N° of txs",
    "TOT_USERS":"N° of users",
    "WITH_AMOUNT":"Withdrawn amount",
    "WITH_TXS":"N° of withdraw txs",
    "WITH_USERS":"N° of withdrawing users",
    'AMOUNT':'Amount deposited (UST)',
    'AVG_BALANCE_USD':'Average balance in the last 30 days (UST)',
    'N_TXS':'N° of txs',
    'SENDER':'User address',
    'N_USERS':'N° of users',
    'bucket_name':'Deposit range'
}

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def claim(claim_hash):
    # load claims into df
    df_claim = pd.read_json(
        f"https://api.flipsidecrypto.com/api/v2/queries/{claim_hash}/data/latest",
        convert_dates=["BLOCK_TIMESTAMP"],
    )

    return df_claim

user_stats = '499224b4-30a6-43d7-80b9-3a019cbb1d3d'
deposits_bucket = 'b4953cda-a874-43fa-b78d-ceb0c1bfc3cf'
deposit_balance = '9e2e9587-0850-466a-8a59-4dda2e8337f3'

user_stats_df = claim(user_stats)
deposit_balance_df = claim(deposit_balance)
deposits_bucket_df = claim(deposits_bucket)

hourly_stats = '520fb3b6-a968-4742-bf0a-31cbb67b6b05'
hourly_stats_df = claim(hourly_stats)

n_txs = user_stats_df.DEPOSIT_TXS.sum() + user_stats_df.WITHDRAW_TXS.sum()
n_users = user_stats_df.SENDER.nunique()
tot_deposits = int(user_stats_df.DEPOSIT_AMOUNT.sum() - user_stats_df.WITHDRAWN_AMOUNT.sum())


alt.renderers.set_embed_options(theme='dark')
st.title('Prism Forge - Phase 1')
st.text('')

col1, col2, col3, col4, col5 = st.columns([1,2,2,2,2])

with col2:
    st.metric(label="Total UST deposited", value=f"${int(tot_deposits/1000)}k", delta=+1765)

with col3:
    st.metric(label="Users", value=n_users, delta=123,
     delta_color="off")
    
with col4:
    st.metric(label="Transactions", value=n_txs, delta=57,
     delta_color="off")

with col5:
    st.metric(label="Estimated price", value=f"$2.5", delta=0.57,delta_color="off")
####
hourly_stats_df = hourly_stats_df.rename(columns=cols_dict)
col1, col2 = st.columns(2)
with col1:
    st.subheader('Transactions over time')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    c = alt.Chart(hourly_stats_df).mark_bar().encode(
        x=alt.X(cols_dict['HR']+':T', axis=alt.Axis(
                            tickCount=10, labelAngle=0, tickBand = 'center')),
        y=cols_dict['TOT_TXS'],
        tooltip=[cols_dict['TOT_TXS']]
    ).configure_mark(
        color='#ffde85'
    ).configure_view(strokeOpacity=0)
    st.altair_chart(c, use_container_width=True)
with col2:
    st.subheader('Users over time')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    c = alt.Chart(hourly_stats_df).mark_bar().encode(
        x=alt.X(cols_dict['HR']+':T', axis=alt.Axis(tickCount=10, 
                                                    labelAngle=0, tickBand = 'center')),
        y=cols_dict['TOT_USERS'],
        tooltip=[cols_dict['TOT_USERS']]
    ).configure_mark(
        color='#fab0ba'
    ).configure_view(strokeOpacity=0)
    st.altair_chart(c, use_container_width=True)
####
hourly_stats_df = hourly_stats_df.rename(columns=cols_dict)
col1, col2 = st.columns(2)
with col1:
    st.subheader('User deposits distribution')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    deposits_bucket_df['bucket_name']=deposits_bucket_df.BUCKET.map({0:'-$0',1:'$0-$10',2:'$10-$100',3:'$100-$1k',4:'$1k-$10k',
                                5:'$10k-$100k',6:'$100k-$1m',7:'$1m-'})
    deposits_bucket_df.sort_values(by='BUCKET')
    c = alt.Chart(deposits_bucket_df.rename(columns=cols_dict).sort_values(by='BUCKET')).mark_bar().encode(
        y=alt.X(cols_dict['bucket_name'], sort=alt.EncodingSortField(order='ascending')),
        x=cols_dict['N_USERS'],
        tooltip=[cols_dict['bucket_name'],cols_dict['N_USERS']]
    ).configure_mark(
        color='#fab0ba'
    ).properties(height=300).configure_axisX(
        labelAngle=0
    ).configure_view(strokeOpacity=0)
    st.altair_chart(c, use_container_width=True)
with col2:
    st.subheader('N° of transactions per wallet')
    st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
    df = user_stats_df.rename(columns=cols_dict)[cols_dict['DEPOSIT_TXS']]\
        .value_counts().sort_index().reset_index().rename(columns={'index':cols_dict['DEPOSIT_TXS'],cols_dict['DEPOSIT_TXS']:'N° of users'})
    print(df.columns)
    c = alt.Chart(df).mark_line(point = True).encode(
        y='N° of users',
        x=cols_dict['DEPOSIT_TXS'],
        tooltip=['N° of users',cols_dict['DEPOSIT_TXS']]
    )
    st.altair_chart(c, use_container_width=True)
####
####
prev_launches = '22bf0295-9733-46d6-ab98-1cb753552c6b'
prev_launches_df = claim(prev_launches) 
st.subheader('User participation previous launches')
st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
c = alt.Chart(prev_launches_df).mark_bar().encode(
    x=alt.X('TYPE', axis=alt.Axis(labelAngle=0, tickBand = 'center')),
    y='PARTICIPANTS',
    color=alt.Color('PARTICIPATE_TYPE',legend=alt.Legend(
        orient='none',
        padding=10,
        legendY=-10,
        direction='horizontal')),
    tooltip=['TYPE','PARTICIPANTS','PARTICIPATE_TYPE']
).properties(height=400).configure_axisX(
    labelAngle=-10
).configure_view(strokeOpacity=0)
st.altair_chart(c, use_container_width=True)
####
st.subheader('Deposit distribution per balance')
st.markdown("""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.""")
df = deposit_balance_df.rename(columns=cols_dict)
c =alt.Chart(df.head(5000)).mark_point().encode(
  y=cols_dict['AMOUNT'],
  x=cols_dict['AVG_BALANCE_USD'],
  color=alt.Color(cols_dict['N_TXS'],
          scale=alt.Scale(scheme='yelloworangered')),
  tooltip=[cols_dict['SENDER'], cols_dict['AMOUNT'],
           cols_dict['AVG_BALANCE_USD'],
          cols_dict['N_TXS']]
).interactive()
st.altair_chart(c, use_container_width=True)
###