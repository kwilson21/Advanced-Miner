import calclog
import coin
import coincalc
import PyCCMiner
import mzip

import os
import logging
import sys
import re
import requests
import time
import json
import random
import subprocess
from datetime import datetime
from threading import Thread, Timer, Event

# Declare all variables
global answered
answered = False
hashrate = 0.0
electricity_costs = 0.0
power_consumption = 0.0

neoscrypt_config = {} 
equihash_config = {} 
xevan_config = {}
lyra2v2_config = {}
bitcore_config = {} 
skunk_config = {} 
nist5_config = {}
skein_config = {}
tribus_config = {}
algorithm_list = []
exchanges = []

minerlog = logging.getLogger('miner')

minerlog.info("Loading configurations...")
coin_info = json.load(open('coininfo.json'))

# Create a list of all of the current algorithms
algorithm_list.append(coin_info[0]['algo'])
for key in coin_info:      
    if not key['algo'] in algorithm_list:
        algorithm_list.append(key['algo'])

# Create a list of all of the current exchanges
exchanges.append(list(coin_info[0]['exchange'].keys())[0])
for key in coin_info:
    for j in range(len(list(key['exchange'].keys()))):
        if not list(key['exchange'].keys())[j] in exchanges and not list(key['exchange'].keys())[j] == '':
            exchanges.append(list(key['exchange'].keys())[j])

miner_info = json.load(open('miners.json'))

# Start miner api
hsr = PyCCMiner.api()
minerlog.info("Starting miner api...")

def isrunning(name):
    # Check if a process is running
    s = subprocess.check_output('tasklist', shell=True)
    if name in str(s):
        return True
    else:
        return False

def kill_miner(algorithm):
    # Depending on what the algorithm is, kill that specific miner process.
    if algorithm == "neoscrypt":
        os.system('taskkill /f /im hsrminer_neoscrypt_fork.exe /t')
    elif algorithm == "equihash":
        os.system('taskkill /f /im Zminer.exe /t')
    elif algorithm == "xevan":
        os.system('taskkill /f /im ccminer_x86.exe /t')
    elif algorithm in ("lyra2v2","nist5","skein"):
        os.system('taskkill /f /im ccminer-alexis.exe /t')
    elif algorithm in ("bitcore","skunk","tribus"):
        os.system('taskkill /f /im ccminer.exe /t')

def check_if_miner_is_running(algorithm):
    # Check if the miner is running and return a boolean state.
    if algorithm == "neoscrypt":
        miner_running = isrunning('hsrminer_neoscrypt_fork')
    elif algorithm == "equihash":
        miner_running = isrunning('Zminer')
    elif algorithm == "xevan":
        miner_running = isrunning('ccminer_x86')
    elif algorithm in ("lyra2v2","nist5","skein"):
        miner_running = isrunning('ccminer-alexis')
    elif algorithm in ("bitcore","skunk","tribus"):
        miner_running = isrunning('ccminer')
    return miner_running

