import math
import random
import numpy as np
import pickle
import matplotlib.pyplot as plt


# Halton sampler
def sample_space_halton(N, B1=2, B2=3):
    points = np.zeros((N, 5))

    # define a halton sampler
    def sample_halton(i, base):
        current = 1
        result = 0
        while i > 0:
            current = current / base
            result = result + current * (i % base)
            i = math.floor(i / base)
        return result
    
    # generate the points
    for i in range(N):
        ## BALL LOCATION
        ball_x = sample_halton(i+1, B1)
        ball_y = sample_halton(i+1, B2)

        ## TARGET LOCATION
        target_x = random.random()
        target_y = random.random()
        target_z = random.random()

        points[i,:] = np.array([ball_x, ball_y, target_x, target_y, target_z])
    
    return points


# random sampler
# inputs:
#   N: number of points
#   xrange: [int:min, int:max]
#   yrange: [int:min, int:max]
def sample_space_random(N):
    points = np.random.random((N, 5))
    return points


# generates initial states for training on a smaller area than testing
def generate_and_store_initial_states_different_geometry():
    #np.random.seed(42)

    # generate the training points
    for train_N in [10, 20, 30]:
        train_points = sample_space_random(train_N)

        train_ballx = 0.144337567  # ball x: -.144, .144
        train_points[:,0] = (train_points[:,0] * 2 - 1) * train_ballx

        train_bally = 0.144337567  # ball y: -.144, .144
        train_points[:,1] = (train_points[:,1] * 2 - 1) * train_bally

        train_targetx = 0.144337567  # target x: -.144, .144
        train_points[:,2] = (train_points[:,2] * 2 - 1) * train_targetx

        train_targety = 0.144337567  # target y: -.144, .144
        train_points[:,3] = (train_points[:,3] * 2 - 1) * train_targety
        
        train_targetz = 0.15  # target z: .15, .35
        train_points[:,4] = (train_points[:,4] * .2) + train_targetz  # target z

        # save the samples
        with open("/home/kolb/GT/CoRX/hand_dapg/data/training_initial_states_" + str(train_N) + ".pickle", "wb") as f:
            pickle.dump(train_points, f)

    print("Generated training states")


    # generate the testing points
    for test_N in [10, 20, 1000]:
        test_points = sample_space_random(test_N)

        test_ballx_min = 0.144337567  # ball x: -.144, .144
        test_ballx_max = 0.25

        test_bally_min = 0.144337567  # ball y: -.144, .144
        test_bally_max = 0.25

        # scale the ball x
        test_points[:,0] = (test_points[:,0] * 2 - 1) * test_ballx_max

        # scale the ball y
        test_points[:,1] = (test_points[:,1] * 2 - 1) * test_bally_max

        # where abs(y) is less than y min, ensure x is outside area
        test_points[:,0] = np.where(
            (np.abs(test_points[:,1]) < test_bally_min) & (np.abs(test_points[:, 0]) < test_ballx_min) & (np.abs(test_points[:, 0]) > np.abs(test_points[:, 1])),
            (test_points[:,0] * (test_ballx_max-test_ballx_min) / test_ballx_max) + (test_ballx_min * np.sign(test_points[:,0])),
            test_points[:,0])
        
        # where abs(x) is less than x min, ensure y is outside area
        test_points[:,1] = np.where(
            (np.abs(test_points[:,1]) < test_bally_min) & (np.abs(test_points[:, 0]) < test_ballx_min) & (np.abs(test_points[:, 0]) < np.abs(test_points[:, 1])),
            (test_points[:,1] * (test_ballx_max-test_ballx_min) / test_ballx_max) + (test_ballx_min * np.sign(test_points[:,1])),
            test_points[:,1])

        test_targetx_min = 0.144337567  # target x: +- .144, +- .25
        test_targetx_max = 0.25

        test_targety_min = 0.144337567  # target y: +- .144, +- .25
        test_targety_max = 0.25

        # scale the target x
        test_points[:, 2] = (test_points[:, 2] * 2 - 1) * test_targetx_max

        # scale the target y
        test_points[:, 3] = (test_points[:, 3] * 2 - 1) * test_targety_max

        # where abs(y) is less than y min, ensure x is outside area
        test_points[:, 2] = np.where(
            (np.abs(test_points[:, 3]) < test_bally_min) & (np.abs(test_points[:, 2]) < test_ballx_min) & (np.abs(test_points[:, 2]) > np.abs(test_points[:, 3])),
            (test_points[:, 2] * (test_ballx_max-test_ballx_min) / test_ballx_max) + (test_ballx_min * np.sign(test_points[:, 2])),
            test_points[:, 2])
        
        # where abs(x) is less than x min, ensure y is outside area
        test_points[:, 3] = np.where(
            (np.abs(test_points[:, 3]) < test_bally_min) & (np.abs(test_points[:, 2]) < test_ballx_min) & (np.abs(test_points[:, 2]) < np.abs(test_points[:, 3])),
            (test_points[:, 3] * (test_ballx_max-test_ballx_min) / test_ballx_max) + (test_ballx_min * np.sign(test_points[:, 3])),
            test_points[:, 3])

        test_targetz = 0.15  # target z: .15, .35
        test_points[:,4] = (test_points[:,4] * .2) + test_targetz  # target z

        # save the samples
        with open("/home/kolb/GT/CoRX/hand_dapg/data/testing_initial_states_" + str(test_N) + ".pickle", "wb") as f:
            pickle.dump(test_points, f)

    print("Generated testing states")


    # plotting verification
    fig = plt.figure(figsize=plt.figaspect(.5))

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_xlim([-.3, .3])
    ax1.set_ylim([-.3, .3])
    
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')

    for train_N in [10, 20, 30]:
        f = open('/home/kolb/GT/CoRX/hand_dapg/data/training_initial_states_' + str(train_N) + '.pickle', 'rb')
        training = pickle.load(f)
        f.close()
        
        ax1.scatter(training[:,0], training[:,1])
        ax2.scatter(training[:,2], training[:,3], training[:,4])
        
    
    for test_N in [10, 20]:
        f = open('/home/kolb/GT/CoRX/hand_dapg/data/testing_initial_states_' + str(test_N) + '.pickle', 'rb')
        testing = pickle.load(f)
        f.close()

        ax1.scatter(testing[:,0], testing[:,1])
        ax2.scatter(testing[:,2], testing[:,3], testing[:,4])
    
    plt.show()


