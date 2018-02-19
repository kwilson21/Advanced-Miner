# Advanced-Miner
Are you tired of mining pools charging ridiculous fees for subpar customer service? Are an experienced miner who manually mines their own coins for profit? Then Advanced Miner is for you!

Advanced miner is an NVIDIA multi-algorithm profit switching calculator and miner combined. Written in python 3.6, Advanced Miner supports 9 different algorithms and as many coins as you can find!

## Getting Started
Make sure that you install python.

This program requires the following modules to run:

[Requests](http://docs.python-requests.org/en/master/)
[Tabulate](https://pypi.python.org/pypi/tabulate)
[wget](https://pypi.python.org/pypi/wget)

How to install the depencies:
```
pip install requests
pip install tabulate
pip install wget
```
Once you have your depencies set up, you will need to configure your coininfo.json file. Here you will need to set up your wallet address for each exchange. Look for the "exchange" field and update each exchange listed with your wallet. I currently mine almost all of my coins directly to the exchange. If you have a cold wallet set up for any of the coins, set each exchange wallet address to your cold wallet.

Once your coininfo file is set up simply run Start-Miner.bat.
The miner will prompt you to enter your electricity costs in kW/h and the amount of time you would like to spend benchmarking each algorithm in minutes.