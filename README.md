# Don't use v1.0.2 before, there are big bugs. 

# bitget_multiwallet_withdraw
Just for 阿彬168

## Give me a coffe 

only Polygon USDT 
```
0xDDaAE2FF362928986A103DA132a3771e15117DD5
```

## Description

Bitget 多地址提幣功能

## Getting Started
Go to [bitget](https://www.bitget.com/zh-CN/account/newapi) and get the api key, set multi-wallet addresses to address list.

### config.json
```
{
    "token": "ETH",
    "network": "ETH",
    "amount": 1,
    "random_amount":true,
    "delay": { "min": 3, "max": 5 },
    "key":"",
    "secret":"",
    "passphrase":""
}
```
1. edit token which you wana withdraw
2. run getTokenSetting.exe to check "chain" and "minWithdrawAmount"
3. edit "network" and "amount"(minWithdrawAmount)
4. random_amount true or false

### wallets.txt
```
0x9FedBBC14302838837284595504Ff15487A5ac85
0x3728814d34c3C271B276F7528A3370b2015C6C9E
```

## run withdraw.exe

## contact info

[telelgram](https://t.me/liiiztw)
[twitter](https://twitter.com/game_liiiz)

## Version History

* v1.0.1
    * add log version
    * fix log transfer amount
    * change max_amount_range precision
* v1
    * Initial Release

## License

GPL ( GNU General Public License )

## Acknowledgments

* [BitgetLimited/v3-bitget-api-sdk](https://github.com/BitgetLimited/v3-bitget-api-sdk/tree/master/bitget-python-sdk-api)
