# append corrective demonstrations
#python ~/GT/CoRX/src/append_corrective_demos.py --user_id $1

# change directory
cd ~/GT/CoRX/hand_dapg/dapg

# train DAPG
num_demos="10 20"
modes="2"
for demos in $num_demos; do
    for mode in $modes; do
        echo /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/policies/${1}_${demos}_$((30-${demos}))_${mode}_policy/
        python examples/job_script.py --output /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/policies/${1}_${demos}_$((30-${demos}))_${mode}_policy/ --config /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/configs/dapg_${1}_${demos}_$((30-${demos}))_${mode}.txt
    done
done

# go back to previous directory
cd - > /dev/null



