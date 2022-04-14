demos='20_10_1 20_10_2 30'
#demos='25_gen_500'

for demo in $demos; do
    for i in `seq 1 10 799`; do
	    echo "user $1 : policy $demo : iter $i"
	    LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so:/usr/lib/nvidia-384/libGL.so python ~/GT/CoRX/hand_dapg/dapg/utils/visualize_policy.py --env_name relocate-v0 --policy ~/GT/CoRX/hand_dapg/dapg/study_data/$1/policies/${1}_${demo}_policy/iterations/policy_${i}.pickle --mode evaluation --record --episodes 1000
    done
done
