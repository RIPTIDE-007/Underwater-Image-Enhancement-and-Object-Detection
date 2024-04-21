import numpy as np
from SSR import single_scale_Retinex

'''
    Multi Scale Retinex
    raw_img: -
    sigma_arr: sigmas for Gaussian blur in single scale retinex
    weight_arr: weights corresponding to different Gaussian kernel
'''
def multi_scale_Retinex(raw_img, sigma_arr, weight_arr):
    while len(weight_arr) < len(sigma_arr):
        weight_arr.append(0)
    weight_sum = sum(weight_arr)

    img = np.zeros(raw_img.shape)
    for i in range(len(sigma_arr)):
        w = weight_arr[i] / weight_sum
        img += single_scale_Retinex(raw_img, sigma_arr[i]) * w
    
    return img

if __name__ == '__main__':
    pass
