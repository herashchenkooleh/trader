from agent import Agent
from environment import Environment

if __name__=='__main__':
    env=Environment(20, 'BTCUSDT', '5m', '9/01/2022 10:00', '9/13/2022 10:00')
    agent=Agent(env)
    observation=env.reset()

    sum_reward=0
    while True:
        action=agent.predict(observation)
        observation, reward, done, _=env.step(action)
        env.render()
        sum_reward+=reward
        if done:
            print('Done! Final profit: ', sum_reward)
            break

    env.close()