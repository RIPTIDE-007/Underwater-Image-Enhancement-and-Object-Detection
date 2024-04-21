import json
import os
import numpy as np
import json
import cv2
from MSR import multi_scale_Retinex
import matplotlib.pyplot as plt

'''
    Build gamma look up table for fast gamma correction.
'''
def create_gamma_lookup_table(gamma):
    lut = list(range(0, 256))
    if gamma != 0:
        for i in range(0,256):
            lut[i] = int((i / 255) ** (1 / gamma) * 255)
    return lut

'''
    Quantify the logarithmic image data. Clip highest(percentage) and lowest data, use gamma correction to map the others to [0, 255].
    img: Input image. Must be (x, y, c) where c represents channels.
    high_clip: Clip highest data to 255. Default 0.0005 for clipping top 0.05% highest data.
    low_clip: Similar to high_clip.
    gamma: Non-zero value for gamma correction. If gamma=0, skip gamma correction.
'''

def quantify_log_image(img, high_clip=0.005, low_clip=0.005, gamma=0.45):
    lut = create_gamma_lookup_table(gamma)

    for c in range(img.shape[-1]):
        flatten = sorted(img[:,:,c].ravel())
        low = flatten[int(len(flatten) * low_clip)]
        high = flatten[int(len(flatten) * (1 - high_clip))]
        # plt.hist(flatten, 200, [min(flatten), max(flatten)])
        # plt.show()
        temp = np.minimum(np.maximum(img[:,:,c], low), high)
        temp = np.uint8((temp - low) / (high - low) * 255.0)

        # Gamma correction.
        if gamma != 0:
            for i in range(temp.shape[0]):
                for j in range(temp.shape[1]):
                    temp[i][j] = lut[temp[i][j]]
                
        img[:,:,c] = temp

    return np.uint8(img)

'''
    Multi-Scale Retinex with Color Restoration
    see 'A multiscale retinex for bridging the gap between color images and the human observation of scenes'
    at https://ieeexplore.ieee.org/abstract/document/597272

    Final image: 
        R(x, y)=G*(C(x, y)*R(x, y)+b),
    where
        C(x, y)=beta*(log(alpha*I(x, y))-log(I1(x, y)+I2(x, y)+I3(x, y))),
    alpha, beta, high_clip, low_clip, gamma are empirical parameters.
'''

def MSR_color_restoration(original_img, sigma_arr, weight_arr, alpha=125, beta=46, high_clip=0.005, low_clip=0.005,gamma=0.45):
    original_img = np.float64(original_img) + 1.0 # Avoiding numerical unstability cause by log(0) in SSR

    # Basic Multiscale Retinex
    R = multi_scale_Retinex(original_img, sigma_arr, weight_arr)

    # Calculate color restoration function(CRF)
    sigmaI = original_img.sum(axis=2)
    # Expand dims to 3 channels, copy data at (1080,1920,0) along 2nd axis. Expanditure is required for the 2nd axis does not exist.
    sigmaI = np.expand_dims(sigmaI, axis=2).repeat(3, axis=2)
    CRF = beta * (np.log10(alpha * original_img) - np.log10(sigmaI))

    # Quantify
    img = quantify_log_image(CRF * R, high_clip, low_clip, gamma)

    # # Grayscale histogram for testing
    # plt.hist(img[:,:,0].ravel(), 200, [img[:,:,0].min(), img[:,:,0].max()])
    # plt.show()
    
    return img

if __name__ == '__main__':
    # os.chdir('./code') # curdir='../Retinex', set to '../Retinex/code'
    config_path = './config_processing.json'

    with open(config_path) as f:
        config = json.load(f)

    for img_path in os.listdir(config['img_path']):
        img = cv2.imread(config['img_path'] + '/' + img_path)

        processed_img = MSR_color_restoration(
            img,
            config['sigma'],
            config['weights'],
            config['alpha'],
            config['beta'],
            config['high_clip'],
            config['low_clip'],
            config['gamma']
        )
        # cv2.imshow('original image', img)
        # cv2.imshow('MSRCR', processed_img)
        # cv2.waitKey()

        if config['output_result']:
            filename = config['output_path'] + '/{}-MSRCR-gamma{}-clip{}.jpg'.format(img_path.split('/')[-1].split('.')[0], config['gamma'], config['high_clip'])
            cv2.imwrite(filename, processed_img)
            print('Write as ' + filename + '.')



