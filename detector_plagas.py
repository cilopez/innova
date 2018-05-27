# -*- coding: utf-8 -*-
"""
Created on Sat May 26 20:19:39 2018

@author: camil
"""

from test import image_read
import cam_detecter
import os


PATH = os.path.join(os.getcwd(),"dataset","val","data")
file = os.listdir(PATH)
print(image_read())
if image_read() == "insect":
    image_processing(file[0])
    