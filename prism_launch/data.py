import pandas as pd
from constants import cols_dict


user_stats = '499224b4-30a6-43d7-80b9-3a019cbb1d3d'
deposits_bucket = 'b4953cda-a874-43fa-b78d-ceb0c1bfc3cf'
deposit_balance = '9e2e9587-0850-466a-8a59-4dda2e8337f3'
hourly_new_users = '65179a1e-fd70-43eb-a9e4-ce14b716c928'
wallet_age = 'fb964d4e-3e67-4662-b9b1-413262737bcb'
hourly_stats = '520fb3b6-a968-4742-bf0a-31cbb67b6b05'
prev_launches = '22bf0295-9733-46d6-ab98-1cb753552c6b'

cols_claim = {
    user_stats : ['DEPOSIT_AMOUNT', 'DEPOSIT_TXS', 'SENDER', 'WITHDRAWN_AMOUNT',
       'WITHDRAW_TXS'],
    deposits_bucket : ['BUCKET', 'N_USERS'],
    prev_launches : ['PARTICIPANTS', 'PARTICIPATE_TYPE', 'TYPE'],
    hourly_stats : ['DEPOSIT_AMOUNT', 'DEPOSIT_TX', 'DEP_USERS', 'HR', 'NET_AMOUNT',
       'TOT_TXS', 'TOT_USERS', 'WITH_AMOUNT', 'WITH_TX', 'WITH_USERS'],
    wallet_age : ['ADDRESS_COUNT', 'MIN_DATE'],
    deposit_balance: ['AMOUNT', 'AVG_BALANCE_USD', 'MAX_BALANCE_USD', 'N_TXS', 'SENDER'],
    hourly_new_users: ['NEW_USERS', 'TIME']
}

def claim(claim_hash):
    df_claim = pd.read_json(
        f"https://api.flipsidecrypto.com/api/v2/queries/{claim_hash}/data/latest",
        convert_dates=["BLOCK_TIMESTAMP"],
    )
    
    if(len(df_claim.columns)==0):
        return pd.DataFrame(columns = cols_claim[claim_hash])

    return df_claim


user_stats_df = claim(user_stats)
deposit_balance_df = claim(deposit_balance)
deposits_bucket_df = claim(deposits_bucket)
wallet_age_df = claim(wallet_age)
hourly_stats_df = claim(hourly_stats)
prev_launches_df = claim(prev_launches)

user_stats_df['DEPOSIT_NET'] = user_stats_df.DEPOSIT_AMOUNT - user_stats_df.WITHDRAWN_AMOUNT
top_depositors = user_stats_df.sort_values(by='DEPOSIT_NET', ascending=False).head(5)[['SENDER','DEPOSIT_NET']]\
             .set_index('SENDER').rename(columns=cols_dict)

hourly_new_users_df = claim(hourly_new_users)
hourly_new_users_df['cumsum_new_users'] = hourly_new_users_df.sort_values(by='TIME').NEW_USERS.cumsum()
df = hourly_new_users_df.sort_values(by='TIME')
index = df.index
if(len(index)>1):
    i = -2
    next_last_users = df.loc[index[i]].cumsum_new_users
else:
    next_last_users = 0
hourly_new_users_df = hourly_new_users_df.rename(columns=cols_dict)


wallet_age_df = wallet_age_df.rename(columns=cols_dict)


hourly_stats_df['cumsum_ust'] = hourly_stats_df.sort_values(by='HR').NET_AMOUNT.cumsum()
hourly_stats_df['cumsum_txs'] = hourly_stats_df.sort_values(by='HR').TOT_TXS.cumsum()
df = hourly_stats_df.sort_values(by='HR')
index = df.index
if(len(index)>1):
    i = -2
    next_last_ust = df.loc[index[i]].cumsum_ust
    next_last_txs = df.loc[index[i]].cumsum_txs
else:
    i = 0
    next_last_ust = 0
    next_last_txs = 0
hourly_stats_df = hourly_stats_df.rename(columns=cols_dict)


n_txs = user_stats_df.DEPOSIT_TXS.sum() + user_stats_df.WITHDRAW_TXS.sum()
n_users = user_stats_df.SENDER.nunique()
tot_deposits = int(user_stats_df.DEPOSIT_AMOUNT.sum() - user_stats_df.WITHDRAWN_AMOUNT.sum())


prev_launches_df = prev_launches_df.rename(columns=cols_dict)

deposit_balance_df = deposit_balance_df.rename(columns=cols_dict)
deposits_bucket_df['bucket_name']=deposits_bucket_df.BUCKET.map({0:'-$0',1:'$0-$10',2:'$10-$100',3:'$100-$1k',4:'$1k-$10k',
                                5:'$10k-$100k',6:'$100k-$1m',7:'$1m-'})
deposits_bucket_df.sort_values(by='BUCKET')

dates_to_mark = pd.DataFrame([
['2021-03-04', '2021-03-11',120,'Anchor launch'],
['2021-09-24', '2021-10-01',120,'Columbus 5'],
['2021-12-12', '2021-12-19',120,'Astroport launch'], 
['2022-01-17', '2022-01-24',120,'Prism launch']], 
columns=['text_date','date','height','text']
)