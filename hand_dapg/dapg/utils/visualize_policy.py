import mj_envs
import click 
import os
import gym
import numpy as np
import pickle
from mjrl.utils.gym_env import GymEnv

DESC = '''
Helper script to visualize policy (in mjrl format).\n
USAGE:\n
    Visualizes policy on the env\n
    $ python utils/visualize_policy --env_name relocate-v0 --policy policies/relocate-v0.pickle --mode evaluation\n
'''

# MAIN =========================================================
@click.command(help=DESC)
@click.option('--env_name', type=str, help='environment to load', required= True)
@click.option('--policy', type=str, help='absolute path of the policy file', required=True)
@click.option('--mode', type=str, help='exploration or evaluation mode for policy', default='evaluation')
@click.option('--collect_failures', help='collect failed scenarios', is_flag=True)
@click.option('--single_failure', help='collect a single failure and write it to a special single failure file', is_flag=True)
@click.option('--record', help='only record policy rollout', is_flag=True)
@click.option('--episodes', type=int, help='rollout for these many episodes', default=100)
@click.option('--num_failures', type=int, help='number of worst failures to collect', default=0)
@click.option('--samples_filename', type=str, help='filename with samples for visualization', default='testing_initial_state_1000')
def main(env_name, policy, mode, collect_failures, single_failure, record, episodes, num_failures, samples_filename):
    e = GymEnv(env_name)
    pi = pickle.load(open(policy, 'rb'))
    failure_file_path = None
    if collect_failures:
        # Failure path is computed using the policy for which failures are being collected
        # Policy path template: /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/<user_id>/policies/<user_id>_<demos>_policy/iterations/best_policy.pickle
        # Failure path template: /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/<user_id>/failures/<user_id>_<demos>_failures.pickle
        failure_file_path = '/'.join(policy.rstrip('/').split('/')[:-2]).replace('policies', 'failures').replace('policy', '_failures.pickle')
        if single_failure:
            failure_file_path = '/'.join(policy.rstrip('/').split('/')[:-2]).replace('policies', 'failures').replace('policy', 'failures_1.pickle')

    # render policy
    e.visualize_policy(
        pi,
        num_episodes=episodes,
        horizon=e.horizon,
        mode=mode,
        failure_file_path=failure_file_path,
        record=record,
        samples_filename=samples_filename,
        num_failures=num_failures
    )

if __name__ == '__main__':
    main()
