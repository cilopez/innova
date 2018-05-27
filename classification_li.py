# -*- coding: utf-8 -*-
"""
Created on Sat May 26 14:00:45 2018

@author: camilo
"""
import os
import torch
import matplotlib.pyplot as plt
from test import visualize_model
from torchvision import datasets


data_transforms = {
    'images': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}

data_dir = 'dataset'
image_datasets = {datasets.ImageFolder(os.path.join(data_dir,'images'),
                                          data_transforms['images'])}
dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=4,
                                             shuffle=True, num_workers=4)

class_names = ['insect', 'leaf']
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def visualize_model(model, num_images=1):
    was_training = model.training
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():

            inputs = dataloaders
            inputs = inputs.to(device)
            #labels = labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images, 1, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_names[preds[j]]))
                imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return class_names[preds[j]]

if __name__ == "__main__":
    PATH =os.path.join(os.getcwd(),"model.pt")
    model_ft = torch.load(PATH)
    visualize_model(model_ft)
    plt.ioff()
    plt.show()