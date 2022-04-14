import mj_envs
import click 
import os
import gym
import numpy as np
import pickle
import copy
from mjrl.utils.gym_env import GymEnv

DESC = '''
Helper script to visualize policy (in mjrl format).\n
USAGE:\n
    Visualizes policy on the env\n
    $ python utils/visualize_policy_on_demos.py --env_name relocate-v0 --policy policies/relocate-v0.pickle --mode evaluation
'''

demos_init = [
    {'hand_qpos': np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]),
       'obj_pos': np.array([-0.04865227,  0.25011298,  0.035     ]),
       'target_pos': np.array([-0.12232168,  0.17191366,  0.21711799]),
       'palm_pos': np.array([-0.00692036, -0.19996033,  0.15038709]),
       'qpos': np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0.]),
       'qvel': np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0.])}
]

# gets a failure case from a given failure file path
def pull_failure_case(failure_file_path):
    with open(failure_file_path, "rb") as f:
        data = pickle.load(f)
        return [{"init_state_dict": demo} for demo in data]


# MAIN =========================================================
@click.command(help=DESC)
@click.option('--env_name', type=str, help='environment to load', required= True)
@click.option('--policy', type=str, help='absolute path of the policy file', required=True)
@click.option('--mode', type=str, help='exploration or evaluation mode for policy', default='evaluation')
@click.option("--failure_file", type=str, help='failure file path.', required=False, default=None)
def main(env_name, policy, mode, failure_file):
    e = GymEnv(env_name)
    pi = pickle.load(open(policy, 'rb'))
    # render policy
    demos = [{
        'init_state_dict': copy.deepcopy(demos_init[0])
    }]
    if failure_file:
        demos = pull_failure_case(failure_file)

    e.visualize_policy_from_demos(pi, demos, num_episodes=100, horizon=e.horizon, mode=mode)

if __name__ == '__main__':
    main()
