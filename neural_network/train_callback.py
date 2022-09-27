from PySide6.QtWidgets import QDialog
from ast import Call
from rl.callbacks import Callback

class TrainCallback(Callback):
    def on_episode_begin(self, episode, logs={}):
        print("Begin episode: ", episode)

    def on_episode_end(self, episode, logs={}):
        print("End episode: ", episode)

    def on_step_begin(self, step, logs={}):
        print("Begin step: ", step)

    def on_step_end(self, step, logs={}):
        print("End step: ", step)

    def on_action_begin(self, action, logs={}):
        print("Begin action: ", action)

    def on_action_end(self, action, logs={}):
        print("End action: ", action)

