import pandas as pd
from constants import cols_dict
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
hourly_stats_df = hourly_stats_df.rename(columns=cols_dict)

n_txs = user_stats_df.DEPOSIT_TXS.sum() + user_stats_df.WITHDRAW_TXS.sum()
n_users = user_stats_df.SENDER.nunique()
tot_deposits = int(user_stats_df.DEPOSIT_AMOUNT.sum() - user_stats_df.WITHDRAWN_AMOUNT.sum())

prev_launches = '22bf0295-9733-46d6-ab98-1cb753552c6b'
prev_launches_df = claim(prev_launches) 
deposit_balance_df = deposit_balance_df.rename(columns=cols_dict)
deposits_bucket_df['bucket_name']=deposits_bucket_df.BUCKET.map({0:'-$0',1:'$0-$10',2:'$10-$100',3:'$100-$1k',4:'$1k-$10k',
                                5:'$10k-$100k',6:'$100k-$1m',7:'$1m-'})
deposits_bucket_df.sort_values(by='BUCKET')
    