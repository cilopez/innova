# -*- coding: utf-8 -*-
"""
Created on Sat May 26 14:00:45 2018

@author: camilo
"""
import os
import torch
import matplotlib.pyplot as plt
from test import visualize_model


if __name__ == "__main__":
    PATH =os.path.join(os.getcwd(),"model.pt")
    model_ft = torch.load(PATH)
    visualize_model(model_ft)
    plt.ioff()
    plt.show()