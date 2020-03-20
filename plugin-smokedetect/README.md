# edge-plugins/plugin-smokedetect

Docker container usage
-------------
The docker image is hosted on [sagecontinuum](https://hub.docker.com/orgs/sagecontinuum).

Build the image:
```bash
docker build --build-arg TOKEN=${TOKEN} -t sagecontinuum/plugin-smokedetect:0.1.0 .
```
where `TOKEN` is set enviroment varibale and created through [JWT](https://jwt.io/) with the appropriate secret.

Run the container:
```bash
docker run sagecontinuum/plugin-smokedetect:0.1.0
```
# Instructions
The following instructions are meant to serve a user from start to finish of how to create the smoke detection plugin.

## Step 1: clone beehive repository 
```bash
git clone https://github.com/waggle-sensor/beehive-server
```
Start the server:
```bash
cd beehive-server
./do.sh deploy
```

## Step 2: run trainning jupyter notebook and save model
First clone the smoke detection model:
```bash
git clone https://gitlab.nautilus.optiputer.net/i3perez/keras-smoke-detection
```
Create a kubernetes deployment (on Nautilus):
```bash
kubectl create -f kerasDeloyment.yaml
```
Run the juputer notebook as describe in the README file. At the end of the notebook
the trainned model will be save to the object storage through [SAGE REST API](https://github.com/sagecontinuum/sage-restapi)

## Step 3: clone waggle repository
```bash
git clone https://github.com/waggle-sensor/waggle-node
```
To start the waggle node (this assumes an existing beehive instance):
```bash
./waggle-node up
```

To start a plugin you will need to create a docker image and pass the following command:
```bash
./waggle-node schedule waggle/plugin-smokedetect:0.1.0
```
To view the output:
```bash
./waggle-node logs | grep plugin
```

Example output of the plugin:
```
plugin-50-0.1.0-0_1     | published measurements:
plugin-50-0.1.0-0_1     | {'sensor_id': 1, 'sensor_instance': 0, 'parameter_id': 10, 'timestamp': 1584738130, 'value': 0.5205857753753662}
plugin-50-0.1.0-0_1     | Get image from HPWREN Camera
plugin-50-0.1.0-0_1     | Image url: https://hpwren.ucsd.edu/cameras/L/bm-n-mobo-m.jpg
plugin-50-0.1.0-0_1     | Description: Big Black Mountain ~north view, monochrome
plugin-50-0.1.0-0_1     | Perform an inference based on trainned model
plugin-50-0.1.0-0_1     | FIRE, 52.06%
plugin-50-0.1.0-0_1     | Publish
```
