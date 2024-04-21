import numpy as np
import cv2

def single_scale_Retinex(raw_img, sigma):
    log_img = np.log10(raw_img) - np.log10(cv2.GaussianBlur(raw_img, (0, 0), sigma)) # sigma = 15
    return log_img

# if __name__ == '__main__':
#     img = cv2.imread('./tests/000001.jpg')

#     plt.figure()
#     plt.subplot(1,2,1); plt.imshow(img)
#     plt.subplot(1,2,2); plt.imshow(single_scale_Retinex(img))
#     plt.show()