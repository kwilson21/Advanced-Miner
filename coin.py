class Coin:
    def __init__(self,coin_name,coin_price,btc_price,exchange,block_reward,difficulty,algorithm):
        self.coin_name = coin_name
        self.btc_price = btc_price
        self.exchange = exchange
        self.price = coin_price
        self.block_reward = block_reward
        self.difficulty = difficulty
        self.algorithm = algorithm
        
    def getAlgorithm(self):
        return self.algorithm

    def getPrice(self):
        return self.price

    def getExchange(self):
        return self.exchange

    def getBTCPrice(self):
        return self.btc_price

    def getCoinname(self):
        return self.coin_name

    def getBlockReward(self):
        return self.block_reward

    def getDifficulty(self):
        return self.difficulty

    def __hash__(self):
        return hash(str(self.coin_name))

    def __eq__(self, other):
        return str(self.coin_name) == str(other.name)