def start_miner(coin_name,coin_info):
    FILEPATH = os.path.dirname(os.path.realpath(__file__))
    date = datetime.now().strftime('%m-%d-%Y')

    for key in coin_info:
        if key['coin'] == coin_name:
            # Store the pool name for the coin.
            if "arcpool" in key['pool_url']:
                pool_url = "Arcpool"
            elif "bsod" in key['pool_url']:
                pool_url = "BSOD"
            elif "unimining" in key['pool_url']:
                pool_url = "Unimining"
            elif "cryptopros" in key['pool_url']:
                pool_url = "Cryptopros"
            elif "altminer" in key['pool_url']:
                pool_url = "Altminer"
            elif "zhash" in key['pool_url']:
                pool_url = "Zhash"
            elif "yiimp" in key['pool_url']:
                pool_url = "Yiimp"
            elif "nanopool" in key['pool_url']:
                pool_url = "Nanopool"
            elif "bitcore" in key['pool_url']:
                pool_url = "Bitcorepool"
            elif "2miners" in key['pool_url']:
                pool_url = "2miners"
            elif "miningspeed" in key['pool_url']:
                pool_url = "Miningspeed"
            elif "cryptoally" in key['pool_url']:
                pool_url = "Cryptoally"
            elif "173.249.24.88" in key['pool_url']:
                pool_url = "Tunecrypto"
            elif "tiny-pool" in key['pool_url']:
                pool_url = "Tiny-Pool"
            
            # Check if a miner is running, if it is, close it before starting another instance.
            miner_running = check_if_miner_is_running(key['algorithm'])
            if miner_running:
                kill_miner(key['algorithm'])

            minerlog.debug("Coin pool: " + pool_url.lower() + " Coin algo: " + key['algorithm'])

            # Depending on the algorithm, start the miner that supports it.
            if key['algorithm'] == "neoscrypt":
                cmd_line = 'start "" ' + FILEPATH + '\\bin\\NVIDIA-hsrminer-neoscrypt\\hsrminer_neoscrypt_fork' + ' -o ' + key['pool_url'] + ":" + key['port'] + " -u " + key['wallet_address'] + ' -p c=' + key['coin']
                minerlog.debug(cmd_line)
                os.system(cmd_line)
            elif key['algorithm'] == "equihash" and pool_url.lower() in ("Zhash","2miners","miningspeed"):
                cmd_line = 'start "" ' + FILEPATH + '\\bin\\NVIDIA-EWBF\\Zminer' + " --server " + key['pool_url'] + " --port " + key['port'] + " --user " + key['wallet_address'] + ".SCMiner" + " --pass x --fee 0 --api 127.0.0.1:42000"
                minerlog.debug(cmd_line)
                os.system(cmd_line)
            elif key['algorithm'] == "equihash" and pool_url.lower() == "nanopool":
                cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-EWBF\\Zminer' + " --server " + key['pool_url'] + " --port " + key['port'] + " --user " + key['wallet_address'] + ".SCMiner" + " --pass z --fee 0 --api 127.0.0.1:42000"
                minerlog.debug(cmd_line)
                os.system(cmd_line)
            elif key['algorithm'] == "xevan":
                cmd_line = 'start "" ' + FILEPATH + '\\bin\\NVIDIA-Alexis78cuda9\\ccminer_x86' + ' -a ' + key['algorithm'] + ' -o ' + key['pool_url'] + ":" + key['port'] + " -u " + key['wallet_address'] + ' -p c=' + key['coin']
                minerlog.debug(cmd_line)
                os.system(cmd_line)
            elif key['algorithm'] in ("lyra2v2","nist5","skein"):
                cmd_line = 'start "" ' + FILEPATH + '\\bin\\NVIDIA-Alexis78cuda8\\ccminer-alexis' + ' -a ' + key['algorithm'] + ' -o ' + key['pool_url'] + ":" + key['port'] + " -u " + key['wallet_address'] + ' -p c=' + key['coin']
                minerlog.debug(cmd_line)
                os.system(cmd_line)
            elif key['algorithm'] in ("bitcore","skunk"):
                cmd_line = 'start "" ' + FILEPATH + '\\bin\\NVIDIA-TPruvot\\ccminer' + ' -a ' + key['algorithm'] + ' -o ' + key['pool_url'] + ":" + key['port'] + " -u " + key['wallet_address'] + ' -p c=' + key['coin']
                minerlog.debug(cmd_line)
                os.system(cmd_line)
            elif key['algorithm'] == "tribus":
                cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-TPruvotcuda9\\ccminer' + ' -a ' + key['algorithm'] + ' -o ' + key['pool_url'] + ":" + key['port'] + " -u " + key['wallet_address'] + ' -p c=' + key['coin']
                minerlog.debug(cmd_line)
                os.system(cmd_line)

            minerlog.info("You are now mining " + key['coin'] + " @ " + pool_url + " " + datetime.now().strftime('%I:%M%p') + " " + date)
            key['date'] = datetime.now().strftime('%I:%M%p') + " " + date
            # Store information about the coin being currently mined in a file.
            with open('currently_mining.json', 'w') as outfile:
                json.dump(key, outfile)
            
    #time = datetime.now().strftime('%I:%M%p')

