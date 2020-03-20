import modelRepo
import os

baseURL = 'http://localhost:8080/api/v1/'
url = 'https://sage-restapi.nautilus.optiputer.net/api/v1/'

modelRepo = modelRepo.modelRepo(url)

bucket = 'plugin-smoke-detection'
object = 'model.tflite'
# bucket = 'sample1'
# object = 'newFuelMap.tif'
#object = 'camera-locations.txt'
directoryLocal = '/Users/iperezx/Downloads/'
directoryDocker = '/app/'
directoryKeras = '/userdata/kerasData/edge-plugins/plugin-smokedetect/src'

modelRepo.getModel(bucket,object,directoryLocal)

bucket = 'sample2'
filePath = os.path.join(directoryLocal, object)
modelRepo.postModel(bucket,filePath)

