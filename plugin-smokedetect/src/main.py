import numpy as np
import inference,hpwren
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
import waggle.plugin,logging,requests

#Sage Storage API parameters
SAGE_USER_TOKEN = os.getenv('SAGE_USER_TOKEN')
if SAGE_USER_TOKEN is None:
    raise EnvironmentError("Failed because {} is not set.".format('SAGE_USER_TOKEN'))

SAGE_HOST = os.getenv('SAGE_HOST')
if SAGE_HOST is None:
    raise EnvironmentError("Failed because {} is not set.".format('SAGE_HOST'))

BUCKET_ID_MODEL = os.getenv('BUCKET_ID_MODEL')
if BUCKET_ID_MODEL is None:
    raise EnvironmentError("Failed because {} is not set.".format('BUCKET_ID_MODEL'))

object = 'model.tflite'
directory = '/data/model/'
modelPath = os.path.join(directory,object)
modelVersion = '2020-05-26'
cloudPath = os.path.join('output/',modelVersion, object)
#Does model exist on waggle node
if not os.path.exists(modelPath):
    command = 'sage-cli.py storage files download ' + str(BUCKET_ID_MODEL) + \
            ' ' + str(cloudPath) + ' --target ' + modelPath
    result = subprocess.run(command, check=True, shell=True,\
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#HPWREN Parameters
hpwrenUrl = "https://firemap.sdsc.edu/pylaski/\
stations?camera=only&selection=\
boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
cameraID=0
siteID=0
camObj = hpwren.cameras(hpwrenUrl)
imageURL,description = camObj.getImageURL(cameraID,siteID)

#For plugin
plugin = waggle.plugin.PrintPlugin()

print('Starting smoke detection inferencing')
while True:
    testObj = inference.FireImage()
    print('Get image from HPWREN Camera')
    print("Image url: " + imageURL)
    print("Description: " + description)
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

    print('Publish\n', flush=True)
    plugin.publish_measurements()
    time.sleep(5)

