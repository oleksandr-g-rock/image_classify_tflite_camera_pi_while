import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageOps

import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from picamera import PiCamera

print("#set classes names")
classes_names = ['animals', 'other', 'person'] #you can change classes

print("#load model")
TF_LITE_MODEL_FILE_NAME = "animall_person_other_v2_fine_tuned.tflite" #you can change model
interpreter = tf.lite.Interpreter(model_path = TF_LITE_MODEL_FILE_NAME)

print("#Check Input Tensor Shape")
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
#print results
print("Input Shape:", input_details[0]['shape'])
print("Input Type:", input_details[0]['dtype'])
print("Output Shape:", output_details[0]['shape'])
print("Output Type:", output_details[0]['dtype'])

print("#Resize Tensor Shape")
interpreter.resize_tensor_input(input_details[0]['index'], (1, 299, 299, 3)) #you can change to your parameters
interpreter.resize_tensor_input(output_details[0]['index'], (1, 3)) #you can change to your parameters
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
#print results
print("Input Shape:", input_details[0]['shape'])
print("Input Type:", input_details[0]['dtype'])
print("Output Shape:", output_details[0]['shape'])
print("Output Type:", output_details[0]['dtype'])

print("# input details")
print(input_details)
print("# output details")
print(output_details)


while True:

	#start time
	start_time = time.time()

	camera = PiCamera()
	camera.capture('image.jpeg')
	img_path = 'image.jpeg'

	#resize image
	img = load_img(img_path, target_size=(299, 299))
	new_img = image.img_to_array(img)
	new_img /= 255
	new_img = np.expand_dims(new_img, axis=0)

	# input_details[0]['index'] = the index which accepts the input
	interpreter.set_tensor(input_details[0]['index'], new_img)
   
	# run the inference
	interpreter.invoke()
    
	# The function `get_tensor()` returns a copy of the tensor data.
	# Use `tensor()` in order to get a pointer to the tensor.
	output_data = interpreter.get_tensor(output_details[0]['index'])
	#print(output_data)    

	#stop time
	elapsed_ms = (time.time() - start_time) * 1000

	#print predict classes
	classes = np.argmax(output_data, axis = 1)
	print("elapsed time: ", elapsed_ms, " , predict class number: ", classes, " ,is class name: ", classes_names[classes[0]], sep='')

	#close camera
	camera.close()
