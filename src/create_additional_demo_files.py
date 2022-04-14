import click
import pickle
import copy
import random

def get_file_name(user_folder, user_id, num_demos):
    return user_folder + '/' + user_id + '_' + str(num_demos) + '_demos.pickle'

@click.command(help='Create 10, 15 and 20 demonstration files from 30 demos for a specific user')
@click.option('--user_id', type=str, help='User ID to create demonstrations for', required=True)
def main(user_id):
    user_folder = '/home/kolb/GT/CoRX/hand_dapg/dapg/study_data/' + user_id

    user_30_demo_file = get_file_name(user_folder, user_id, 30)
    f_30 = open(user_30_demo_file, 'rb')
    all_demos = pickle.load(f_30)
    random.seed(123321)

    user_20_demo_file = get_file_name(user_folder, user_id, 20)
    with open(user_20_demo_file, 'wb') as f_20:
        pickle.dump(copy.deepcopy(random.sample(all_demos, 20)), f_20)

    user_15_demo_file = get_file_name(user_folder, user_id, 15)
    with open(user_15_demo_file, 'wb') as f_15:
        pickle.dump(copy.deepcopy(random.sample(all_demos, 15)), f_15)
    
    user_10_demo_file = get_file_name(user_folder, user_id, 10)
    with open(user_10_demo_file, 'wb') as f_10:
        pickle.dump(copy.deepcopy(random.sample(all_demos, 10)), f_10)

if __name__ == '__main__':
    main()