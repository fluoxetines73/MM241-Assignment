import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
<<<<<<< HEAD
NUM_EPISODES = 2

if __name__ == "__main__":
    # # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test GreedyPolicy
    # print("Test GreedyPolicy")
    # print(len(observation["products"]))
    # print(observation["products"])
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         ep += 1

    # # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test RandomPolicy
    # print ("Test RandomPolicy")
    # print(len(observation["products"]))
    # print(observation["products"])
    # rd_policy = RandomPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = rd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         ep += 1

    # Uncomment the following code to test your policy
=======
NUM_EPISODES = 3

if __name__ == "__main__":
>>>>>>> 8b92d5a1c9ccdbffaecc521e57264835cd2f2826
    # # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test GreedyPolicy
    # print("Test GreedyPolicy")
    # # print (observation["products"])
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         # print (observation["products"])

    #         ep += 1

    # # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test RandomPolicy
    # print ("Test RandomPolicy")
    # # print (observation["products"])

    # rd_policy = RandomPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = rd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         # print (observation["products"])
    #         ep += 1

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

    # # Test Policy2210xxx
    # print ("Test Policy2210xxx")
    # # print (observation["products"])
    # policy2210xxx = Policy2210xxx()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = policy2210xxx.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         # print (observation["products"])
    #         ep += 1

    ##################### same environment for all policies #####################
    # Reset the environment
    observation0, info0 = observation1, info1 = observation2, info2 = env.reset(seed=42)

<<<<<<< HEAD
    # Test Policy2210xxx
    print ("Test Policy2210xxx")
    print(len(observation["products"]))
    print(observation["products"])
    policy2210xxx = Policy2210xxx()
=======
>>>>>>> 8b92d5a1c9ccdbffaecc521e57264835cd2f2826
    ep = 0
    while ep < NUM_EPISODES:
        print ("==================== Episode {} ====================".format(ep))
        # Test GreedyPolicy
        print("Test GreedyPolicy")
        print (len(observation0["products"]))
        gd_policy = GreedyPolicy()
        while True:
            action = gd_policy.get_action(observation0, info0)
            observation0, reward, terminated, truncated, info0 = env.step(action)

            if terminated or truncated:
                print(info0)
                observation0, info0 = env.reset(seed=ep)
                break

        # Test RandomPolicy
        print ("Test RandomPolicy")
        print(len(observation1["products"]))
        rd_policy = RandomPolicy()
        while True:
            action = rd_policy.get_action(observation1, info1)
            observation1, reward, terminated, truncated, info1 = env.step(action)

            if terminated or truncated:
                print(info1)
                observation1, info1 = env.reset(seed=ep)
                break

        # Test Policy2210xxx
        print ("Test Policy2210xxx")
        print(len(observation2["products"]))
        policy2210xxx = Policy2210xxx()
        while True:
            action = policy2210xxx.get_action(observation2, info2)
            observation2, reward, terminated, truncated, info2 = env.step(action)

            if terminated or truncated:
                print(info2)
                observation2, info2 = env.reset(seed=ep)
                break

        ep += 1
        observation0, info0 = observation1, info1 = observation2, info2 = env.reset(seed=42)


<<<<<<< HEAD
        if terminated or truncated:
            print(info)
            observation, info = env.reset(seed=ep)
            print(len(observation["products"]))
            print(observation["products"])
            ep += 1
=======
>>>>>>> 8b92d5a1c9ccdbffaecc521e57264835cd2f2826

env.close()