def benchmark(coin_info,algorithm,electricity_costs,bench_time):
    calc_details = {}
    hashrate_list = []
    power_consumption_list = []
    hashrate = 0.0
    power_consumption = 0.0
    FILEPATH = os.path.dirname(os.path.realpath(__file__))

    minerlog.info("Benchmarking: " + algorithm)

    # Generate a random number between the the total amount of coins stored in the coin info file.
    valid = False
    while not valid:
        random_num = random.randint(0,len(coin_info) - 1) 
        try:
            if coin_info[random_num]['pool_url'] and coin_info[random_num]['algo'] == algorithm:
                minerlog.debug(" Pool URL is: " + coin_info[random_num]['pool_url'] + " Algorithm is: " + coin_info[random_num]['algo'])
                valid = True
        except:
            pass

    # Generate a random number between the total amount of exchanges stored in the coin info file.
    valid = False
    while not valid:
        random_num2 = random.randint(0,len(exchanges) - 1)
        minerlog.debug("exchange length is: " + str(len(exchanges)))
        minerlog.debug("rannum2 is " + str(random_num2))
        try:
            if not coin_info[random_num]['exchange'][exchanges[random_num2]] == "NA":
                minerlog.debug("Exchange found, wallet address is: " + coin_info[random_num]['exchange'][exchanges[random_num2]])
                valid = True
        except:
            pass

    minerlog.debug("random num is: " + str(random_num))
    minerlog.debug("random num 2 is: " + str(random_num))
    minerlog.info(coin_info[random_num]['coin'] + " has been randomly chosen to mine while benchmarking")

    random_pool = coin_info[random_num]['pool_url']
    port = coin_info[random_num]['port']
    random_wallet_address = coin_info[random_num]['exchange'][exchanges[random_num2]]
    random_coin_name = coin_info[random_num]['coin']

    def open_miner():
        for key in coin_info:
            if key['coin'] == random_coin_name:
                if "arcpool" in key['pool_url']:
                    pool_url = "Arcpool"
                elif "bsod" in key['pool_url']:
                    pool_url = "BSOD"
                elif "unimining" in key['pool_url']:
                    pool_url = "Unimining"
                elif "cryptopros" in key['pool_url']:
                    pool_url = "Cryptopros"
                elif "altminer" in key['pool_url']:
                    pool_url = "Altminer"
                elif "zhash" in key['pool_url']:
                    pool_url = "Zhash"
                elif "yiimp" in key['pool_url']:
                    pool_url = "Yiimp"
                elif "nanopool" in key['pool_url']:
                    pool_url = "Nanopool"
                elif "bitcore" in key['pool_url']:
                    pool_url = "Bitcorepool"
                elif "2miners" in key['pool_url']:
                    pool_url = "2miners"
                elif "miningspeed" in key['pool_url']:
                    pool_url = "Miningspeed"
                elif "cryptoally" in key['pool_url']:
                    pool_url = "Cryptoally"
                elif "173.249.24.88" in key['pool_url']:
                    pool_url = "Tunecrypto"
                elif "tiny-pool" in key['pool_url']:
                    pool_url = "Tiny-pool"

        minerlog.debug("Coin pool: " + pool_url.lower() + " Coin algo: " + algorithm)

        if algorithm == "neoscrypt":
            cmd_line = 'start "" ' + FILEPATH + '\\bin\\NVIDIA-hsrminer-neoscrypt\\hsrminer_neoscrypt_fork' + ' -o ' + random_pool + ":" + port + " -u " + random_wallet_address + ' -p c=' + random_coin_name
            minerlog.debug(cmd_line)
            os.system(cmd_line)
        elif algorithm == "equihash" and pool_url.lower() in ("zhash","2miners","miningspeed"):
            cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-EWBF\\Zminer' + " --server " + random_pool + " --port " + port + " --user " + random_wallet_address + ".SCMiner" + " --pass x --fee 0 --api 127.0.0.1:42000"
            minerlog.debug(cmd_line)
            os.system(cmd_line)
        elif algorithm == "equihash" and pool_url.lower() == "nanopool":
            cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-EWBF\\Zminer' + " --server " + random_pool + " --port " + port + " --user " + random_wallet_address + ".SCMiner" + " --pass z --fee 0 --api 127.0.0.1:42000"
            minerlog.debug(cmd_line)
            os.system(cmd_line)
        elif algorithm == "xevan":
            cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-Alexis78cuda9\\ccminer_x86' + ' -a ' + algorithm + ' -o ' + random_pool + ":" + port + " -u " + random_wallet_address + ' -p c=' + random_coin_name
            minerlog.debug(cmd_line)
            os.system(cmd_line)
        elif algorithm in ("lyra2v2","nist5","skein"):
            cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-Alexis78cuda8\\ccminer-alexis' + ' -a ' + algorithm + ' -o ' + random_pool + ":" + port + " -u " + random_wallet_address + ' -p c=' + random_coin_name
            minerlog.debug(cmd_line)
            os.system(cmd_line)
        elif algorithm in ("bitcore","skunk"):
            cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-TPruvot\\ccminer' + ' -a ' + algorithm + ' -o ' + random_pool + ":" + port + " -u " + random_wallet_address + ' -p c=' + random_coin_name
            minerlog.debug(cmd_line)
            os.system(cmd_line)
        elif algorithm == "tribus":
            cmd_line ='start "" ' + FILEPATH + '\\bin\\NVIDIA-TPruvotcuda9\\ccminer' + ' -a ' + algorithm + ' -o ' + random_pool + ":" + port + " -u " + random_wallet_address + ' -p c=' + random_coin_name
            minerlog.debug(cmd_line)
            os.system(cmd_line)

    # Once the random coin, pool and exchange is selected, begin benchmarking the coin.
    open_miner()

    # Give the miner a chance get started before querying for hashrates.
    time.sleep(60)

    for i in range(int(bench_time) * 2):
        # Every minute, check if the miner is running and if it isn't start the miner again.
        miner_running = check_if_miner_is_running(algorithm)
        if not miner_running:
            minerlog.info("Miner is not open, restarting...")
            open_miner()
            time.sleep(50)
        
        # The 2 miners currently used in this program are EWBF and CCminer
        # Depending on what miner is running, this accesses each api in order to retrieve the current hashrate and power consumption.
        if not algorithm == "equihash":
            temp_hash = hsr.getHashrate()
            minerlog.info("Hashes: " + temp_hash + "KH/s")
            hashrate_list.append(float(temp_hash))
        else:
            hash_list = []
            ewbf_stats = requests.get('http://127.0.0.1:42000/getstat').json()
            for i in range(len(ewbf_stats['result'])):
                hash_list.append(ewbf_stats['result'][i]['speed_sps'])
            temp_hash = sum(hash_list)
            minerlog.info("Hashes: " + str(temp_hash) + "Sol/s")
            hashrate_list.append(float(temp_hash))

        time.sleep(30)

    # The benchmark stores a hashrate from the miner every minute and puts them into a list,
    # once the benchmark is done it takes the average of the hashrates.
    hashrate = sum(hashrate_list, 0.0) / len(hashrate_list)

    # Get the power consumption before closing closing the miner.
    if not algorithm == "equihash":
        power_consumption_list = [float(i) for i in hsr.getPowerConsumption()]
        power_consumption = sum(power_consumption_list)
    else:
        ewbf_stats = requests.get('http://127.0.0.1:42000/getstat').json()
        for i in range(len(ewbf_stats['result'])):
            power_consumption_list.append(float(ewbf_stats['result'][i]['gpu_power_usage']))
        power_consumption = sum(power_consumption_list)

    # Store all of the information needed for the calculator and write this configuration to a file in JSON format.
    calc_details = {algorithm : {'hashrate' : hashrate, 'electricity_costs':electricity_costs, 'power_consumption':power_consumption}}

    def write_config():
        config = []
        
        try:
            config = json.load(open('config.json'))
        except:
            pass
        config.append(calc_details)
        with open('config.json', 'w') as f:
            json.dump(config, f)

    write_config()
    minerlog.info("Benchmark finished. Closing miner...")
    kill_miner(algorithm)
    return True

