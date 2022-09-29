from PySide6.QtCore import QObject, Signal
from rl.callbacks import Callback

class TrainCallback(Callback):
    class Signals(QObject):
        on_episode_begin=Signal()
        on_episode_end=Signal()
        on_step_begin=Signal(int)
        on_step_end=Signal(int)
        on_action_begin=Signal(list)
        on_action_end=Signal(list)

    def __init__(self) -> None:
        super().__init__()
        self.signals=TrainCallback.Signals()

    def on_episode_begin(self, episode, logs={}):
        self.signals.on_episode_begin.emit()

    def on_episode_end(self, episode, logs={}):
        self.signals.on_episode_end.emit()

    def on_step_begin(self, step, logs={}):
        self.signals.on_step_begin.emit(int(step))

    def on_step_end(self, step, logs={}):
        self.signals.on_step_end.emit(int(step))

    def on_action_begin(self, action, logs={}):
        self.signals.on_action_begin.emit(action)

    def on_action_end(self, action, logs={}):
        self.signals.on_action_end.emit(action)
