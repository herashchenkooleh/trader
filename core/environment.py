from cmath import nan
import rl.core as krl
import random
import numpy as np
import pandas as pd
from datetime import datetime

from stocktrends import Renko

class ActionSpace(krl.Space):
    def __init__(self):
        self.shape = (3,)

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
    def __init__(self, binance_manager, settings) -> None:
        super().__init__()
        self.binance_manager=binance_manager
        self.settings=settings

        self.update()
        

    def update(self):
        start_timestamp=str(datetime.strptime(self.settings.start_time, "%d/%m/%Y %H:%M").timestamp())
        end_timestamp=str(datetime.strptime(self.settings.end_time, "%d/%m/%Y %H:%M").timestamp())
        binance_data=pd.DataFrame(self.binance_manager.get_futures_historical_klines(self.settings.symbol, self.settings.interval, start_timestamp, end_timestamp))
        
        binance_data.columns=['date', 'open', 'high', 'low', 'close', 'volume', '6', '7', '8', '9', '10', '11']
        
        #renko
        self.renko_df=binance_data.loc[: , ['date', 'open', 'high', 'low', 'close']]
        self.renko_df=self.renko_df.astype(np.float)
        self.renko_df=Renko(self.renko_df)
        self.renko_df.brick_size=self.settings.renko_n
        self.renko_df=self.renko_df.get_ohlc_data()
        self.renko_df=self.renko_df.loc[: , ['open', 'high', 'low', 'close']]
        self.renko_df=self.renko_df.reset_index(drop=True)        
        
        #candlestick
        self.df=binance_data.loc[: , ['open', 'high', 'low', 'close']]
        self.df=self.df.reset_index(drop=True)
        self.df=self.df.astype(np.float)

        #dates
        self.dates=binance_data.loc[:, ['date']]
        self.dates=self.dates['date'].apply(lambda x: datetime.fromtimestamp(float(x) / 1000.0))

        self.action_space = ActionSpace()
        self.observation_space = ObservationSpace(self.settings.frame_size * self.df.shape[1])
        self.done=False
        self.current_index=0
        self.buy_price=[]
        self.sell_price=[]
        self.actions_index=[]

        for i in range(1, self.settings.frame_size):
            self.buy_price.append(nan)
            self.sell_price.append(nan)
            self.actions_index.append(i)

    def setAgent(self, agent):
        self.agent=agent

    def reset(self):
        self.buy_price=[]
        self.sell_price=[]
        self.actions_index=[]
        
        for i in range(1, self.settings.frame_size):
            self.buy_price.append(nan)
            self.sell_price.append(nan)
            self.actions_index.append(i)

        self.current_index=0
        observation=self.getNextObservation()
        self.done=self.isDone()        
        return observation

    def getData(self):
        if self.settings.chart_type == 'Candlestick':
            return self.df
        elif self.settings.chart_type == 'Renko':
            return self.renko_df

        return None

    def getPrice(self, action, index):
        if action == -1:
            return self.df['low'].values[index + self.settings.frame_size - 1]
        elif action == 1:
            return self.df['high'].values[index + self.settings.frame_size - 1]

        return 0.0

    def getNumSteps(self):
        if self.settings.chart_type == 'Candlestick':
            return (self.df.shape[0] - self.settings.frame_size) + 1
        elif self.settings.chart_type == 'Renko':
            return (self.renko_df.shape[0] - self.settings.frame_size) + 1

    def isDone(self):
        status=False if self.current_index + self.settings.frame_size - 1 < self.df.shape[0] else True
        return status

    def getNextObservation(self):
        unnormalized_frame=[]
        if self.settings.chart_type == 'Candlestick':
            unnormalized_frame=list(zip(self.df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'open'].values,
                    self.df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'high'].values,
                    self.df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'low'].values,
                    self.df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'close'].values))
        elif self.settings.chart_type == 'Renko':
            unnormalized_frame=list(zip(self.renko_df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'open'].values,
                    self.renko_df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'high'].values,
                    self.renko_df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'low'].values,
                    self.renko_df.loc[self.current_index: self.current_index +
                                self.settings.frame_size - 1, 'close'].values))

        linear=[]
        for ohlc in unnormalized_frame:
            for value in ohlc:
                linear.append(value)
        normalized_frame=[]

        m=np.mean(linear, axis=0)
        std=np.std(linear, axis=0)
        normalized_frame.append(0.5 * (np.tanh(0.01 * ((linear - m) / std)) + 1))
        self.current_index+=1
        normalized_frame=np.array(normalized_frame)
        normalized_frame=normalized_frame.reshape(normalized_frame.shape[0] * normalized_frame.shape[1])
        
        return normalized_frame

    def roundAction(self, action):
        action=action.tolist()
        max_value=max(action)
        index=action.index(max_value)
        return index - 1

    def processFuture(self, action):
        saved_current_index=self.current_index
        reward=-100.0

        open_price=self.getPrice(action, self.current_index)
        if action == 1:
            self.buy_price.append(open_price)
            self.sell_price.append(nan)
        elif action == -1:
            self.buy_price.append(nan)
            self.sell_price.append(open_price)

        self.actions_index.append(self.current_index + self.settings.frame_size - 1)

        observation=self.getNextObservation()
        self.done=self.isDone()

        while not self.done:
            predict_action=self.agent.predict(observation)[0]
            predict_action=self.roundAction(predict_action)            
            if predict_action == -1 or predict_action == 1:
                close_price=self.getPrice(predict_action, self.current_index)
                reward=float(open_price)-float(close_price)
                break
            observation=self.getNextObservation()
            self.done=self.isDone()

        self.current_index=saved_current_index
        return reward

    def getRewardForAction(self, action):
        if action == 0:
            self.buy_price.append(nan)
            self.sell_price.append(nan)
            self.actions_index.append(self.current_index + self.settings.frame_size - 1)
            return 0.0
        
        return self.processFuture(action)

    def step(self, action):
        action=self.roundAction(action)
        reward=self.getRewardForAction(action)
        observation=self.getNextObservation()
        self.done=self.isDone()

        return observation, reward, self.done, {}

    def render(self, mode='human'):
        pass

    def close(self):
        pass