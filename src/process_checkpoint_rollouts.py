# processes a given checkpoints file to generate a CSV for the user's rollout success rate at each iteration checkpoint

import click


DESC = '''
Helper script to convert all checkpoint rollouts for a user to a CSV format.\n
USAGE:\n
    Converts checkpoint rollouts file to CSV format\n
    $ python process_checkpoint_rollouts.py --user 0102 --file 0102_all_checkpoint_rollout_results.txt\n
'''

@click.command(help=DESC)
@click.option('--file', type=str, help='rollout success file', required= True)
@click.option('--user', type=str, help='user ID', required= True)
def main(file, user):
    # process the checkpoint rollout file into a values matrix (dict of dicts)
    values = {}
    with open(file, "r") as f:
        lines = f.readlines()
        policy = -1  # running values for the policy and iteration
        iter = -1
        for line in lines:
            line = line.replace("\n", "")  # remove the \n
            if "user" in line:  # ensure the user ID in the rollout file matches the given user ID
                if line.split(" : ")[0].replace("user ", "") != user:
                    print("Error! --user does not match user ID found in file!")
                    return
            if "policy" in line:  # set the policy, if applicable
                policy = line.split(" : ")[1].replace("policy ", "")
            if "iter" in line:  # set the iter, if applicable
                iter = line.split(" : ")[2].replace("iter ", "")
            
            if "Success rate" in line:  # add a success rate
                success_rate = line.split(" = ")[1]
                policy_sr = user + "_" + policy + "_sr"  # set the header
                if policy_sr not in values:
                    values[policy_sr] = {}
                values[policy_sr][iter] = success_rate
            
            if "Average score" in line:  # add an average score
                average_score = line.split(" = ")[1]
                policy_as = user + "_" + policy + "_as"  # set the header
                if policy_as not in values:
                    values[policy_as] = {}
                values[policy_as][iter] = average_score
        
    # save the values matrix as a CSV file
    with open(user + "_rollout_results.csv", "w") as f:
        # write the headers
        headers = ["iter"] + sorted(list(values.keys()))
        f.write(",".join(headers))

        # get the total iterations, sorted and deduped
        iters = sorted(list(set([int(x) for y in values for x in list(values[y].keys())])))

        # for each iteration, write the values
        for iter in iters:
            csv_string = "\n" + str(iter)
            for policy in sorted(values.keys()):
                csv_string += "," + values[policy][str(iter)] if str(iter) in values[policy] else ""
            f.write(csv_string)
            #f.write("\n" + ",".join([str(iter)] + [values[x][str(iter)] if str(iter) in sorted(list(values[x].keys())) else "" for x in values]))
     
    print("Done processing rollout checkpoints!")
    return

if __name__ == '__main__':
    main()