# 載入設定
import json
import os
config_filepath = 'config.json'
address_filepath = 'wallets.txt'

# 開啟設定
with open(config_filepath) as f:
    config_dict = json.load(f)
    config_dict['token'] = config_dict['token'].upper()
with open(address_filepath) as f:
    address_list = f.read().split()

# 亂數定義
if config_dict['random_amount']:
    max_amount_range = 100
else:
    max_amount_range = 0    


# 檢查log若存在就往下推一個版本
filename = 'log.csv'
counter = 0
while os.path.isfile(filename):
    counter += 1
    filename = f"log{str(counter).zfill(2)}.csv"



try:
    import pandas as pd
    import bitget.spot.account_api as account
    import bitget.spot.public_api as public
    import bitget.spot.wallet_api as wallet
    
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
    
    walletApi = wallet.WalletApi(
        api_key=config_dict['key'],
        api_secret_key=config_dict['secret'],
        passphrase=config_dict['passphrase'],
        use_server_time=True, first=False)

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
    minfee = float(df_coin.loc[(df_coin['coinName']==config_dict['token'])&(df_coin['chain']==config_dict['network']),'withdrawFee'].iloc[0])
    print(f"手續費: {minfee}")

    import time
    import random
    if bal >= (len(address_list)*(config_dict['amount']*(1+max_amount_range/10000)+minfee)):
        for address in address_list:

            ratio = (1+random.randint(0,max_amount_range)/10000)
            send_amount = str(config_dict['amount']*ratio)[:10]

            res_withdraw = walletApi.withdrawal(
                coin=config_dict['token'],
                chain=config_dict['network'],
                address=address,
                amount=send_amount,
                remark=None
            )
            

            try:
                pd.read_csv(filename)
            except FileNotFoundError:
                with open(filename, 'w') as f:
                    f.write("time,targetAddress,network,amount,token,fee\n")

            with open(filename, 'a') as f:
                f.write(f"{pd.to_datetime('now').ceil(freq='s')},{address},{config_dict['network']},{send_amount},{config_dict['token']},{minfee}\n")

            print(f"[{pd.to_datetime('now').ceil(freq='s')}] {address} {config_dict['network']}:{send_amount}{config_dict['token']} fee:{minfee}")
            
            delay = random.randint(config_dict['delay']['min'],config_dict['delay']['max'])
            for t in range(delay):
                print(f'waiting - {delay-t}s ', end="\r")
                time.sleep(1)
            
        # 檢查餘額
        df_bal = pd.DataFrame(accountApi.assets()['data'])
        df_bal['Balance'] = df_bal['available'].astype(float)
        if len(df_bal.loc[df_bal['coinName']==config_dict['token'],])>0:
             bal = float(df_bal.loc[df_bal['coinName']==config_dict['token'],'Balance'].iloc[0])
        else:
            bal = 0
        print(f"現在餘額: {bal}")
        
    else:
        print(f"餘額不足: {bal-(len(address_list)*(config_dict['amount']+minfee))}")

except Exception as msg:
    print(msg)
    pass

input('\npress "ENTER" to close.')
