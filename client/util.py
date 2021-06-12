import pickle
import json
import numpy as np
import os
import cv2
#import tensorflow as tf
from keras.models import model_from_json

#__model = None

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
	
	loaded_model = model_from_json(loaded_model_json)
	
	loaded_model.load_weights("model.h5")
	print("Loaded model from disk")
	
	# predicting the sign
	pred = loaded_model.predict(frame_data)
	print("\nPREDICTION >> \n",pred)
	#index_ = pred.index(np.max(pred))
	
	#index_ = np.where(pred == np.max(pred))
	index_ = np.argmax(pred)
	print(index_)
	
	if index_ == 0:
	    return 'Begin'
	elif index_ == 1:
	    return 'Good Afternoon'
	elif index_ == 2:
	    return 'Good Morning'
	elif index_ == 3:
	    return 'Good Night'
	elif index_ == 4:
	    return 'Hello'
	elif index_ == 5:
	    return 'How are you'
	elif index_ == 6:
	    return 'Nice'
	elif index_ == 7:
	    return 'Sorry'
	elif index_ == 8:
	    return 'Thank You'
	elif index_ == 9:
	    return 'Welcome'
		
	'''	
		
	if index_ == 0:
	    p = {'prediction': 'Begin'}
	elif index_ == 1:
	    p = {'prediction': 'Good Afternoon'}
	elif index_ == 2:
	    p = {'prediction': 'Good Morning'}
	elif index_ == 3:
	    p = {'prediction': 'Good Night'}
	elif index_ == 4:
	    p = {'prediction': 'Hello'}
	elif index_ == 5:
	    p = {'prediction': 'How are you'}
	elif index_ == 6:
	    p = {'prediction': 'Nice'}
	elif index_ == 7:
	    p = {'prediction': 'Sorry'}
	elif index_ == 8:
	    p = {'prediction': 'Thank You'}
	elif index_ == 9:
	    p = {'prediction': 'Welcome'}
		
	return json.dumps(p)
	
	'''
		