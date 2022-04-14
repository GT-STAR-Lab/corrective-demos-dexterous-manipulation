# leap -> mujoco server
gnome-terminal -- python2 /home/kolb/GT/CoRX/src/cddm_leap.py
echo "started leap controller"

# Mujoco
cd /home/kolb/GT/CoRX/hand_dapg/dapg
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so:/usr/lib/nvidia-384/libGL.so python utils/visualize_cddm_demos.py --env_name relocate-v0 --samples_filename $1
