import cv2
import cv2
import numpy as np
#from os import listdir
#from os.path import isfile, join
from math import sqrt
import os
import sys
import time
from matplotlib import pyplot as plt
from MSRCR import MSR_color_restoration

import json

def clahe(bgr):
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    lab_planes=list(lab_planes)
    clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(8,8))

    lab_planes[0] = clahe.apply(lab_planes[0])

    lab = cv2.merge(lab_planes)

    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr

def ih(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    img_ih = plt.hist(img.ravel(), 256, [0,256])
    return img_ih
def imageEnhancer(imageName):
    data_path = r"C:\Users\anand\OneDrive\Desktop\New folder\react\images\input"
    result_path = r"C:\Users\anand\OneDrive\Desktop\New folder\react\images\output"
    img_list = os.listdir(data_path)
    if len(img_list) == 0:
        print('Data directory is empty.')
        exit()

    with open('config_processing.json', 'r') as f:
        config = json.load(f)
    img = cv2.imread(os.path.join(data_path, imageName))
    print(time.strftime("%H:%M:%S", time.localtime()), "Processing image: ", imageName)



    #0 write original image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[0] Original")
    name_0 = "original.jpg"
    cv2.imwrite(os.path.join(result_path, name_0), img)

    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[1] CLAHE")
    img_3 = clahe(img)

    # cv2.imwrite(os.path.join(result_path, name_3), img_3)
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "ENDED CLAHE TIME")
    # THE  RETINEX ALGO

    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[2] Retinex")
    img_2 = MSR_color_restoration(
        img_3,
        config['sigma'],
        config['weights'],
        config['alpha'],
        config['beta'],
        config['high_clip'],
        config['low_clip'],
        config['gamma']
    )

    # cv2.imwrite(os.path.join(result_path, name_2),img_2)
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "ENDED RETINEX TIME")



    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[3] BILATERAL FILTER")
    img_4 = cv2.bilateralFilter(img_2, 7, 25, 9)
    name_4 = "enhanced.jpg"
    cv2.imwrite(os.path.join(result_path, name_4), img_4)
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "ENDED BILATERAL TIME")

