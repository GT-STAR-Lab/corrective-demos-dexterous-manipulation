# Citation

This repo contains code used for the following paper ([arXiv](https://arxiv.org/abs/2204.07631)):

>Abhineet Jain*, Jack Kolb*, J.M. Abbess IV and Harish Ravichandar (2022). **Evaluating the Effectiveness of Corrective Demonstrations and a Low-Cost Sensor for Dexterous Manipulation**. *Machine Learning in Human-Robot Collaboration: Bridging the Gap Workshop at the 17th Annual ACM/IEEE International Conference on Human-Robot Interaction (HRI 2022).*


# Contents
- [Collecting demonstrations](#collecting-demonstrations)
- [Training DAPG](#training-dapg)
- [Collecting failures](#collecting-failures)
- [Collecting corrections](#collecting-corrections)
- [Retraining with corrections](#retraining-with-corrections)
- [Policy rollout and success rate](#policy-rollouts-and-success-rate)
- [Visualizing demonstrations](#visualizing-demonstrations)

# Collecting demonstrations

1. In one terminal, open `sudo leapd`
2. In a new terminal, activate conda environment with `conda activate mjrl-env`.
3. Run `~/GT/CoRX/src/study_setup.sh --samples_filename <samples file>` where `<samples file>` is the file name, NOT the path (ex: `testing_initial_states_20`)
4. Enter the User ID for which we are collecting data
6. Once you wave your hand over the LeapMotion, MuJoCo will open up.
7. In a separate terminal via ssh, open `python control_demos.py`. The conductor will guide the subject to start the demonstration via this control.
8. The control will stop after collecting 35 demos. At this point, the study is over. MuJoCo will be open but we should force close it.

You can find these demonstrations saved in `~/GT/CoRX/hand_dapg/dapg/study_data/<user_id>/<user_id>_35_demos.pickle`.
# Training DAPG

Uncomment lines `88-91` and comment lines `82-85` in `~/GT/CoRX/mj_envs/mj_envs/hand_manipulation_suite/relocate_v0.py`. The values under `MuJoCo boundaries` should be used for training and beyond.

Run `~/GT/CoRX/src/training_dapg.sh <user_id>` and enjoy.

This will take care of the following steps.
1. Create `<user_id>_25_demos.pickle` and `<user_id>_15_demos.pickle` demo files out of `<user_id>_35_demos.pickle`. Run `python ~/GT/CoRX/src/create_additional_demo_files.py --user_id <user_id>`.
2. Run `bash study_data/setup_training_configs.bash <user_id>` to set up configuration files for different demonstration sources for a specific user.
3. Go to `cd ~/GT/CoRX/hand_dapg/dapg`
4. Run `python examples/job_script.py --output /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/<user_id>/policies/<user_id>_35_policy/ --config /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/<user_id>/configs/dapg_<user_id>_35.txt`
5. Repeat step 4 for 25 and 15 demo files.

# Collecting failures

Run `~/GT/CoRX/src/collect_failures.sh <user_id>` and enjoy.

This will take care of the following steps.
1. Go to `cd ~/GT/CoRX/hand_dapg/dapg`
2. Run `MJPL python utils/visualize_policy.py --env_name relocate-v0 --policy study_data/<user_id>/policies/<user_id>_25_policy/iterations/best_policy.pickle --mode evaluation --collect_failures --record`
3. This will save the failures at `/home/kolb/GT/CoRX/hand_dapg/dapg/study_data/<user_id>/failures/<user_id>_25_failures.pickle`
4. Repeat the same for the 15 demo policy.

# Collecting corrections

1. Make sure that the `conda` environment is set to `mjrl-env` and `sudo leapd`, `python2 cddm_leap.py` are running.
2. Run `~/GT/CoRX/src/corrections_setup.sh <user_id> <num_demos>`.
3. You'll have to input the same `<user_id>` as input.
4. Once you wave your hand over the LeapMotion, MuJoCo will open up.
5. In a separate terminal via ssh, open `python control_demos.py --max_demos 10`. The conductor will guide the subject to start the demonstration via this control.
6. The control will stop after collecting 10 demos. At this point, the study is over. MuJoCo will be open but we should force close it.

You will find these demonstrations saved in `/home/kolb/GT/CoRX/hand_dapg/dapg/study_data/<user_id>/corrections/<user_id>_<num_demos>_corrections.pickle`.

Follow this process for `<num_demos>` as 15 and 25.

# Combining demo sets

1. Run `python ~/GT/CoRX/src/combine_demos.py --user_id <user_id> --input1 <demo file path 1> --input2 <demo file path 2> --output <output demo file path>`.

For example:

`python ~/GT/CoRX/src/combine_demos.py --user_id 0201 --input1 /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/0201/0201_training_20_demos.pickle --input2 /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/0201/0201_testing_10_demos.pickle --output /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/0201/0201_combined_20_10_1.pickle`


This will concatenate the demos from the two input demo files and output them to the provided output demo file path.

# Redoing bad demos

After visualizing your demos, you may want to redo a few. Follow these steps:

0. Know the indexes of the demos you want to correct, for example, indexes 5, 13, and 15
1. Isolate the samples by running `python ~/GT/CoRX/src/fix_demos_util.py --task isolate_sample --sample_filepath <samples file path> --sample_index <sample index>` for each of the sample indexes; the samples file path is typically in `~/GT/CoRX/hand_dapg/data/`
2. Collect the demo for the single sample by running `~/GT/CoRX/src/study_setup.sh <samples file name>` where the samples file name is the name of the samples file followed by `_isolated_<index>`, for example `training_initial_states_20_isolated_5`. Run this for each of the indices.
3. Replace the sample by running `python ~/GT/CoRX/src/fix_demos_util.py --task replace_demo --replace_demo_input_filepath <demo file path> --replace_demo_index <demo index> --replace_demo_original_filepath <original demo file path>` for each of the indices.


# Retraining with corrections

Run `~/GT/CoRX/src/training_dapg_corrections.sh <user_id>` and enjoy.

This will take care of the following steps.
1. Create `<user_id>_25_10_demos.pickle` and `<user_id>_15_10_demos.pickle` demo files. Run `python ~/GT/CoRX/src/append_corrective_demos.py --user_id <user_id>`.
2. Follow steps 3 and 4 from the `Training DAPG` section.
3. Repeat step 2 for the 15 demo policy corrections.

# Policy rollouts and success rate

1. Go to `cd ~/GT/CoRX/hand_dapg/dapg`
2. Run `MJPL python utils/visualize_policy.py --env_name relocate-v0 --policy study_data/<user_id>/policies/<user_id>_25_policy/iterations/best_policy.pickle --mode evaluation`. If you don't want to visualize the rollouts, add a `--record` flag.
3. This will perform 100 policy rollouts in MuJoCo and report task success for each rollout and total success rate.
4. Repeat step 2 for each trained policy. We have 5 policies - 35 demos, 25 demos, 15 demos, 25 demos + 10 corrections, 15 demos + 10 corrections.

# Visualizing demonstrations

1. Go to `cd ~/GT/CoRX/hand_dapg/dapg`
2. Run `MJPL python utils/visualize_collected_demos.py --env_name relocate-v0 --demo_file study_data/<user_id>/<user_id>_<num_demos>_demos.pickle`.

# Recording rollouts

1. Go to `cd ~/GT/CoRX/src`
2. Run `./collect_rollout_statistics.sh`. This will run the following for each user, for each policy
3. `MJPL python utils/visualize_policy.py --env_name relocate-v0 --policy study_data/<user_id>/policies/<user_id>_<num_demos>_policy/iterations/best_policy.pickle --mode evaluation --record --episodes 500`
