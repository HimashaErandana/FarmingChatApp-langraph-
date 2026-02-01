import os
# Must set these BEFORE importing tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # suppress TF C++ logs
os.environ['ABSL_LOG_LEVEL'] = '3'       # suppress absl logs

import warnings
warnings.filterwarnings("ignore")        # suppress Python warnings

import tensorflow as tf
from tensorflow.keras.models import load_model
import json
from tensorflow.keras.preprocessing import image
import numpy as np



class ModelService:

    def __init__(self):
        self.model = None
        #self.model = load_model("Graph\Agents\Decease_agent\efficientnet_plant_disease1.keras")
        #self.model.summary()  # optional, smaller output

        with open("Graph\Agents\Decease_agent\class_indicesh5.json", "r") as f:
            self.class_indices = json.load(f)

    def getService(self,img_path):


        if self.model is None:
            self.model = load_model(r"Graph\Agents\Decease_agent\efficientnet_plant_disease1_finalll.h5", compile=False)

        idx_to_class = {int(v): k for k, v in self.class_indices.items()}

        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0



        pred = self.model.predict(img_array)
        predicted_class_index = np.argmax(pred,axis=1)[0]
        pred_class = idx_to_class[predicted_class_index]

        return pred_class