import modelRepo

baseURL = 'http://localhost:8080/api/v1/'
url = 'https://sage-restapi.nautilus.optiputer.net/api/v1/'

modelRepo = modelRepo.modelRepo(baseURL)

bucket = 'sample1'
object = 'newFuelMap.tif' 
directoryLocal = '/Users/iperezx/Documents/'
directoryDocker = '/app/'
modelRepo.getModel(bucket,object,directoryDocker)

bucket = 'sample2'
filePath = directoryLocal + 'camera-locations.txt'
modelRepo.postModel(bucket,filePath)

