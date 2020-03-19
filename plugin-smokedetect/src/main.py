import numpy as np
import inference
import tflite_runtime.interpreter as tflite
import time
import datetime
import modelRepo
import os,sys
import waggle.plugin
import logging
import requests

#Sage REST API parameters
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

#HPWREN Parameters
hpwrenUrl = "https://firemap.sdsc.edu/pylaski/\
stations?camera=only&selection=\
boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
requestData = requests.get(hpwrenUrl)
hpwrenCams = requestData.json() #returns a dictionary
hpwrenCamsF = hpwrenCams["features"]
siteID = 0
cameraID = 0
numSites = len(hpwrenCamsF)
hpwrenCamsAtSite = hpwrenCamsF[siteID]["properties"]["latest-images"]
imageURL = hpwrenCamsAtSite[cameraID][0]["image"]
description = hpwrenCamsAtSite[cameraID][0]["description"]

#For plugin
plugin = waggle.plugin.PrintPlugin()

print('Starting smoke detection inferencing')
while True:
    testObj = inference.FireImage()
    print('Get image from HPWREN Camera')
    print("Image url: " + imageURL)
    print("Description: " + description)
    #testObj.readImage(testImg)
    testObj.urlToImage(imageURL)
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

