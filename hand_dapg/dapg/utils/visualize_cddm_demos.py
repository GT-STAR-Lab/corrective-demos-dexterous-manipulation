import click
import mj_envs
import numpy as np
import os
import pickle
from mjrl.utils.gym_env import GymEnv
import json
import copy

from torch import save

DESC = '''
Helper script to collect demonstrations via LeapMotion sensor.\n
USAGE:\n
    Collects demonstrations for the env via LeapMotion sensor.\n
    $ python utils/visualize_cddm_demos --env_name relocate-v0\n
'''

def get_empty_demonstration():
    return {
        'actions': np.empty((0, 30)),
        'observations': np.empty((0, 39)),
        'rewards': np.array([]),
        'init_state_dict': {}
    }

def save_demonstration():
    global demonstration, demonstrations, e, failure_cases, index
    demonstrations.append(copy.deepcopy(demonstration))
    print(demonstration['init_state_dict']['obj_pos'])
    print(demonstrations[-1]['init_state_dict']['obj_pos'])
    if failure_cases is not None:
        print("Incremented index")
        index += 1
    with open(user_demo_file_name, 'wb') as demos:
        pickle.dump([d for d in demonstrations], demos)

def reset_demonstration(same_pos, samples_filename=None):
    global demonstration, demonstrations, e, failure_cases, index, SAMPLES_FILENAME
    demonstration = get_empty_demonstration().copy()

    # update the samples filename
    if SAMPLES_FILENAME is None:
        SAMPLES_FILENAME = samples_filename
    e.reset(mode='demos', samples_filename=SAMPLES_FILENAME, same_pos=same_pos)
    if failure_cases is not None:
        print(failure_cases[index])
        e.set_env_state(copy.deepcopy(failure_cases[index]))
        print("Set state to failure case")
    demonstration['init_state_dict'] = copy.deepcopy(e.get_env_state())
    print(demonstration['init_state_dict']['obj_pos'])

def initialize_data_files(user_id, failure_file, samples_filename=None):
    global user_demo_file_name, demonstrations, index
    
    user_folder_name = '/home/kolb/GT/CoRX/hand_dapg/dapg/study_data/' + user_id
    
    if failure_file is None:
        if samples_filename is None:
            user_demo_file_name = user_folder_name + '/' + user_id + '_30_demos.pickle' 
        else:
            user_demo_file_name = user_folder_name + '/' + user_id + '_' + samples_filename + '_demos.pickle'
    else:
        user_demo_file_name = failure_file.replace('failures', 'corrections') 
        # This is hacky. We'll need to make sure we collect the corrections for failures
        # for the same user_id.
    
    print('Storing demonstrations to', user_demo_file_name)
    
    if os.path.exists(user_folder_name):
        if os.path.exists(user_demo_file_name):
            with open(user_demo_file_name, 'rb') as demo_file:
                demonstrations = copy.deepcopy(pickle.load(demo_file))
                index = len(demonstrations)
    else:
        os.makedirs(user_folder_name)
        os.makedirs(user_folder_name + '/policies')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_30_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_20_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_15_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_10_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_20_10_1_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_15_15_1_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_10_20_1_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_20_10_2_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_15_15_2_policy')
        os.makedirs(user_folder_name + '/policies/' + user_id + '_10_20_2_policy')
        os.makedirs(user_folder_name + '/failures')
        os.makedirs(user_folder_name + '/corrections')
        os.makedirs(user_folder_name + '/configs')

e = None

collect_demos = False

save_demo = None

demonstration = get_empty_demonstration().copy()

SAMPLES_FILENAME = None

demonstrations = []

failure_cases = None

index = 0

####################
# Server Code start
####################

from flask import Flask, request
import logging
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/set', methods=['GET'])
def setter():
    data = json.loads(request.args.get('data'))
    demo_step(data)
    return ''

@app.route('/record', methods=['GET'])
def record_setter():
    data = request.args.get('data')
    global collect_demos
    collect_demos = int(data) == 1
    print("record", data, collect_demos)
    return ''

@app.route('/save', methods=['GET'])
def save_setter():
    data = request.args.get('data')
    global save_demo
    save_demo = int(data) == 1
    print("save", data, save_demo)
    if save_demo:
        save_demonstration()
    reset_demonstration(same_pos=not save_demo, samples_filename=SAMPLES_FILENAME)
    return ''

##################
# Server Code end
##################

# MAIN =========================================================
@click.command(help=DESC)
@click.option('--env_name', type=str, help='environment to load', required= True)
@click.option('--failure_file',type=str, help='absolute path of the file with failure scenarios to be corrected', required=False, default=None)
@click.option('--samples_filename', type=str, help='filename for the sampling file, NOT THE PATH', required=False, default=30)
def main(env_name, failure_file, samples_filename):
    if env_name is "":
        print("Unknown env.")
        return
    # initialize the environment and start server
    global demonstration, e, failure_cases
    if failure_file is not None:
        failure_cases = pickle.load(open(failure_file, 'rb'))
    #print('# Failure Cases:', len(failure_cases))
    user_id = input('Enter User ID: ')
    initialize_data_files(user_id, failure_file, samples_filename)
    e = GymEnv(env_name)
    reset_demonstration(same_pos=True, samples_filename=samples_filename)
    app.run(port=5000)

