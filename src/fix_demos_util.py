import re
import click
import pickle
import copy
import random
import numpy as np


def isolate_sample(filepath, index):
    # load the sample file
    try:
        f = open(filepath, "rb")
    except FileNotFoundError:
        print("fix_demos_util.py: Sample path does not exist!")
        return

    # load the demos
    demos = pickle.load(f)
    f.close()

    # isolate the demo
    demo = demos[index]

    output_filepath = filepath[:filepath.index(".pickle")] + "_isolated_" + str(index) + ".pickle"

    # save the demo
    try:
        f = open(output_filepath, "wb")
    except:
        print("fix_demos_util.py: Could not open the output filepath for writing")
        return
    
    pickle.dump(demo, f)

    print("fix_demos_util.py: Isolated the sample to", output_filepath)

    return


def replace_demo(single_demo_filepath, index, original_filepath):
    # load the original sample
    try:
        f = open(original_filepath, "rb")
    except FileNotFoundError:
        print("fix_demos_util.py: Main sample file does not exist!")
        return

    # load the demos
    orig_demos = pickle.load(f)
    f.close()

    # load the single demo sample
    try:
        f = open(single_demo_filepath, "rb")
    except FileNotFoundError:
        print("fix_demos_util.py: Single demo file does not exist!")
        return
    
    # load the demos
    single_demo = pickle.load(f)
    f.close()

    # insert the demo
    orig_demos[index] = single_demo[-1]

    # save the demo
    try:
        f = open(original_filepath + "_NEW", "wb")
    except:
        print("fix_demos_util.py: Could not open the output filepath for writing")
        return
    
    pickle.dump(orig_demos, f)

    print("fix_demos_util.py: Inserted the sample and saved result as", original_filepath + "_NEW", "... remember to rename the file!!")
    return

@click.command(help='Contains several utilities for fixing demonstrations, such as isolating samples and inserting corrections')
@click.option('--task', type=str, help='task that the utility is performing', required=True)
@click.option('--sample_filepath', type=str, help='when isolating a sample, the sample filepath', required=False)
@click.option('--sample_index', type=int, help='when isolating a sample, the sample index', required=False)
@click.option('--replace_demo_input_filepath', type=str, help='when replacing a demo, the filepath of the replacing demo', required=False)
@click.option('--replace_demo_index', type=int, help='the index to replace the demo into', required=False)
@click.option('--replace_demo_original_filepath', type=str, help='when replacing a demo, the filepath of the original demo set', required=False)
def main(task, sample_filepath, sample_index, replace_demo_input_filepath, replace_demo_index, replace_demo_original_filepath):
    # check the task
    if task == "isolate_sample":
        isolate_sample(sample_filepath, sample_index)
        return
    elif task == "replace_demo":
        replace_demo(replace_demo_input_filepath, replace_demo_index, replace_demo_original_filepath)
        return
    else:
        print('fix_demos_util.py: Invalid task, use isolate_sample or replace_demo')
        return
    

if __name__ == '__main__':
    main()