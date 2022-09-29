from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess

from PySide6.QtCore import QObject, Signal

from core.train_callback import TrainCallback

class Agent(object):
    class Signals(QObject):
        on_episode_begin=Signal()
        on_episode_end=Signal()
        on_step_begin=Signal(int)
        on_step_end=Signal(int)
        on_action_begin=Signal(list)
        on_action_end=Signal(list)

    def __init__(self, env):
        self.env=env
        self.signals=Agent.Signals()

    def init(self, file_path=''):
        self.actor=Sequential()
        self.actor.add(Flatten(input_shape=(1,) + (self.env.observation_space.shape[0],)))
        self.actor.add(Dense(self.env.observation_space.shape[0], use_bias=True))
        self.actor.add(Activation('relu'))
        self.actor.add(Dense(self.env.observation_space.shape[0], use_bias=True))
        self.actor.add(Activation('relu'))
        self.actor.add(Dense(self.env.observation_space.shape[0], use_bias=True))
        self.actor.add(Activation('relu'))
        self.actor.add(Dense(self.env.observation_space.shape[0], use_bias=True))
        self.actor.add(Activation('relu'))
        self.actor.add(Dense(self.env.observation_space.shape[0], use_bias=True))
        self.actor.add(Activation('relu'))
        self.actor.add(Dense(self.env.observation_space.shape[0], use_bias=True))
        self.actor.add(Activation('relu'))
        self.actor.add(Dense(self.env.observation_space.shape[0], use_bias=True))
        self.actor.add(Activation('relu'))
        self.actor.add(Dense(self.env.action_space.shape[0], use_bias=True))
        self.actor.add(Activation('sigmoid'))

    def learn(self, epochs):
        action_input=Input(shape=(self.env.action_space.shape[0],), name='action_input')
        observation_input=Input(shape=(1,) + (self.env.observation_space.shape[0],), name='observation_input')
        flattened_observation=Flatten()(observation_input)
        x=Concatenate()([action_input, flattened_observation])
        x=Dense(8, use_bias=False)(x)
        x=Activation('relu')(x)
        x=Dense(5, use_bias=True)(x)
        x=Activation('relu')(x)
        x=Dense(1)(x)
        x=Activation('linear')(x)
        critic=Model(inputs=[action_input, observation_input], outputs=x)
        memory=SequentialMemory(limit=self.env.getNumSteps() * epochs, window_length=1)
        random_process=OrnsteinUhlenbeckProcess(size=self.env.action_space.shape[0], theta=.15, mu=0., sigma=.3)

        self.agent=DDPGAgent(nb_actions=self.env.action_space.shape[0], actor=self.actor, critic=critic, critic_action_input=action_input,
                             memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                             random_process=random_process, gamma=.99, target_model_update=1e-3)

        self.agent.compile(Adam(learning_rate=.001, clipnorm=1.), metrics=['mae'])
        self.callback=TrainCallback()

        self.callback.signals.on_episode_begin.connect(self.signals.on_episode_begin)
        self.callback.signals.on_episode_end.connect(self.signals.on_episode_end)
        self.callback.signals.on_step_begin.connect(self.signals.on_step_begin)
        self.callback.signals.on_step_end.connect(self.signals.on_step_end)
        self.callback.signals.on_action_begin.connect(self.signals.on_action_begin)
        self.callback.signals.on_action_end.connect(self.signals.on_action_end)

        callbacks=[self.callback]
        self.agent.fit(self.env, nb_steps=self.env.getNumSteps() * epochs, callbacks=callbacks, visualize=True, verbose=0, nb_max_episode_steps=self.env.getNumSteps())

    def test(self, epochs):
        self.agent.test(self.env, nb_episodes=5, visualize=True, nb_max_episode_steps=epochs)

    def predict(self, observation):
        predicted_action=self.actor.predict(observation.reshape((1,1,observation.shape[0])))
        return predicted_action