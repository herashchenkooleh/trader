from PySide6.QtCore import QRunnable, QThreadPool

class TrainWorker(QRunnable):
    def __init__(self, agent, settings) -> None:
        super().__init__()
        self.agent=agent
        self.settings=settings

    def start(self):
        QThreadPool.globalInstance().start(self)

    def run(self):
        self.agent.init()
        self.agent.learn(self.settings.epochs)