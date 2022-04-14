# change directory
cd ~/GT/CoRX/hand_dapg/dapg

# train DAPG
num_demos="10 20"
for demos in $num_demos; do
    echo /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/policies/${1}_${demos}_policy/
    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so:/usr/lib/nvidia-384/libGL.so python utils/visualize_policy.py --env_name relocate-v0 --policy study_data/${1}/policies/${1}_${demos}_policy/iterations/best_policy.pickle --mode evaluation --record --collect_failures --episodes 1000 --num_failures $((30-${demos})) 
done

# go back to previous directory
cd - > /dev/null
