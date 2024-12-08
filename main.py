import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx

import random

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 15

if __name__ == "__main__":
    # Reset the environment
    observation, info = env.reset(seed=42)

    # # Test GreedyPolicy
    # print("Testing GreedyPolicy")
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         ep += 1

    # # # Reset the environment
    # # observation, info = env.reset(seed=42)

    # # # Test RandomPolicy
    # # rd_policy = RandomPolicy()
    # # ep = 0
    # # while ep < NUM_EPISODES:
    # #     action = rd_policy.get_action(observation, info)
    # #     observation, reward, terminated, truncated, info = env.step(action)

    # #     if terminated or truncated:
    # #         print(info)
    # #         observation, info = env.reset(seed=ep)
    # #         ep += 1

    # # Uncomment the following code to test your policy
    # # # Reset the environment
    # # observation, info = env.reset(seed=42)
    # # print(info)

    # # policy2210xxx = Policy2210xxx()
    # # for _ in range(200):
    # #     action = policy2210xxx.get_action(observation, info)
    # #     observation, reward, terminated, truncated, info = env.step(action)
    # #     print(info)

    # #     if terminated or truncated:
    # #         observation, info = env.reset()

    # # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test First Fit Decreasing Policy
    # print("Testing First Fit Decreasing Policy")
    # policy2210 = Policy2210xxx()
    # ep = 0

    # while ep < NUM_EPISODES:
    #     action = policy2210.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         ep += 1

    ##################### Test all policy in one loop #####################
    # create seed list for each episode by random
    seeds = random.sample(range(100), NUM_EPISODES)
    seeds[0] = 42
    print(seeds)

    # Test all policies
    print("Testing all policies")
    policies = [GreedyPolicy(), Policy2210xxx()]
    ep = 0
    while ep < NUM_EPISODES:
        print ("\n==================== Episode {} ====================".format(ep))
        # reset the environment
        observation, info = env.reset(seed=seeds[ep])
        # print env information
        print("size of stocks: ", len(observation["stocks"]))
        print("size of products: ", len(observation["products"]))
        print("total quantity of products: ", sum([prod["quantity"] for prod in observation["products"]]))
        print("total area of products: ", sum([prod["size"][0] * prod["size"][1] * prod["quantity"] for prod in observation["products"]]))

        for i, policy in enumerate(policies):
            print("\nTesting {} Policy".format(policy.__class__.__name__))
            if i != 0:
                observation, info = env.reset(seed=seeds[ep])
            while True:
                action = policy.get_action(observation, info)
                observation, reward, terminated, truncated, info = env.step(action)

                if terminated or truncated:
                    print(info)
                    break

        ep += 1
            



env.close()