# SJTU EE208

import math
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader
import os

# pic = 'huawei3.png'

def getMatch(pic):
    # 只能处理一个在文件夹中已经有的照片
    print("=>Start matching")

    # model = torch.hub.load('pytorch/vision:v0.10.1', 'resnet50', pretrained=True)

    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
    trans = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ])

    path = "test_pic/{}".format(pic)

    test_image = default_loader(path)
    test_image = trans(test_image)
    test_image = torch.unsqueeze(test_image, 0)

    def features_VGG19(x):
        vgg_model_4096 = models.vgg19(pretrained=True)
        new_classifier = torch.nn.Sequential(*list(vgg_model_4096.children())[-1][:4])
        vgg_model_4096.classifier = new_classifier
        image_feature_4096 = vgg_model_4096(x).data[0]
        
        return image_feature_4096

    def getTheta_VGG19(vector1, vector2):
        abs_vec1 = 0
        abs_vec2 = 0
        for i in range(len(vector1)):
            dim1 = vector1[i]
            dim1 = dim1 ** 2
            abs_vec1 += dim1
        for i in range(len(vector2)):
            dim2 = vector2[i]
            dim2 = dim2 ** 2
            abs_vec2 += dim2
        abs_vec1 = math.sqrt(abs_vec1)
        abs_vec2 = math.sqrt(abs_vec2)
        pointpower = 0
        for i in range(len(vector1)):
            dim3 = vector1[i]*vector2[i]
            pointpower += dim3
        cos = pointpower/(abs_vec1*abs_vec2)
        return cos

    image_feature_VGG19_test = features_VGG19(test_image).detach().numpy()

    simliarity_VGG19 = []
    dict_VGG19 = {}
    for filename in os.listdir('allLogos'):
        test_image = default_loader('allLogos'+'/'+filename)
        test_image = trans(test_image)
        test_image = torch.unsqueeze(test_image, 0)
        
        image_feature_VGG19 = features_VGG19(test_image).detach().numpy()
        
        VGG19_theta = getTheta_VGG19(image_feature_VGG19_test, image_feature_VGG19)
        VGG19_theta = round(VGG19_theta, 5) * 100000
        VGG19_theta = - VGG19_theta
        simliarity_VGG19.append(VGG19_theta)
        
        dict_VGG19[VGG19_theta] = filename

    simliarity_VGG19.sort()
    
    output = dict_VGG19[simliarity_VGG19[0]]
    
    output = output[:-4]
        
    return output
        

