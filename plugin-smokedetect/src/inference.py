import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
import os

class FireImage:
    oneFire = False
    newsize = (128,128)
    classes = ["No Fire", "FIRE"]
    def __init__(self, imageID):
        self.image = None
        self.location = imageID
        self.direction = imageID
    
    def read_image(self, imagePath):
        PIL_image = Image.open(imagePath)
        img = np.array(PIL_image.resize(FireImage.newsize))
        img = img.astype("float32") / 255.0
        self.image = img

    def inference(self, tf_lite_interpreter):
        try:
            input_data = np.expand_dims(self.image, axis=0)
            image_shape = input_data.shape
        except AttributeError:
            return "No Image Attatched!"
        try:
            input_details = tf_lite_interpreter.get_input_details()
            input_shape = input_details[0]["shape"]
            output_details = tf_lite_interpreter.get_output_details()
            output_shape = output_details[0]["shape"]
        except AttributeError:
            print("TF_Lite Model is not able to be formated!")

        if np.array_equal(input_shape, image_shape):
            tf_lite_interpreter.set_tensor(input_details[0]["index"], input_data)
            tf_lite_interpreter.invoke()
            output = tf_lite_interpreter.get_tensor(output_details[0]["index"])
            j = np.argmax(output)
            percent = "{:.2%}".format(output[0][j])
            ans = f"{FireImage.classes[j]}, {percent}"

            return  [ans]
        else:
            return "ERROR! Image input is not in correct dimensions!"