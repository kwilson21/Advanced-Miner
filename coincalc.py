import calclog
import logging
import requests
import coin
import time
import json
import os
import sys
import multiprocessing
import concurrent.futures
from datetime import datetime
from tabulate import tabulate

calclog = logging.getLogger('calc')

class globalvars():
    se_prices = ''
    ts_prices = ''
    sx_prices = ''
    ct_prices = ''
    cb_prices = ''
    btc_price = ''
    algo_config_list = []
    coins = {}
    
def load_difficulty(url,name):
    new_num = ''
    difficulty_loaded = False

    if "crypto-coinz" in url:
        i=0
        while not difficulty_loaded:
            difficulty_loaded = False
            try:
                response = requests.get(url)
                txt = response.text
                num = txt.find("Difficulty:")
                for i in range(15):
                    if txt[num+19+i].isdigit() or txt[num+19+i] == '.':
                        new_num += txt[num+19+i]
                difficulty = float(new_num)
                difficulty_loaded = True
            except (requests.exceptions.HTTPError, ValueError) as err:
                #calclog.error("Error loading " + name + " difficuly. Retrying...")
                i+=1
            except:
                calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                difficulty = 0
                return difficulty, difficulty_loaded
            finally:
                if i == 3:
                    calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                    difficulty = 0
                    return difficulty, difficulty_loaded


    elif "fsight" in url:
        difficulty_loaded = False
        i=0
        while not difficulty_loaded:
            try:
                temp = requests.get(url).json()
                difficulty = float(temp["difficulty"])
                difficulty_loaded = True
            except (requests.exceptions.HTTPError, ValueError) as err:
                #calclog.error("Error loading " + name + " difficuly. Retrying...")
                i+=1
            except:
                calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                difficulty = 0
                return difficulty, difficulty_loaded
            finally:
                if i == 3:
                    calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                    difficulty = 0
                    return difficulty, difficulty_loaded
    
    elif "trezar" in url or "denarius" in url:
        i=0
        difficulty_loaded = False
        while not difficulty_loaded:
            try:
                temp = requests.get(url).json()
                difficulty = float(temp["proof-of-work"])
                difficulty_loaded = True
            except (requests.exceptions.HTTPError, ValueError) as err:
                #calclog.error("Error loading " + name + " difficuly. Retrying...")
                i+=1
            except:
                calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                difficulty = 0
                return difficulty, difficulty_loaded
            finally:
                if i == 3:
                    calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                    difficulty = 0
                    return difficulty, difficulty_loaded

    else:
        i=0
        difficulty_loaded = False
        while not difficulty_loaded:
            try:
                difficulty  = float(requests.get(url).text)
                difficulty_loaded = True
            except (requests.exceptions.HTTPError, ValueError) as err:
                #calclog.error("Error loading " + name + " difficuly. Retrying...")
                i+=1
            except:
                calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                difficulty = 0
                return difficulty, difficulty_loaded
            finally:
                if i == 3:
                    calclog.error("Could not load the difficulty for " + name + ". Skipping coin")
                    difficulty = 0
                    return difficulty, difficulty_loaded

    return difficulty, difficulty_loaded

def load_se_prices(se_prices):
    prices_loaded = False
    # Load the prices of coins on stocks exchange.
    while not prices_loaded:
        try:
            se_prices = requests.get('https://stocks.exchange/api2/prices').json()
            prices_loaded = True
        except (requests.exceptions.HTTPError, ValueError, ConnectionError) as err:
            prices_loaded = False
            calclog.error("Error loading prices from Stocks.Exchange api, trying again in 30 seconds...")
            time.sleep(30)
    return se_prices
            
def load_ts_prices(ts_prices):
    prices_loaded = False
    # Load prices from trade satoshi.
    while not prices_loaded:
        try:
            ts_prices = requests.get('https://tradesatoshi.com/api/public/getmarketsummaries').json()
            prices_loaded = True
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ValueError, ConnectionError) as err:
            prices_loaded = False
            calclog.error("Error loading prices from Trade Satoshi api, trying again in 30 seconds...")
            time.sleep(30)
    return ts_prices

