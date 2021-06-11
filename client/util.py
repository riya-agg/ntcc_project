import pickle
import json
import numpy as np
import os
import cv2
import tensorflow as tf

__model = None

def predict_sign():
	# reading the recorded video from webcam
	cap = cv2.VideoCapture('sign.mp4')
	print("read the recorded video")
	
	totalframecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	print("TFC:", totalframecount)
	x = totalframecount // 10
	
	frame_saved = []
	while(cap.isOpened()):
		frameId = cap.get(1)
		ret, frame = cap.read()
		if (ret != True):
			break
			
		if (frameId%x == 0):
			frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			frame_grey = cv2.resize(frame_grey,(200,200))
			frame_grey = frame_grey/255
			frame_saved.append(frame_grey)
			
	cap.release()              
	frame_saved = frame_saved[:10]
	frame_saved = np.array(frame_saved)
	frame_data = frame_saved.reshape((1,10,200,200,1))

	# loading the saved model and its weights
	json_file = open('model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	
	loaded_model = tf.keras.model.model_from_json(loaded_model_json)
	
	loaded_model.load_weights("model.h5")
	print("Loaded model from disk")
	
	# predicting the sign
	pred = __model.predict(frame_data)
	print("\nPREDICTION >> \n",pred)
	'''
	if pred >= 0.5:
		return 'Loan Approved!'
		
	else:
		return 'Loan Rejected!' 

	
def load_saved_artifacts():
	print("loading saved artifacts...start")
	path = os.path.dirname(__file__) 
	artifacts = os.path.join(path, "artifacts")
	
	global __model
	
	if __model is None:
		with open(artifacts[0]+"/signPickleFileGBM.pkl", 'rb') as f:
			__model = pickle.load(f)
			
	print("loading saved artifacts...done")


load_saved_artifacts()
'''