# Download and extract miners
mzip.download_miners(miner_info)
mzip.extract_miners()

def bench_algos(algo,electricity_costs,bench_time):
    algo_finished = False
    for key in coin_info:
        if not algo_finished and key['algo'] == algo:
            algo_finished = benchmark(coin_info,algo,electricity_costs,bench_time)
            algo_finished = True
    return algo_finished

def get_info():
    electricity_costs = float(input("Please enter your electricity costs in $kWh/h: "))

    bench_time = input("Please enter your miner benchmark time in minutes (a minimum of 8 minutes is recommended): ")

    while not re.match("^[0-9]*$", bench_time):
        minerlog.info("ERROR: Please only enter numbers!")
        minerlog.debug("User entered bad input, prompting again...")
        bench_time = input("Please enter your miner benchmark time in minutes (a minimum of 8 minutes is recommended): ")
    
    return electricity_costs,bench_time

# Check for the configuration file. If there isn't, begin benchmarking.
config_load_successful,config = coincalc.load_config()

if not config_load_successful:
    minerlog.info("Config file not found. Configuring new settings...")

    electricity_costs,bench_time = get_info()    

    # Benchmark each algorithm
    neoscrypt_finished, equihash_finished, xevan_finished, lyra2v2_finished, bitcore_finished, skunk_finished, nist5_finished, skein_finished, tribus_finished = (False,)*9

    for key in coin_info:
        if key['algo'] == "neoscrypt" and not neoscrypt_finished:
            neoscrypt_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "equihash" and not equihash_finished:
           equihash_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "xevan" and not xevan_finished:
            xevan_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "lyra2v2" and not lyra2v2_finished:
            lyra2v2_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "bitcore" and not bitcore_finished:
            bitcore_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "skunk" and not skunk_finished:
            skunk_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "nist5" and not nist5_finished:
            nist5_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "skein" and not skein_finished:
            skein_finished = bench_algos(key['algo'],electricity_costs,bench_time)
        elif key['algo'] == "tribus" and not tribus_finished:
            tribus_finished = bench_algos(key['algo'],electricity_costs,bench_time)

    config_load_successful,config = coincalc.load_config()

