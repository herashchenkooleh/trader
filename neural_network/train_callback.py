from PySide6.QtCore import QObject, Signal
from ast import Call
from rl.callbacks import Callback

class TrainCallback(Callback):
    class TrainCallbackSignals(QObject):
        on_episode_begin=Signal()
        on_episode_end=Signal()

    def __init__(self) -> None:
        super().__init__()
        self.signals=TrainCallback.TrainCallbackSignals()

    def on_episode_begin(self, episode, logs={}):
        self.signals.on_episode_begin.emit()

    def on_episode_end(self, episode, logs={}):
        self.signals.on_episode_end.emit()

    def on_step_begin(self, step, logs={}):
        print("Begin step: ", step)

    def on_step_end(self, step, logs={}):
        print("End step: ", step)

    def on_action_begin(self, action, logs={}):
        print("Begin action: ", action)

    def on_action_end(self, action, logs={}):
        print("End action: ", action)

