import click
import pickle
import copy

def get_demo_file_name(user_folder, user_id, num_demos):
  return user_folder + '/' + user_id + '_' + str(num_demos) + '_demos.pickle'

def get_combined_file_name(user_folder, user_id, num_demos, mode):
  return user_folder + '/' + user_id + '_' + str(num_demos) + '_' + str(30-num_demos) + '_' + str(mode) + '_demos.pickle'

def get_correction_file_name(user_folder, user_id, num_demos, mode):
  return user_folder + '/corrections/' + user_id + '_' + str(num_demos) + '_' + str(mode) + '_corrections.pickle'

@click.command(help='Append corrective demonstrations for a specific user to the original demos')
@click.option('--user_id', type=str, help='User ID to append corrective demonstrations for', required=True)
def main(user_id):
    user_folder = '/home/kolb/GT/CoRX/hand_dapg/dapg/study_data/' + user_id
    
    for num_demos in [10, 20]:
      for mode in [1, 2]:
          demo_file = open(get_demo_file_name(user_folder, user_id, num_demos), 'rb')
          demos = pickle.load(demo_file)

          correction_file = open(get_correction_file_name(user_folder, user_id, num_demos, mode), 'rb')
          corrections = pickle.load(correction_file)
        
          combined_demos = copy.deepcopy(demos + corrections)
        
          combined_file_name = get_combined_file_name(user_folder, user_id, num_demos, mode)
          with open(combined_file_name, 'wb') as combined_file:
              pickle.dump(copy.deepcopy(combined_demos), combined_file)

if __name__ == '__main__':
    main()