def load_sx_prices(sx_prices):
    prices_loaded = False
    # Load prices from Southxchange.
    while not prices_loaded:
        try:
            sx_prices = requests.get('https://www.southxchange.com/api/prices').json()
            prices_loaded = True
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ValueError, ConnectionError) as err:
            prices_loaded = False
            calclog.error("Error loading prices from Southxchange api, trying again in 30 seconds...")
            time.sleep(30)
    return sx_prices

def load_ct_prices(ct_prices):
    prices_loaded = False
    # Load prices from Cryptopia.
    while not prices_loaded:
        try:
            ct_prices = requests.get('https://www.cryptopia.co.nz/api/GetMarkets').json()
            prices_loaded = True
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ValueError, ConnectionError) as err:
            prices_loaded = False
            calclog.error("Error loading prices from Cryptopia api, trying again in 30 seconds...")
            time.sleep(30)
    return ct_prices

def load_cb_prices(cb_prices):
    prices_loaded = False
    # Load prices from Crypto-bridge.
    while not prices_loaded:
        try:
            cb_prices = requests.get('https://api.crypto-bridge.org/api/v1/ticker').json()
            prices_loaded = True
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ValueError, ConnectionError) as err:
            prices_loaded = False
            calclog.error("Error loading prices from Crypto-bridge api, trying again in 30 seconds...")
            time.sleep(30)
    return cb_prices
        
def load_btc_price(btc_price):
    prices_loaded = False
    # Load the price of BTC from coinbase.
    while not prices_loaded:
        try:
            btc_price = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=BTC').json()
            prices_loaded = True
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ValueError, ConnectionError) as err:
            prices_loaded = False
            calclog.error("Error loading prices from Coinbase api, trying again in 30 seconds...")
            time.sleep(30)
    return btc_price

def add_se_prices(se_prices,coin_name):
    buy_price_se = 0.0
    # Add stocks exchange prices
    for i in range(len(se_prices)):
        if se_prices[i]['market_name'] == coin_name + '_BTC':
            try:
                buy_price_se = float(se_prices[i]['buy'])
            except TypeError:
                buy_price_se = 0.0
            break
    return buy_price_se

def add_ts_prices(ts_prices,coin_name):
    buy_price_ts = 0.0
    # Add trade satoshi exchange prices
    for i in range(len(ts_prices['result'])):
        if ts_prices['result'][i]['market'] == coin_name + '_BTC':
            try:
                buy_price_ts = float(ts_prices['result'][i]['last'])
            except TypeError:
                buy_price_ts = 0.0
            break
    return buy_price_ts
def add_sx_prices(sx_prices,coin_name):
    buy_price_sx = 0.0
    # Add Southxchange exchange prices
    for i in range(len(sx_prices)):
        if sx_prices[i]['Market'] == coin_name + '/BTC':
            try:
                buy_price_sx = float(sx_prices[i]['Last'])
            except TypeError:
                buy_price_sx = 0.0
            break
    return buy_price_sx

def add_ct_prices(ct_prices,coin_name):
    buy_price_ct = 0.0
    # Add Cryptopia exchange prices
    for i in range(len(ct_prices['Data'])):
        if ct_prices['Data'][i]['Label'] == coin_name + '/BTC':
            try:
                buy_price_ct = float(ct_prices['Data'][i]['LastPrice'])
            except TypeError:
                buy_price_ct = 0.0
            break
    return buy_price_ct

def add_cb_prices(cb_prices,coin_name):
    buy_price_cb = 0.0
    # Add Crypto-bridge exchange prices
    for i in range(len(cb_prices)):
        if cb_prices[i]['id'] == coin_name + '_BTC':
            try:
                buy_price_cb = float(cb_prices[i]['last'])
            except TypeError:
                buy_price_cb = 0.0
            break
    return buy_price_cb

