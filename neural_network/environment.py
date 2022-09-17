from trading.binance_manager import BinanceManager
import rl.core as krl
import random
import numpy as np
import pandas as pd
import datetime

class ActionSpace(krl.Space):
    def __init__(self):
        self.shape = (1,)

    def sample(self, seed=None):
        return random.randint(-1, 1)

    def contains(self, x):
        if x == 1 or x == 0 or x == -1:
            return True

        return False

class ObservationSpace(krl.Space):
    def __init__(self, inputs):
        self.shape = (inputs,)

    def sample(self, seed=None):
        pass

    def contains(self, x):
        pass

class Environment(krl.Env):
    def __init__(self, inputs, symbol, interval, start_time, end_time) -> None:
        super().__init__()
        self.action_space = ActionSpace()
        self.observation_space = ObservationSpace(inputs)

        self.binance=BinanceManager(symbol)
        self.df=self.getData(symbol, interval, start_time, end_time)
        self.frame_size=self.observation_space.shape[0]

    def getData(self, symbol, interval, start_time, end_time):
        start_timestamp=str(datetime.datetime.strptime(start_time, "%m/%d/%Y %H:%M").timestamp())
        end_timestamp=str(datetime.datetime.strptime(end_time, "%m/%d/%Y %H:%M").timestamp())
        df=pd.DataFrame(self.binance.get_futures_historical_klines(symbol, interval, start_timestamp, end_timestamp))
        df=df.drop(columns=[0, 6, 11])
        df=df.reset_index(drop=True)
        df.columns=['Open', 'Hight', 'Low', 'Close', 'Volume', 'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume']

        return df

    def reset(self):
        self.last_action=0
        self.last_price=0
        self.done=False
        self.reward=0
        self.current_index=0
        observation=np.array([
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Open'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Hight'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Low'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Close'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Volume'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'QuoteAssetVolume'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'NumberOfTrades'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'TakerBuyBaseAssetVolume'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'TakerBuyQuoteAssetVolume'].values,
        ])

        return observation

    def getPrice(self, action):
        return 0.0

    def getMaxIndex(self):
        return self.df.shape[0]

    def getNextObservation(self):
        frame=np.array([
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Open'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Hight'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Low'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Close'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Volume'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'QuoteAssetVolume'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'NumberOfTrades'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'TakerBuyBaseAssetVolume'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'TakerBuyQuoteAssetVolume'].values,
        ])
        self.current_index+=1
        return frame, self.current_index == self.getMaxIndex() - self.frame_size

    def step(self, action):
        if action == -1 or action == 1:
            self.last_price=self.getPrice(action)
            self.last_action=action

        if self.last_action == -1:
            pass
        elif self.last_action == 1:
            pass
        
        observation, self.done=self.getNextObservation()

        return observation, self.reward, self.done, None

    def render(self):
        pass

    def close(self):
        pass