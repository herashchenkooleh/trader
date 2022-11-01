from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam
import tensorflow.keras as tfk
import tensorflow as tf
tf.keras.backend.set_floatx("float64")
import tensorflow_probability as tfp
tfd = tfp.distributions

from tf_agents.agents.ddpg import ddpg_agent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess

from PySide6.QtCore import QObject, Signal

from core.nn.training_callback import TrainingCallback

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
        n_batches=10
        prior = tfd.Independent(tfd.Normal(loc=tf.zeros(self.env.action_space.shape[0], dtype=tf.float64), scale=1.0), reinterpreted_batch_ndims=1)
        self.actor=tfk.Sequential([
                tfk.layers.InputLayer(input_shape=(self.env.observation_space.shape[0],), name="input"),
                tfk.layers.Dense(self.env.observation_space.shape[0], activation="relu", name="dense_1"),
                tfk.layers.Dense(tfp.layers.MultivariateNormalTriL.params_size(
                self.env.action_space.shape[0]), activation=None, name="distribution_weights"),
                tfp.layers.MultivariateNormalTriL(event_size=self.env.action_space.shape[0], activity_regularizer=tfp.layers.KLDivergenceRegularizer(prior, weight=1/n_batches), name="output")], name="model")

    def learn(self, epochs):
        action_input=Input(shape=(self.env.action_space.shape[0],), name='action_input')
        observation_input=Input(shape=(self.env.observation_space.shape[0],), name='observation_input')
        flattened_observation=Flatten()(observation_input)
        x=Concatenate()([action_input, flattened_observation])
        x=Dense(self.env.observation_space.shape[0], use_bias=True)(x)
        x=Activation('relu')(x)
        x=Dense(self.env.observation_space.shape[0] / 2, use_bias=True)(x)
        x=Activation('relu')(x)
        x=Dense(1)(x)
        x=Activation('linear')(x)
        critic=Model(inputs=[action_input, observation_input], outputs=x)
        memory=SequentialMemory(limit=self.env.getNumSteps() * epochs, window_length=1)
        random_process=OrnsteinUhlenbeckProcess(size=self.env.action_space.shape[0], theta=.05, mu=0., sigma=.1)

        custom_model_objects = { 'MultivariateNormalTriL': tfp.layers.MultivariateNormalTriL }
        self.agent=ddpg_agent.DdpgAgent(nb_actions=self.env.action_space.shape[0], actor=self.actor, critic=critic, critic_action_input=action_input,
                             memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                             random_process=random_process, gamma=.99, target_model_update=1e-3, 
                             custom_model_objects=custom_model_objects)
        
        self.agent.compile(Adam(learning_rate=.001, clipnorm=1.), metrics=['mae'])
        self.callback=TrainingCallback(self.env, self.settings)

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
        predicted_action=self.actor.predict(observation.reshape((1, observation.shape[0])))
        return predicted_action