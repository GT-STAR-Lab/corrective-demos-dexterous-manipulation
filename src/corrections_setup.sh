# sets up the MuJuCo for corrective demos
# arg 1: user_id
# arg 2: # of demos (25 or 15)

# activate conda
#conda activate mjrl-env
#echo "activated conda"

# leapd driver
#gnome-terminal -- "sudo" leapd
#echo "started leapd driver"

#conda activate mjrl-env

# leap -> mujoco server
#gnome-terminal -- python2 /home/kolb/GT/CoRX/src/cddm_leap.py
#echo "started leap controller"

# mujoco
cd /home/kolb/GT/CoRX/hand_dapg/dapg
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so:/usr/lib/nvidia-384/libGL.so python utils/visualize_cddm_demos.py --env_name relocate-v0 --failure_file /home/kolb/GT/CoRX/hand_dapg/dapg/study_data/${1}/failures/${1}_${2}_failures.pickle
echo "started mujoco"