# Begin loading the hashrates for each algorithm.
# If a hashrate is not found for the algorithm, prompt the user to benchmark the algorithm.
i=0
for algo in algorithm_list:
    new_algo_config = {}
    algo_config_load_successful,algo,new_algo_config = coincalc.load_algo_config(config,algo)
    if not algo_config_load_successful:
        minerlog.info("Some algorithms are missing from your config file, now benchmarking those algorithms...")
        if i == 0:
            # Only prompt the user to enter their electricity and desired benchmark time once.
            electricity_costs,bench_time = get_info()
        algos_finished = bench_algos(algo,electricity_costs,bench_time)
        algo_config_load_successful,algo,new_algo_config = coincalc.load_algo_config(config,algo)
    if algo == "neoscrypt":
        neoscrypt_config = new_algo_config
    elif algo == "equihash":
        equihash_config = new_algo_config
    elif algo == "xevan":
        xevan_config = new_algo_config
    elif algo == "lyra2v2":
        lyra2v2_config = new_algo_config
    elif algo == "bitcore":
        bitcore_config = new_algo_config
    elif algo == "skunk":
        skunk_config = new_algo_config
    elif algo == "nist5":
        nist5_config = new_algo_config
    elif algo == "skein":
        skein_config = new_algo_config
    elif algo == "tribus":
        tribus_config = new_algo_config
    i+=1

