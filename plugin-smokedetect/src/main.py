import numpy as np
import inference
import tflite_runtime.interpreter as tflite
import time

print('Starting smoke detection inferencing')
while True:
    print('Get image from HPWREN Camera')
    testImg = "/data/bh-n-mobo-c/1546362010.jpg"
    testObj = inference.FireImage(testImg)
    testObj.read_image(testImg)
    modelPath = "/data/model/2020-03-12/model.tflite"
    interpreter = tflite.Interpreter(model_path=modelPath)
    interpreter.allocate_tensors()
    print('Perform an inference based on trainned model')
    result = testObj.inference(interpreter)
    print(result)
    time.sleep(30)

