
# created 10/15/20 splits
#python ~/GT/CoRX/src/create_additional_demo_files.py --user_id $1

# set up config files
#bash ~/GT/CoRX/hand_dapg/dapg/study_data/setup_training_configs.bash $1

# change directory
cd ~/GT/CoRX/hand_dapg/dapg

# train DAPG
num_demos="20 20_10_1"
for demos in $num_demos; do
    echo /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/policies/${1}_${demos}_policy/
    python examples/job_script.py --output /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/policies/${1}_${demos}_policy/ --config /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/configs/dapg_${1}_${demos}.txt
done

# go back to previous directory
cd - > /dev/null