while True:
    # Start the calculator
    most_profitable_coins = coincalc.calc(coin_info,neoscrypt_config,equihash_config,xevan_config,lyra2v2_config,bitcore_config,skunk_config,nist5_config,skein_config,tribus_config)

    minerlog.debug(most_profitable_coins)

    # Print the most profitable coins on the console.
    coincalc.print_coins(most_profitable_coins)

    # Store the most profitable coin's name.
    most_profitable_coin_name = most_profitable_coins[0]['coin']

    minerlog.info("Your most profitable coin is: " + most_profitable_coin_name)

    def finish():
        interval = 28800
        minerlog.debug("Sleeping for " + str(interval) + " seconds.")
        time.sleep(interval)

    def process_input(timer):
        global answered
        global answer
        minerlog.debug("Prompting user to switch miners...")
        if not answered:
            answer = input("Do you want to mine the current most profitable coin? (WARNING: Miner will auto switch in 15 seconds if you do not respond): ")

            while not re.match("^[A-Za-z]*$", answer):
                minerlog.info("ERROR: Please only enter letters!")
                minerlog.debug("User entered bad input, prompting again...")
                answer = input("Do you want to mine the current most profitable coin? (WARNING: Miner will auto switch in 15 seconds if you do not respond): ")
        
            if answer.lower() in ("yes", "ye", "y",""):
                answered = True
                print()
                minerlog.info("Switching miner to most profitable coin...")
                start_miner(most_profitable_coin_name,most_profitable_coins)
                timer.cancel()
                finish()
            elif answer.lower() in ("no", "n"):
                answered = True
                timer.cancel()
                minerlog.info("You selected no, closing timer thread...")

    def manually_mine(coin_info):
        minerlog.debug("Prompting the user to mine a different coin...")
        response = input("Would you like to mine a different coin instead?: ")

        while not re.match("^[A-Za-z]*$", response):
            minerlog.info("ERROR: Please only enter letters!")
            minerlog.debug("User entered bad input, prompting again...")
            response = input("Would you like to mine a different coin instead?: ")

        if response.lower() in ("yes", "ye", "y",""):
            minerlog.debug("Prompting the user to enter the coin they would like to mine...")
            coin_name = input("Please enter the coin you would like to mine: ")

            for key in coin_info:
                if key['coin'] == coin_name:
                    key_found = True
                else:
                    key_found = False

            while not re.match("^[A-Za-z]*$", coin_name) and not key_found:
                minerlog.info("ERROR: Please enter a coin from the list above!")
                minerlog.debug("User entered bad input, prompting again...")
                coin_name = input("Would you like to mine a different coin instead?: ")

                for key in coin_info:
                    if key['coin'] == coin_name:
                        key_found = True
                    else:
                        key_found = False
            start_miner(coin_name,coin_info)
        else:
            # If the user does not want to mine a coin, exit the program.
            finish()

    # Create a timer and prompt the user to switch coins, if they do not respond before the time is up,
    # the program will automatically switch coins.
    delay = 15
    finished = Event()
    while not finished.isSet():
        timer = Timer(delay, finished.set)
        worker = Thread(target=process_input, args=(timer,))
        worker.setDaemon(True)
        worker.start()
        timer.start()
        timer.join()

    # If the user does not respond within 15 seconds, start mining. If they do respond but say no, prompt them to mine another coin instead.
    if not answered:
        print()
        minerlog.info("Switching miner to most profitable coin...")
        start_miner(most_profitable_coin_name,most_profitable_coins)
        timer.cancel()
        finish()
    else:
        manually_mine(most_profitable_coins)