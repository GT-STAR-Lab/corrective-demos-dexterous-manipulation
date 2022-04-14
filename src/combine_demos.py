import click
import pickle
import copy
import random
import numpy as np

@click.command(help='Combine two demonstration files into one')
@click.option('--user_id', type=str, help='user ID, as a confirmation', required=True)
@click.option('--input1', type=str, help='input demo file path 1', required=True)
@click.option('--input2', type=str, help='input demo file path 2', required=True)
@click.option('--output', type=str, help='output file path', required=True)
def main(user_id, input1, input2, output):
    # check if the user ID matches the ID used by the input and output files
    if user_id not in input1:
        print("Input 1 does not use the given user ID! Check it!")
        return
    if user_id not in input2:
        print("Input 2 does not use the given user ID! Check it!")
        return
    if user_id not in output:
        print("Output does not use the given user ID! Check it!")
        return
    
    try:
        f1 = open(input1, "rb")
    except FileNotFoundError:
        print("Input 1 does not exist!")
        return

    demos_1 = pickle.load(f1)
    f1.close()
    
    try:
        f2 = open(input2, "rb")
    except FileNotFoundError:
        print("Input 2 does not exist!")
        return
    
    demos_2 = pickle.load(f2)
    f2.close()
    combined = np.concatenate((np.array(demos_1), np.array(demos_2)))
    
    try:
        f3 = open(output, "wb")
    except FileNotFoundError:
        print("Cannot create output file!")
        return
    
    pickle.dump(combined, f3)
    f3.close()

    print("Combined the demos! Output to", output)

if __name__ == '__main__':
    main()