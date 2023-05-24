# 載入設定
config_filepath = 'config.json'
address_filepath = 'wallets.txt'

import json
with open(config_filepath) as f:
    config_dict = json.load(f)
    config_dict['token'] = config_dict['token'].upper()
with open(address_filepath) as f:
    address_list = f.read().split()

import bitget.spot.account_api as account
import bitget.spot.public_api as public
accountApi = account.AccountApi(
    api_key=config_dict['key'],
    api_secret_key=config_dict['secret'],
    passphrase=config_dict['passphrase'],
    use_server_time=False, first=False)

publicApi = public.PublicApi(
    api_key=config_dict['key'],
    api_secret_key=config_dict['secret'],
    passphrase=config_dict['passphrase'],
    use_server_time=True, first=False)

try:
    import pandas as pd

    # 檢查餘額
    df_bal = pd.DataFrame(accountApi.assets()['data'])

    df_bal['Balance'] = df_bal['available'].astype(float)
    if len(df_bal.loc[df_bal['coinName']==config_dict['token'],])>0:
         bal = float(df_bal.loc[df_bal['coinName']==config_dict['token'],'Balance'].iloc[0])
    else:
        bal = 0
    print(f"初始餘額: {bal}")

    # 提幣訊息
    res_coin_info = [coin_info for coin_info in publicApi.currencies()['data'] if coin_info['coinName']==config_dict['token']]
    df_coin = pd.concat(
        [
            pd.DataFrame(res_coin_info[0])[['coinName']],
            pd.DataFrame(res_coin_info[0]['chains'])[['chain','minWithdrawAmount','withdrawFee']]
        ], axis=1
    )
    print(df_coin)
except Exception as msg:
    print(msg)
    pass
    
input('\npress "ENTER" to close.') 