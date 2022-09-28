from PySide6.QtCore import QRunnable, Slot, QThreadPool
from neural_network.agent import Agent
from neural_network.environment import Environment

from widgets.episode_end_widget import EpisodeEndWidget

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

        agent.signals.on_episode_begin.connect(self.onEpisodeBegin)
        agent.signals.on_episode_end.connect(self.onEpisodeEnd)

        env.setAgent(agent)
        agent.learn(self.epohs)

    @Slot()
    def onEpisodeBegin(self):
        pass

    @Slot()
    def onEpisodeEnd(self):
        #TODO remove UI from this file
        widget=EpisodeEndWidget()
        widget.exec_()
