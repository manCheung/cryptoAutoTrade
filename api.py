import time

import requests
import json
import config

headers = {"Content-Type": "application/json", "Content-Length": "16", 'Accept': '*/*'}
end_point = ""


def get_target_coins(minute, risingPercentage):
    body = {
        "minute": minute,
        "risingPercentage": risingPercentage
    }

    target_coins_rs = requests.post(end_point + "/target_coins", headers=headers, data=json.dumps(body))
    if target_coins_rs.status_code == 200:
        return target_coins_rs.json()['message']

    return []


def check_is_keep_rising(symbol_id, minute):
    body = {
        "minute": minute,
        "symbol_id": symbol_id
    }

    is_keep_rising_rs = requests.post(end_point + "/is_keep_rising", headers=headers, data=json.dumps(body))
    print(is_keep_rising_rs.json())
    if is_keep_rising_rs.status_code == 200:
        return is_keep_rising_rs.json()['isKeepRising']

    return False


def insert_history(access_token, symbol_id, amount, address, current_price, action_type, gas, gas_price):
    insert_headers = {
        "Content-Type": "application/json",
        "Content-Length": "16",
        "Accept": "*/*",
        'Authorization': 'Bearer {}'.format(access_token)
    }

    body = {
        "symbol_id": symbol_id,
        "amount": amount,
        "address": address,
        "current_price": current_price,
        "action_type": action_type,
        "gas": gas,
        "gas_price": gas_price
    }

    insert_history_rs = requests.post(end_point + "/history", headers=insert_headers, data=json.dumps(body))
    if insert_history_rs.status_code == 200:
        return True

    return False


def insert_excluded_coins(access_token, symbol_id, address):
    insert_headers = {
        "Content-Type": "application/json",
        "Content-Length": "16",
        "Accept": "*/*",
        'Authorization': 'Bearer {}'.format(access_token)
    }

    body = {
        "symbol_id": symbol_id,
        "address": address
    }

    insert_history_rs = requests.post(end_point + "/excluded_coins", headers=insert_headers, data=json.dumps(body))
    if insert_history_rs.status_code == 200:
        return True

    return False


def get_token():
    body = {
        "project": config.project,
        "key": config.key,
        "version": config.version
    }

    token_rs = requests.post(end_point + "/token", headers=headers, data=json.dumps(body))
    if token_rs.status_code == 200:
        return token_rs.json()['token']

    return False


def get_address_by_symbol_id(symbol_id):
    url = 'https://api.coingecko.com/api/v3/coins/' + symbol_id
    coin_rs = requests.get(url)
    print(url)
    print(coin_rs.json())
    coin_info = coin_rs.json()

    if coin_info.get("platforms") is not None:
        return coin_rs.json()["platforms"]["binance-smart-chain"]

    return False


def get_pancake_price_by_address(address):
    url = 'https://deep-index.moralis.io/api/v2/erc20/' + address + '/price?chain=bsc'
    # url = 'https://api.pancakeswap.info/api/v2/tokens/' + address
    headers = {'X-API-Key': 'fGE9SywVjamuGltZLVjxhYJjsjpM7BLmATYVMzHd1PXe0hiQlC4EYbaK7yKDWJHT'}
    rs = requests.get(url, headers=headers)
    coin_info = rs.json()

    if coin_info.get("usdPrice") is not None:
        return float(format(float(coin_info['usdPrice']), '.5f'))

    return False


def insert_wallet(access_token, symbol_id, address, price, amount):
    insert_headers = {
        "Content-Type": "application/json",
        "Content-Length": "16",
        "Accept": "*/*",
        'Authorization': 'Bearer {}'.format(access_token)
    }

    body = {
        "symbol_id": symbol_id,
        "address": address,
        "price": price,
        "amount": amount
    }

    insert_wallet_rs = requests.post(end_point + "/wallet", headers=insert_headers, data=json.dumps(body))
    if insert_wallet_rs.status_code == 200:
        return True

    return False


def get_wallet(access_token):
    wallet_headers = {
        "Content-Type": "application/json",
        'Authorization': 'Bearer {}'.format(access_token)
    }

    wallet_rs = requests.get(end_point + "/wallet", headers=wallet_headers)
    if wallet_rs.status_code == 200:
        return wallet_rs.json()['message']

    return []


def delete_wallet(access_token, symbol_id):
    wallet_headers = {
        "Content-Type": "application/json",
        'Authorization': 'Bearer {}'.format(access_token)
    }

    body = {
        "symbol_id": symbol_id
    }

    wallet_rs = requests.delete(end_point + "/wallet", headers=wallet_headers, data=json.dumps(body))
    if wallet_rs.status_code == 200:
        return True

    return []


def check_price_avg(symbol_id, minute):
    body = {
        "symbol_id": symbol_id,
        "minute": minute
    }

    price_avg_rs = requests.post(end_point + "/sma", headers=headers, data=json.dumps(body))
    print(price_avg_rs.json())
    if price_avg_rs.status_code == 200:
        return price_avg_rs.json()['avg']

    return False


def check_price_sd(symbol_id, minute):
    body = {
        "symbol_id": symbol_id,
        "minute": minute
    }

    price_sd_rs = requests.post(end_point + "/sd", headers=headers, data=json.dumps(body))
    print(price_sd_rs.json())
    if price_sd_rs.status_code == 200:
        return price_sd_rs.json()['stddev']

    return False


def check_transaction_status(tx):
    # TODO
    # status 0 = fail
    # 1 = success
    url = "https://api.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash=" + tx + "&apikey=GH6XKEAI6PKUZ1T9KVQ9V5UA1AUQITKDQR"
    print(url)

    while True:
        status_rs = requests.get(url)
        if status_rs.status_code == 200:
            if status_rs.json()['result']['status'] != "":
                return status_rs.json()['result']['status']

            time.sleep(2)


def get_abi(contract_address):
    url_scan = "https://api.bscscan.com/api?module=contract&action=getabi&address=" + str(contract_address) + "&apikey=2KBITXQRRN678CF8QY9PNSNIJI4JC7KC9T"
    r = requests.get(url=url_scan)
    response = r.json()
    # abi = json.loads(response["result"])
    return response["result"]
