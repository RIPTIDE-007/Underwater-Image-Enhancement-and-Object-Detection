from detectron2.engine import DefaultPredictor

import os
import pickle
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2 import model_zoo

from detectron2.utils.visualizer import ColorMode
import time
import random
import cv2
import matplotlib.pyplot as plt
# from utils import *
def on_image(predictor):

    output_directory = r"C:\Users\anand\OneDrive\Desktop\New folder\react\images\output"
    im = cv2.imread(os.path.join(output_directory, "enhanced.jpg"))
    outputs = predictor(im)
    v = Visualizer(im[:,:, ::- 1], metadata ={"thing_classes":['e', 'Bottle', 'Can', 'Fishing_Net', 'Packaging_Bag', 'Plastic_Bag', 'Plastic_Debris']}, scale=1.0, instance_mode=ColorMode. SEGMENTATION)
    V = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    output_file_path = os.path.join(output_directory, f'object.jpg')
    cv2.imwrite(output_file_path, V.get_image()[:, :, ::-1])
    # plt.figure(figsize=(14,10))
    # plt.imshow(V.get_image())
    # plt.show()


def objectDetector():
    print("  ", time.strftime("%H:%M:%S", time.localtime()),"[4]OBJECT DETECTION")
    cfg_save_path = "config.pkl"
    OUTPUT_DIR="./finalmodel"
    with open(cfg_save_path, 'rb') as f:
        cfg = pickle. load(f)

    cfg.MODEL.WEIGHTS = os.path.join(OUTPUT_DIR, "model_final.pth")
    cfg.MODEL. ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.MODEL.DEVICE = "cpu"
    predictor = DefaultPredictor(cfg)
    on_image(predictor)
    print("  ", time.strftime("%H:%M:%S", time.localtime()),"ENDED OBJECT DETECTION")
objectDetector()