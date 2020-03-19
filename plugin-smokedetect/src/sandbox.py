import modelRepo

baseURL = 'http://localhost:8080/api/v1/'
url = 'https://sage-restapi.nautilus.optiputer.net/api/v1/'

modelRepo = modelRepo.modelRepo(url)

bucket = 'sample1'
object = 'newFuelMap.tif' 
directoryLocal = '/Users/iperezx/Documents/'
directoryDocker = '/userdata/kerasData/edge-plugins/plugin-smokedetect/src'
modelRepo.getModel(bucket,object,directoryLocal)

bucket = 'sample2'
filePath = directoryLocal + 'camera-locations.txt'
modelRepo.postModel(bucket,filePath)

