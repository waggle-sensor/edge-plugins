import os
import requests

class cameras:
    def __init__(self,hpwrenUrl):
        self.hpwrenUrl = hpwrenUrl
        self.requestData = requests.get(self.hpwrenUrl)
        self.hpwrenCams = self.requestData.json()

    def getImageURL(self, cameraID=0,siteID=0):
        hpwrenCams = self.hpwrenCams
        hpwrenCamsF = hpwrenCams["features"]
        hpwrenCamsAtSite = hpwrenCamsF[siteID]["properties"]["latest-images"]
        imageURL = hpwrenCamsAtSite[cameraID][0]["image"]
        description = hpwrenCamsAtSite[cameraID][0]["description"]
        return imageURL,description