def add_exchange_prices(coin_name):
    buy_price_se = 0.0
    buy_price_ts = 0.0
    buy_price_sx = 0.0
    buy_price_ct = 0.0
    buy_price_cb = 0.0

    funcs = [add_se_prices,add_ts_prices,add_sx_prices,add_ct_prices,add_cb_prices]

    all_prices = [globalvars.se_prices,globalvars.ts_prices,globalvars.sx_prices,globalvars.ct_prices,globalvars.cb_prices]

    pool = multiprocessing.pool.ThreadPool()

    new_prices = []

    for i,f in enumerate(funcs):
        new_prices.append(pool.apply(f, (all_prices[i],coin_name)))

    for i,price in enumerate(new_prices):
        if i == 0:
            buy_price_se = price
        elif i == 1:
            buy_price_ts = price
        elif i == 2:
            buy_price_sx = price
        elif i == 3:
            buy_price_ct = price
        elif i == 4:
            buy_price_cb = price
    return buy_price_se,buy_price_ts,buy_price_sx,buy_price_ct,buy_price_cb

def get_exchange_prices():
    funcs = [load_se_prices,load_ts_prices,load_sx_prices,load_ct_prices,load_cb_prices,load_btc_price]

    all_prices = [globalvars.se_prices,globalvars.ts_prices,globalvars.sx_prices,globalvars.ct_prices,globalvars.cb_prices,globalvars.btc_price]

    pool = multiprocessing.Pool()

    new_prices = []

    for i,f in enumerate(funcs):
        new_prices.append(pool.apply(f, (all_prices[i],)))

    for i,price in enumerate(new_prices):
        if i == 0:
            globalvars.se_prices = price
        elif i == 1:
            globalvars.ts_prices = price
        elif i == 2:
            globalvars.sx_prices = price
        elif i == 3:
            globalvars.ct_prices = price
        elif i == 4:
            globalvars.cb_prices = price
        elif i == 5:
            globalvars.btc_price = price

