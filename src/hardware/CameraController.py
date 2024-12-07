#!/usr/bin/python
import numpy as np
import time
from picamera2 import Picamera2, Preview
from PIL import Image
from controllers.config_controller import ConfigController

class CameraController:
    _instance = None

    def __init__(self):
        if not CameraController._instance:
            self.config_controller                = ConfigController.get_instance()
            self.config                           = self.config_controller.get_config()
            self.camera                           = Picamera2()
            self.camera.options["quality"]        = 10
            #self.camera.options["compress_level"] = 2
            
            self.camera.start()
            
            CameraController._instance = self
        else:
            raise Exception("You cannot create another CameraController class")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = CameraController()
        return cls._instance

    def take_image(self):
        data          = self.camera.capture_array("main")
        # The following will rotate the image by 270 deg
        rot_array     = np.rot90(data, 3)
        # Next we will flip the image horizontally
        flipped_array = np.fliplr(rot_array)
        final_image   = Image.fromarray(flipped_array)
        return final_image