# generates initial states for testing and training on the SAME area
def generate_and_store_initial_states_same_geometry():
    """
    Generates and stores the initial ball and target states to a file.
    """

    N = 30
    points = sample_space_halton(N)
    
    points[:,0] = (points[:,0] * 2 - 1) * 0.1 # map ball x to -0.15 to 0.15
    points[:,1] = (points[:,1] * 0.45) - 0.1 # map ball y to -0.15 to 0.3
    points[:,2:4] = (points[:,2:4] * 2 - 1) * 0.15 # map target x and y to -0.2 to 0.2
    points[:,4] = (points[:,4] * .2) + .15 # map target z to 0.15 to 0.35

    with open("/home/abhineet/IRL/CoRX/hand_dapg/data/training_initial_states.pickle", "wb") as f:
        pickle.dump(points, f)

    # with open("/home/abhineet/IRL/CoRX/hand_dapg/data/test_initial_states.pickle", "wb") as f:
    #     pickle.dump(points[500:], f)

    print("Generated training and testing states")

    # plotting verification
    fig = plt.figure(figsize=plt.figaspect(.5))
   
    with open("/home/abhineet/IRL/CoRX/hand_dapg/data/training_initial_states.pickle", "rb") as f:
        training = pickle.load(f)

        ax1 = fig.add_subplot(1, 2, 1)
        ax1.scatter(training[:,0], training[:,1])

        ax2 = fig.add_subplot(1, 2, 2, projection='3d')
        ax2.scatter(training[:,2], training[:,3], training[:,4])

    
    # with open("/home/abhineet/IRL/CoRX/hand_dapg/data/test_initial_states.pickle", "rb") as f:
    #     testing = pickle.load(f)

    #     ax1 = fig.add_subplot(2, 2, 3)
    #     ax1.scatter(testing[:,0], testing[:,1])

    #     ax2 = fig.add_subplot(2, 2, 4, projection='3d')
    #     ax2.scatter(testing[:,2], testing[:,3], testing[:,4])
    
    plt.show()

generate_and_store_initial_states_different_geometry()