def calc_coin(key):
    buy_price_se = 0.0
    buy_price_ts = 0.0
    buy_price_sx = 0.0
    buy_price_ct = 0.0
    buy_price_cb = 0.0
    difficulty = 0.0
    coins_mined = 0.0
    coin_profit = 0.0
    coin_list = []
    exchange = ''

    # Gather information for the coin and store them in variables 
    coin_name = key['coin']   
    url = key['api_url']
    block_reward = key['block_reward']
    pool_url = key['pool_url']
    port = key['port']
    algorithm = key['algo']
    difficulty,difficulty_loaded = load_difficulty(url,coin_name)
        
    if not difficulty_loaded:
        calclog.debug("Skipping coin: " + coin_name)
    else:
        buy_price_se,buy_price_ts,buy_price_sx,buy_price_ct,buy_price_cb = add_exchange_prices(coin_name)
        # Find the BTC price in the json file queried from coinbase, then calculate it's value in USD.
        usd_price = float(globalvars.btc_price["data"]["rates"]["USD"])

        calclog.debug(" Stocks.Exchange Price: " +  str(buy_price_se) + " Trade Satoshi Price: " + str(buy_price_ts) + " Southxchange Price: " + str(buy_price_sx) + " Cryptopia Price: " + str(buy_price_ct) + " Crypto-Bridge Price: " + str(buy_price_cb))

        buy_prices = [buy_price_ct,buy_price_se,buy_price_sx,buy_price_ts,buy_price_cb]
        buy_prices.sort(reverse=True)

        # List the exchange with the highest value of the coin.
        calclog.debug("Highest Price: " + str(buy_prices))

        for i in range(len(buy_prices)):
            if buy_prices[i] == buy_price_se and not key['exchange']['Stocks.Exchange'] == "NA":
                coin_price = buy_price_se * usd_price
                calclog.debug(" Stocks.Exchange Price: " +  str(buy_price_se) + " USD price: " + str(coin_price))
                exchange = "Stocks.Exchange"
                break
            elif buy_prices[i] == buy_price_ts and not key['exchange']['Trade Satoshi'] == "NA":
                coin_price = buy_price_ts * usd_price
                calclog.debug(" Trade Satoshi Price: " + str(buy_price_ts) + " USD price: " + str(coin_price))
                exchange = "Trade Satoshi"
                break
            elif buy_prices[i] == buy_price_sx and not key['exchange']['Southxchange'] == "NA":
                coin_price = buy_price_sx * usd_price
                calclog.debug(" Southxchange Price: " + str(buy_price_sx) + " USD price: " + str(coin_price))
                exchange = "Southxchange"
                break
            elif buy_prices[i] == buy_price_ct and not key['exchange']['Cryptopia'] == "NA":
                coin_price = buy_price_ct * usd_price
                calclog.debug(" Cryptopia Price: " + str(buy_price_ct) + " USD price: " + str(coin_price))
                exchange = "Cryptopia"
                break
            elif buy_prices[i] == buy_price_cb and not key['exchange']['Crypto-Bridge'] == "NA":
                coin_price = buy_price_cb * usd_price
                calclog.debug(" Crypto-Bridge Price: " +  str(buy_price_cb) + " USD price: " + str(coin_price))
                exchange = "Crypto-Bridge"
                break

        # Initialize an object for each coin and the object as a key in a dictionary, then calculate the 24 hour
        # profitiability of the coin and store it as the value in the dictionary.
        # e.g. { "coin" : 12.34 }
        new_coin = coin.Coin(coin_name,coin_price,usd_price,exchange,block_reward,difficulty,algorithm)

        for k in globalvars.algo_config_list:
            for algo in list(k.keys()):
                if algorithm == algo:
                    #calclog.info(str( globalvars.algo_config_list[i]) + '\n' + list(k.keys())[i] + '\n' + algorithm)
                    hashrate = k[algorithm]['hashrate']
                    electricity_costs = k[algorithm]['electricity_costs']
                    power_consumption = k[algorithm]['power_consumption']
                
        
        if not algorithm == "equihash" and not coin_name == "HUSH" and not coin_name == "CROP":
            # Convert KH/s to H/s
            hashrate *= 1000
            coins_mined = (hashrate/(difficulty*(2**32))*86400*block_reward)
        elif coin_name == "CROP":
            # Convert KH/s to H/s
            hashrate *= 1000
            coins_mined = (hashrate/(difficulty*(2**23))*86400*block_reward)
        elif coin_name == "HUSH":
            coins_mined = (hashrate/(difficulty*(2.001313))*86400*block_reward)
        else:
            coins_mined = (hashrate/(difficulty*(2**13))*86400*block_reward)
        
        coin_profit = coins_mined * new_coin.getPrice()

        calclog.debug("Coin: " + coin_name + " Hashrate: " + str(hashrate) + " Difficulty: " + str(difficulty) + " Price: " + str(coin_price) + " Block reward: " + str(block_reward) + " Reward: " + str(coins_mined) + " Revenue: " + str(coin_profit))

        globalvars.coins[new_coin] = coin_profit
        calclog.debug("Currently processing" + coin_name)
        wallet_address = key['exchange'][new_coin.getExchange()]
        daily_electricity_costs = ((power_consumption/1000)*24)*float(electricity_costs)
        calclog.info(coin_name + " coin has been loaded.")
        coin_list = [coin_profit, coins_mined, difficulty, new_coin.getPrice(), new_coin.getBTCPrice(), new_coin.getExchange(), pool_url, wallet_address,algorithm,port,daily_electricity_costs]

    return coin_list

def calc_coins(coin_info):
    pool = multiprocessing.pool.ThreadPool()
    all_coins = {}
    coin_obj = []

    coin_obj = pool.map(calc_coin, coin_info)

    for i,key in enumerate(coin_obj):
        all_coins[coin_info[i]['coin']] = key

    return all_coins

