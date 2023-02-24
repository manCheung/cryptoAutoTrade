from datetime import datetime
import time

import config
import trade
from web3 import Web3
import api
import pytz
import sys

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

# pancakeswap router abi
pan_abi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
contract = web3.eth.contract(address=config.router_address, abi=pan_abi)

pancake_factory_v2_address = ''
pancake_factory_v2_abi = api.get_abi(pancake_factory_v2_address)
pancake_factory_v2 = web3.toChecksumAddress(pancake_factory_v2_address)
factory_contract = web3.eth.contract(address=pancake_factory_v2, abi=pancake_factory_v2_abi)

nonce = web3.eth.getTransactionCount(config.sender_address)


def buy_process(pass_nonce):
    token = api.get_token()
    target_coins_rs_10 = api.get_target_coins(minute=10, risingPercentage=10)
    target_coins_rs_9 = api.get_target_coins(minute=9, risingPercentage=10)
    target_coins_rs_8 = api.get_target_coins(minute=8, risingPercentage=10)
    target_coins_rs_7 = api.get_target_coins(minute=7, risingPercentage=10)
    target_coins_rs_6 = api.get_target_coins(minute=6, risingPercentage=10)
    target_coins_rs_5 = api.get_target_coins(minute=5, risingPercentage=10)
    target_coins_rs_4 = api.get_target_coins(minute=4, risingPercentage=10)
    target_coins_rs_3 = api.get_target_coins(minute=3, risingPercentage=10)
    target_coins_rs = target_coins_rs_3 + target_coins_rs_4 + target_coins_rs_5 + target_coins_rs_6 + target_coins_rs_7 + target_coins_rs_8 + target_coins_rs_9 + target_coins_rs_10
    for x in target_coins_rs:
        symbol_id = x['symbol_id']

        if api.check_is_keep_rising(symbol_id=symbol_id, minute=15):

            token_buy = api.get_address_by_symbol_id(symbol_id)

            if token_buy is not None:
                pancake_price = api.get_pancake_price_by_address(token_buy)

                balance = trade.round_down(pancake_price, 5)

                if pancake_price is not False and balance > 0:
                    current_balance = trade.check_current_trade_coin_balance(config.busd_address, web3)

                    if balance > 0:
                        amount = trade.get_amount(current_balance, pancake_price)

                        if trade.check_token_approval(web3, token_buy) == 0:
                            trade.approve(web3, token_buy)

                        try:
                            is_price_correct = trade.is_price_correct(web3, contract, current_balance, config.busd_address,
                                                                      token_buy)

                            if is_price_correct:

                                tx_token = trade.trade(
                                    web3=web3,
                                    contract=contract,
                                    nonce=pass_nonce,
                                    trade_amount=current_balance,
                                    token_spend=config.busd_address,
                                    token_buy=token_buy
                                )

                                status = api.check_transaction_status(tx_token)

                                if str(status) == '1':

                                    wallet_amount = trade.check_current_trade_coin_balance(token_buy, web3)
                                    print("wallet_amount: " + str(wallet_amount))
                                    api.insert_history(
                                        access_token=token,
                                        symbol_id=symbol_id,
                                        amount=float(wallet_amount),
                                        address=token_buy,
                                        current_price=pancake_price,
                                        action_type=1,
                                        gas=config.gas,
                                        gas_price=config.gas_price
                                    )

                                    api.insert_wallet(
                                        access_token=token,
                                        symbol_id=symbol_id,
                                        address=token_buy,
                                        price=pancake_price,
                                        amount=float(wallet_amount)
                                    )

                                    api.insert_excluded_coins(
                                        access_token=token,
                                        symbol_id=symbol_id,
                                        address=token_buy
                                    )
                                    print('trade completed! - ' + str(datetime.now(pytz.timezone('Asia/Hong_Kong'))))

                                elif str(status) == '0':
                                    print('trade failed! - ' + str(datetime.now(pytz.timezone('Asia/Hong_Kong'))))
                        except:
                            print("An exception occurred")

    time.sleep(60)


def buy(nonce):
    while True:
        # if trade.check_BNB(web3, 0.03):
        # print('bnb enough')
        buy_process(nonce)
        # else:
        # print('bnb not enough')
        # trade.buy_BNB(web3, contract, 12)
        # time.sleep(60)


def sell_process(pass_nonce, amount, token_spend, api_token, symbol_id, pancake_price):
    tx_token = trade.trade(
        web3=web3,
        contract=contract,
        nonce=pass_nonce,
        trade_amount=amount,
        token_spend=token_spend,
        token_buy=config.busd_address
    )

    status = api.check_transaction_status(tx_token)

    if str(status) == '1':

        api.insert_history(
            access_token=api_token,
            symbol_id=symbol_id,
            amount=amount,
            address=token_spend,
            current_price=pancake_price,
            action_type=2,
            gas=config.gas,
            gas_price=config.gas_price
        )

        api.delete_wallet(
            access_token=api_token,
            symbol_id=symbol_id
        )

        print('sell trade completed! - ' + str(datetime.now(pytz.timezone('Asia/Hong_Kong'))))

    elif str(status) == '0':
        print('sell trade failed! - ' + str(datetime.now(pytz.timezone('Asia/Hong_Kong'))))


def sell(pass_nonce):
    while True:
        token = api.get_token()
        wallet_rs = api.get_wallet(token)
        for x in wallet_rs:
            token_spend = x['address']
            price = x['price']
            symbol_id = x['symbol_id']
            amount = x['amount']
            buy_time = x['datetime']

            pancake_price = api.get_pancake_price_by_address(token_spend)

            bought_minute = trade.cal_minutes_diff(buy_time)

            situation1 = (pancake_price >= price * 1.2 or pancake_price <= price * 0.85)
            situation2 = ((bought_minute >= 180) and (pancake_price * 1.08 >= price or pancake_price <= price * 0.9))
            situation3 = ((bought_minute >= 360) and not price <= pancake_price)
            situation4 = (bought_minute >= 720)

            if situation1 or situation2 or situation3 or situation4:

                if not api.check_is_keep_rising(symbol_id, round(bought_minute)):

                    approved = trade.check_token_approval(web3, token_spend)

                    if approved > 0:

                        sell_process(
                            pass_nonce=pass_nonce,
                            amount=amount,
                            token_spend=token_spend,
                            api_token=token,
                            symbol_id=symbol_id,
                            pancake_price=pancake_price
                        )

                    else:
                        approve_tx = trade.approve(web3, token_spend)
                        status = api.check_transaction_status(approve_tx)
                        if str(status) == '1':
                            sell_process(
                                pass_nonce=pass_nonce,
                                amount=amount,
                                token_spend=token_spend,
                                api_token=token,
                                symbol_id=symbol_id,
                                pancake_price=pancake_price
                            )
                        else:
                            trade.approve(web3, token_spend)

        time.sleep(60)


if __name__ == '__main__':

    nonce = nonce + 1

    if len(sys.argv) == 1:
        buy(nonce)
    else:
        action = sys.argv[1]
        if action == 'buy':
            buy(nonce)
        else:
            sell(nonce)
