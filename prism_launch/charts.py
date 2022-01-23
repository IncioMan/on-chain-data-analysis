import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from constants import cols_dict
from data import user_stats_df,hourly_stats_df, wallet_age_df, hourly_new_users_df,deposits_bucket_df,deposit_balance_df,prev_launches_df


txs_over_time_chart = alt.Chart(hourly_stats_df).mark_bar().encode(
    x=alt.X(cols_dict['HR']+':T', axis=alt.Axis(
                        tickCount=10, labelAngle=0, tickBand = 'center')),
    y=cols_dict['TOT_TXS'],
    tooltip=[cols_dict['HR']+':T',cols_dict['TOT_TXS']]
).configure_mark(
    color='#ffde85'
).configure_view(strokeOpacity=0)
####
users_over_time_chart = alt.Chart(hourly_new_users_df).mark_bar().encode(
    x=alt.X(cols_dict['TIME']+':T', axis=alt.Axis(tickCount=10, 
                                                labelAngle=0, tickBand = 'center')),
    y=cols_dict['cumsum_new_users'],
    tooltip=[cols_dict['TIME']+':T', cols_dict['cumsum_new_users']]
).configure_mark(
    color='#fab0ba'
).configure_view(strokeOpacity=0)
####
users_dep_distr_chart = alt.Chart(deposits_bucket_df.rename(columns=cols_dict).sort_values(by='BUCKET')).mark_bar().encode(
    y=alt.X(cols_dict['bucket_name'], sort=alt.EncodingSortField(order='ascending')),
    x=cols_dict['N_USERS'],
    tooltip=[cols_dict['bucket_name'],cols_dict['N_USERS']]
).configure_mark(
    color='#fab0ba'
).properties(height=300).configure_axisX(
    labelAngle=0
).configure_view(strokeOpacity=0)
####
cum_ust_chart = alt.Chart(hourly_stats_df.rename(columns=cols_dict)).mark_line(point=True).encode(
    x=alt.X(cols_dict['HR']+':T', sort=alt.EncodingSortField(order='ascending')),
    y=cols_dict['cumsum_ust'],
    tooltip=[cols_dict['HR']+':T',cols_dict['cumsum_ust']]
).configure_mark(
    color='#fab0ba'
).properties(width=700).configure_axisX(
    labelAngle=0
).configure_view(strokeOpacity=0)
####
df = user_stats_df.rename(columns=cols_dict)[cols_dict['DEPOSIT_TXS']]\
    .value_counts().sort_index().reset_index().rename(columns={'index':cols_dict['DEPOSIT_TXS'],cols_dict['DEPOSIT_TXS']:'N° of users'})
n_tx_wallet_chart = alt.Chart(df).mark_line(point = True).encode(
    y='N° of users',
    x=cols_dict['DEPOSIT_TXS'],
    tooltip=['N° of users',cols_dict['DEPOSIT_TXS']]
)
####
user_part_prev_launches_chart = alt.Chart(prev_launches_df).mark_bar().encode(
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
####
dep_dist_balance_chart =alt.Chart(deposit_balance_df.sample(n=5000, random_state=1)).mark_point().encode(
y=cols_dict['AMOUNT'],
x=cols_dict['AVG_BALANCE_USD'],
color=alt.Color(cols_dict['N_TXS'],
    scale=alt.Scale(scheme='yelloworangered')),
tooltip=[cols_dict['SENDER'], cols_dict['AMOUNT'],
    cols_dict['AVG_BALANCE_USD'],
    cols_dict['N_TXS']]
).interactive()
###
wallet_age_df = wallet_age_df.rename(columns=cols_dict)
wallet_age_chart = alt.Chart(wallet_age_df).mark_bar().encode(
    x=alt.X(cols_dict['MIN_DATE']+":T", axis=alt.Axis(tickCount=10, labelAngle=0)),
    y=cols_dict['ADDRESS_COUNT'],
    tooltip=[cols_dict['MIN_DATE']+":T",cols_dict['ADDRESS_COUNT']]
).configure_mark(
    color='#ffde85'
).configure_view(strokeOpacity=0)