def calc(coin_info):
    most_profitable_coin_list = []

    # Begin fetching the price of each coin
    calclog.info("Fetching coin prices...")
   
    get_exchange_prices()

    calclog.info("Coin prices successfully loaded.")

    # Load the coins from the file and store them into a list
    calclog.info("Loading coins...")
    
    all_coins = calc_coins(coin_info)

    # Store info on each coin as a list of dictionaries sorted by most profitable to least profitable.
    for key, value in sorted(all_coins.items(), key=lambda item: (item[1], item[0]), reverse=True):
        for key2, value2 in globalvars.coins.items():
            try:
                if value2 == value[0]:
                    most_profitable_coin_list.append({'coin' : key,
                    'est_block_reward' : all_coins[key][1],
                    'difficulty' : all_coins[key][2],
                    'price' : all_coins[key][3],
                    'exchange' : all_coins[key][5],
                    'btc_price' : all_coins[key][4],
                    'pool_url' : all_coins[key][6],
                    'wallet_address' : all_coins[key][7],
                    'algorithm' : all_coins[key][8],
                    'port' :  all_coins[key][9],
                    'electricity_costs' :  all_coins[key][10],
                    'estimated_revenue' : all_coins[key][0],
                    'estimated_profits' : all_coins[key][0] - all_coins[key][10]})
            except IndexError:
                pass

    with open('most_profitable_coins.json', 'w') as outfile:
        json.dump(most_profitable_coin_list, outfile)

    return most_profitable_coin_list

def print_coins(coin_list):
    tablist = []

    for key in coin_list:
        tablist.append([key['coin'],
        key['algorithm'],
        key['difficulty'],
        key['est_block_reward'],
        "$" +  str("%.4f" % key['price']),
        key['exchange'],
        "$" +  str(key['btc_price']),
        "$" + str("%.2f" % key['estimated_revenue']),
        "$" + str("%.2f" % key['estimated_profits'])])
    
    calclog.info("\n" + tabulate(tablist, headers=['Coin', 'Algorithm', 'Difficulty', 'Reward', "Price", "Exchange", "BTC Price", "Revenue", "Profits"], stralign="center", numalign="right", floatfmt=".4f"))

def load_config():
    load_successful = False
    config = {}
    try:
        config = json.load(open('config.json'))
        load_successful = True
        return load_successful,config
    except (IOError, ValueError) as err:
        return load_successful,config

def load_algo_config(config,algo):
    load_successful = False

    for i,algo_config in enumerate(config):
        if algo == list(algo_config.keys())[0]:
            try:
                globalvars.algo_config_list.append(algo_config)
                calclog.debug("Found " + algo + " in config file")
                load_successful = True
                return load_successful
            except (KeyError, IndexError) as err:
                calclog.error(algo + " not found in file")
                return load_successful

if __name__ == "__main__":
    # Check if the person has a configuration file. If not, start benchmarking.
    config_load_successful,config = load_config()

    if not config_load_successful:
        calclog.error("Config file not found, try running the benchmark first.")

    if config_load_successful:
        coin_info = json.load(open('coininfo.json'))

        algorithm_list = []

        algorithm_list.append(coin_info[0]['algo'])
        for key in coin_info:      
            if not key['algo'] in algorithm_list:
                algorithm_list.append(key['algo'])

        for i,algo in enumerate(algorithm_list):
            algo_config_load_successful = load_algo_config(config,algo)
            if not algo_config_load_successful:
                calclog.error("Some algorithms are missing from your config file, please run the benchmark first...")
                sys.exit()

        most_profitable_coins = calc(coin_info)

        print_coins(most_profitable_coins)

        # Store the most profitable coin's name.
        most_profitable_coin_name = most_profitable_coins[0]['coin']

        calclog.info("Your most profitable coin is: " + most_profitable_coin_name)
