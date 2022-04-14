demos='15 25 35 15_10 25_10'

for demo in $demos; do
    echo "Rolling out constrained policy trained on $demo demos for user $1"
    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so:/usr/lib/nvidia-384/libGL.so python ~/GT/CoRX/hand_dapg/dapg/utils/visualize_policy.py --env_name relocate-v0 --policy ~/GT/CoRX/hand_dapg/dapg/study_data/$1/policies/${1}_${demo}_constrained_policy/iterations/best_policy.pickle --mode evaluation --record --episodes 1000
done
