demos='25 35'

for demo in $demos; do
    echo "Rolling out standard generalized policy trained on $demo demos for user $1"
    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so:/usr/lib/nvidia-384/libGL.so python ~/GT/CoRX/hand_dapg/dapg/utils/visualize_policy.py --env_name relocate-v0 --policy ~/GT/CoRX/hand_dapg/dapg/study_data/$1/policies/${1}_${demo}_policy/iterations/policy_300.pickle --mode evaluation --record --episodes 1000
done
