
# created 15/25 splits
# python ~/GT/CoRX/src/create_additional_demo_files.py --user_id $1

# # set up config files
# bash ~/GT/CoRX/hand_dapg/dapg/study_data/setup_training_configs.bash $1

# change directory
cd ~/GT/CoRX/hand_dapg/dapg

# Ensure the environment changes are done for training
echo "Have you made the required changes to relocate_v0.py? Press ENTER to continue."
read changes_done

# train DAPG
num_demos="35"
for demos in $num_demos; do
    sed -i 's/300/500/g' /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/configs/dapg_${1}_${demos}.txt
    echo /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/policies/${1}_${demos}_policy/
    python examples/job_script.py --output /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/policies/${1}_${demos}_policy/ --config /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/configs/dapg_${1}_${demos}.txt
done

# go back to previous directory
cd - > /dev/null