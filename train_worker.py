from PySide6.QtCore import QRunnable, Slot, QThreadPool
from neural_network.agent import Agent
from neural_network.environment import Environment

class TrainWorker(QRunnable):
    def __init__(self, binance_manager, frame_size, symbol, interval, start_time, end_time, epohs=500) -> None:
        super().__init__()
        self.binance_manager=binance_manager
        self.frame_size=frame_size
        self.symbol=symbol
        self.interval=interval
        self.start_time=start_time
        self.end_time=end_time
        self.epohs=epohs

        QThreadPool.globalInstance().start(self)

    @Slot()
    def run(self):
        env=Environment(self.binance_manager, self.frame_size, self.symbol, self.interval, self.start_time, self.end_time)
        agent=Agent(env)
        env.setAgent(agent)
        agent.learn(self.epohs)    