def compute_vector_angle(a, b):
    # adapted from (https://www.quora.com/How-do-I-find-the-angle-of-a-3D-vector-i-e-A-2i-3j-5k)
    if (np.array_equal(a, np.zeros_like(a)) or np.array_equal(b, np.zeros_like(b))):
        return 0
    theta = np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    return theta

# converts joint radians to [-1,1] scale for the hand
def convert_joint_angle_to_mujoco_scale(radians):
    deg = np.rad2deg(radians)  # radians to degrees
    clamp = max(min(deg, 90), 0)
    scale = clamp / 90 * 2 - 1  # scales from -1 to 1
    return scale

def centeredWrist(pose):
    _p = pose[30][1] # wrist position (looks like a sweep rn)
    # goes between 47 and 300, -1.0, 1.0
    if _p > 300:
        _p = 344
    elif _p <= 45:
        _p = 0
    _p = int(_p)
    space = np.arange(-1.0, 1.0, 2.0/345.0)
    return (-1.0)*space[_p]

def compute_bone_angle(pose):
    actions = np.zeros((30,))

    # WRJ1: wrist
    actions[0], actions[1], actions[2] = (-.005)*pose[0]

    # WRJ0: palm

    # FFJ3: pointer knuckle

    # FFJ2: pointer proximal
    actions[9] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[3], pose[4]))

    # FFJ1: pointer middle
    actions[10] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[4], pose[5]))
    
    # FFJ0: pointer distal
    actions[11] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[5], pose[6]))

    # MFJ2: middle proximal
    actions[13] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[8], pose[9]))
    
    # MFJ1: middle middle
    actions[14] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[9], pose[10]))

    # MFJ0: middle distal
    actions[15] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[10], pose[11]))

    # RFJ2: ring proximal
    actions[17] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[13], pose[14]))
    
    # RFJ1: ring middle
    actions[18] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[14], pose[15]))

    # RFJ0: ring distal
    actions[19] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[15], pose[16]))

    # RFJ0: little knuckle
    actions[21] = -0.5 # adjusting the yaw since the rest position is too close to the ring finger

    # LFJ2: little proximal
    actions[22] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[19], pose[20]))
    
    # LFJ1: little middle
    actions[23] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[20], pose[21]))

    # LFJ0: little distal
    actions[24] = convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[21], pose[22]))

    # THJ3a
    actions[25] = 0

    # THJ3b
    actions[26] = .75
        
    # THJ2: thumb proximal
    actions[27] = 0
    
    # THJ1: thumb middle
    actions[28] = -.25

    # THJ0: thumb distal
    actions[29] = -convert_joint_angle_to_mujoco_scale(compute_vector_angle(pose[27], pose[28]))

    # TODO: Figure out the mapping and add basis vectors
    actions[3] = centeredWrist(pose)
    #j#min(pose[30][1]/300, 1.0)#j #max(min((-1)*pose[30][1], 0.0)/90.0, 30.0)#j

    return actions

def demo_step(pose):
    pose = np.array(pose) # convert to np array
    actions = compute_bone_angle(pose)
    global demonstration, demonstrations, e
        
    # 0 - forearm left
    # 1 - forearm up
    # 2 - forearm forward
    # 3 - forearm pitch down
    # 4 - forearm yaw left
    # 5 - forearm roll clockwise
    # 6 - wirst yaw left
    # 7 - wrist pitch down
    # 8 - pointer knuckle (yaw left)
    # 9 - pointer proximal (pitch down)
    # 10 - pointer middle (pitch down)
    # 11 - pointer distal (pitch down)
    # 12 - middle knuckprint('wirsts' + str(pose[30]))mal
    # 23 - little middle
    # 24 - little distal
    # 25 - thumb metacarpal knuckle (yaw left - but awkwardly bc ball joint)
    # 26 - thumb metacarpal proximal (pitch down - but awkwardly because ball joint)
    # 27 - thumb proximal (yaw left)
    # 28 - thumb middle
    # 29 - thumb distal

    global collect_demos
    pass_threshold = 25 * 4  # number of consecutive frames in which the ball must be at the target
    if e.env.num_success_run < pass_threshold:
        o, r, _, _ = e.step(actions) # move the hand in simulation

        e.env.mj_render() # render the simulation
    
        demonstration['actions'] = np.append(demonstration['actions'], np.array(actions).reshape(1, 30), axis=0)
        demonstration['observations'] = np.append(demonstration['observations'], np.array(o).reshape(1, 39), axis=0)
        demonstration['rewards'] = np.append(demonstration['rewards'], [r], axis=0)

    else:
        collect_demos = False


if __name__ == '__main__':
    main()