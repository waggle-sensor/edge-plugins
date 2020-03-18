import numpy as np
import inference
import tflite_runtime.interpreter as tflite
import time
import datetime
import modelRepo
import os,sys
import waggle.plugin
import logging

url = 'https://sage-restapi.nautilus.optiputer.net/api/v1/'
testImg = "/data/bh-n-mobo-c/1546362010.jpg"
modelFile = 'model.tflite'
modelPath = "/data/model/2020-03-12/"+modelFile
bucket = 'plugin-smoke-detection'
object = 'model/2020-03-17/'+modelFile
modelRepo = modelRepo.modelRepo(url)
directory = '/data/model/2020-03-17/'
#does model exist on waggle node
if not os.path.exists(modelPath):
    #get model from object storage
    modelRepo.getModel(bucket,object,directory)
    modelPath = directory + modelFile

#For plugin
plugin = waggle.plugin.PrintPlugin()

print('Starting smoke detection inferencing')
while True:
    print('Get image from HPWREN Camera')
    testObj = inference.FireImage(testImg)
    testObj.read_image(testImg)
    interpreter = tflite.Interpreter(model_path=modelPath)
    interpreter.allocate_tensors()
    print('Perform an inference based on trainned model')
    result,percent = testObj.inference(interpreter)
    print(result)
    currentDT = str(datetime.datetime.now())
    
    plugin.add_measurement({
        'sensor_id': 1,
        'parameter_id':10,
        'value': percent,
    })

    print('Publish', flush=True)
    plugin.publish_measurements()
    time.sleep(5)

