from PySide6.QtCore import QRunnable, QThreadPool

from core.nn.agent import Agent
from core.nn.trading_env import TradingEnv

class TrainingWorker(QRunnable):
    def __init__(self, settings) -> None:
        super().__init__()
        self.settings=settings
        self.env=TradingEnv(self.settings)
        self.agent=Agent(self.env)

    def start(self):
        QThreadPool.globalInstance().start(self)

    def run(self):
        self.agent.init()
        self.agent.learn(self.settings.epochs)