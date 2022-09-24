from trading.binance_manager import BinanceManager
import rl.core as krl
import random
import numpy as np
import pandas as pd
import datetime

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
        print(inputs)
        self.shape = (inputs,)

    def sample(self, seed=None):
        pass

    def contains(self, x):
        pass

class Environment(krl.Env):
    def __init__(self, binance, inputs, symbol, interval, start_time, end_time) -> None:
        super().__init__()
        self.binance=binance
        self.df=self.getData(symbol, interval, start_time, end_time)
        self.frame_size=inputs
        self.action_space = ActionSpace()
        self.observation_space = ObservationSpace(inputs * self.df.shape[1])
        self.done=False
        self.current_index=0

    def setAgent(self, agent):
        self.agent=agent

    def getData(self, symbol, interval, start_time, end_time):
        start_timestamp=str(datetime.datetime.strptime(start_time, "%d/%m/%Y %H:%M").timestamp())
        end_timestamp=str(datetime.datetime.strptime(end_time, "%d/%m/%Y %H:%M").timestamp())
        df=pd.DataFrame(self.binance.get_futures_historical_klines(symbol, interval, start_timestamp, end_timestamp))
        df=df.drop(columns=[0, 6, 11])
        df=df.reset_index(drop=True)
        df.columns=['Open', 'High', 'Low', 'Close', 'Volume', 'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume']

        return df

    def reset(self):
        #print('reset')
        self.current_index=0
        observation=self.getNextObservation()
        self.done=self.isDone()        
        return observation

    def getPrice(self, action, index):
        if action == -1:
            return self.df['Low'].values[index + self.frame_size - 1]
        elif action == 1:
            return self.df['High'].values[index + self.frame_size - 1]
        else:
            return 0.0

    def getNumSteps(self):
        return (self.df.shape[0] - self.frame_size) + 1

    def isDone(self):
        status=False if self.current_index + self.frame_size - 1 < self.df.shape[0] else True
        return status

    def getNextObservation(self):
        unnormalized_frame=np.array([
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'Open'].values,
            self.df.loc[self.current_index: self.current_index +
                        self.frame_size - 1, 'High'].values,
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
        ]).astype(np.float)
        normalized_frame=[]
        for unnormalized_data in unnormalized_frame:
            m=np.mean(unnormalized_data, axis=0)
            std=np.std(unnormalized_data, axis=0)
            normalized_frame.append(0.5 * (np.tanh(0.01 * ((unnormalized_data - m) / std)) + 1))
        self.current_index+=1
        normalized_frame=np.array(normalized_frame)
        normalized_frame=normalized_frame.reshape(normalized_frame.shape[0] * normalized_frame.shape[1])
        return normalized_frame

    def roundAction(self, action):
        action=action.tolist()
        max_value=max(action)
        if max_value > 0.95:
            index=action.index(max_value)
            return index - 1
        return 0

    def processFuture(self, action):
        saved_current_index=self.current_index
        reward=-100.0

        open_price=self.getPrice(action, self.current_index)
        #print('open price: ', open_price)

        observation=self.getNextObservation()
        self.done=self.isDone()

        while not self.done:
            predict_action=self.agent.predict(observation)[0]
            predict_action=self.roundAction(predict_action)            
            if predict_action == -1 or predict_action == 1:
                close_price=self.getPrice(predict_action, self.current_index)
                reward=float(open_price)-float(close_price)
                #print('close price: ', close_price, predict_action, reward)
                break
            observation=self.getNextObservation()
            self.done=self.isDone()

        self.current_index=saved_current_index
        return reward

    def getRewardForAction(self, action):
        if action == 0:
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