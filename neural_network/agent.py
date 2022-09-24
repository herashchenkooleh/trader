from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess

class Agent(object):
    def __init__(self, env):
        self.env=env
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

        self.agent.fit(self.env, nb_steps=self.env.getNumSteps() * epochs, visualize=True, verbose=1, nb_max_episode_steps=self.env.getNumSteps())

    def test(self, epochs):
        self.agent.test(self.env, nb_episodes=5, visualize=True, nb_max_episode_steps=epochs)

    def predict(self, observation):
        predicted_action=self.actor.predict(observation.reshape((1,1,observation.shape[0])))
        return predicted_action