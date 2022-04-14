# cddm_leap.py: connects to a Leap device and continuously outputs the joint locations
import os, sys, inspect, threading, time
import Leap
import numpy as np
import requests
import threading

def main():
	# create the post listener and controller
	listener = LeapListener()
	controller = Leap.Controller()
	
	# start listening
	controller.add_listener(listener)
	
	# wait for keyboard exit
	print("Press ENTER to quit...")
	
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

def map(frame):
	pose = np.zeros((31,3))
	
	# actions: joints
	# WRJ1: wrist
	#print(frame.hands[0].wrist_position)
	pose[0] = frame.hands[0].wrist_position.to_float_array()
	# WRJ0: palm
	pose[1] = frame.hands[0].palm_position.to_float_array()

	# FFJ3: pointer knuckle
	pose[2] = frame.fingers[1].bone(0).next_joint.to_float_array()
	# FFJ2: pointer proximal
	pose[3] = frame.fingers[1].bone(0).direction.to_float_array()
	# FFJ1: pointer middle
	pose[4] = frame.fingers[1].bone(1).direction.to_float_array() #next_joint.to_float_array()
	# FFJ0: pointer distal
	pose[5] = frame.fingers[1].bone(2).direction.to_float_array() #next_joint.to_float_array()
	# FFJ-1: pointer tip
	pose[6] = frame.fingers[1].bone(3).direction.to_float_array()

	# MFJ3: middle knuckle
	pose[7] = frame.fingers[2].bone(0).next_joint.to_float_array()
	# MFJ2: middle proximal
	pose[8] = frame.fingers[2].bone(0).direction.to_float_array()
	# MFJ1: middle middle
	pose[9] = frame.fingers[2].bone(1).direction.to_float_array()
	# MFJ0: middle distal
	pose[10] = frame.fingers[2].bone(2).direction.to_float_array()
	# MFJ-1: middle tip
	pose[11] = frame.fingers[2].bone(3).direction.to_float_array()

	# RFJ3: ring knuckle
	pose[12] = frame.fingers[3].bone(0).next_joint.to_float_array()
	# RFJ2: ring proximal
	pose[13] = frame.fingers[3].bone(0).direction.to_float_array()
	# RFJ1: ring middle
	pose[14] = frame.fingers[3].bone(1).direction.to_float_array()
	# RFJ0: ring distal
	pose[15] = frame.fingers[3].bone(2).direction.to_float_array()
	# RFJ-1: ring tip
	pose[16] = frame.fingers[3].bone(3).direction.to_float_array()

	# LFJ4: little metacarpal (same as knuckle since we don't have a roll joint)
	pose[17] = frame.fingers[4].bone(0).next_joint.to_float_array()
	# LFJ3: little knuckle
	pose[18] = frame.fingers[4].bone(0).next_joint.to_float_array()
	# LFJ2: little proximal
	pose[19] = frame.fingers[4].bone(0).direction.to_float_array()
	# LFJ1: little middle
	pose[20] = frame.fingers[4].bone(1).direction.to_float_array()
	# LFJ0: little distal
	pose[21] = frame.fingers[4].bone(2).direction.to_float_array()
	# LFJ-1: little tip
	pose[22] = frame.fingers[4].bone(3).direction.to_float_array()

	# THJ4: thumb metacarpal
	pose[23] = frame.fingers[0].bone(0).prev_joint.to_float_array()
	# THJ3: thumb knuckle
	pose[24] = frame.fingers[0].bone(0).next_joint.to_float_array()
	# THJ2: thumb proximal
	pose[25] = frame.fingers[0].bone(0).direction.to_float_array()
	# THJ1: thumb middle
	pose[26] = frame.fingers[0].bone(1).direction.to_float_array()
	# THJ0: thumb distal
	pose[27] = frame.fingers[0].bone(2).direction.to_float_array()
	# THJ-1: thumb tip
	pose[28] = frame.fingers[0].bone(3).direction.to_float_array()

	# Palm normal
	pose[29] = frame.hands[0].palm_normal.to_float_array()
	# Wrist?
	pose[30] = frame.hands[0].wrist_position.to_float_array()
	# if np.all(prev_Pose < -500):
	# 	prev_Pose = pose
	# else:
	# 	for i in range(len(pose)):
	# 		for j in range(len(pose[i])):
	# 			if (abs(pose[i][j]) > 0.001 and abs(prev_Pose[i][j] > 0.001)) and (pose[i][j]/prev_Pose[i][j] > 1.4 or pose[i][j]/prev_Pose[i][j] < 0.6):
	# 				pose[i][j] = prev_Pose[i][j]
	# 			else:
	# 				prev_Pose[i][j] = pose[i][j]
	#print("MAP", pose)
	requests.get(url='http://localhost:5000/set', params={'data': str(pose.tolist())})
	# return prev_Pose
	# pose: palm translation/rotation



class LeapListener(Leap.Listener):
	# prev_Pose = np.ones((31,3))*-1000.0
	def on_connect(self, controller):
		print("Connected")
	
	def on_frame(self, controller):
		frame = controller.frame()
		
		if len(frame.hands) > 0:
			map(frame)
		

if __name__ == "__main__":
	main()