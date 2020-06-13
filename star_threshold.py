# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:49:24 2020

@author: tranq
"""

import json
import cv2
import numpy as np

#with open('train_anno_grouped.json', 'r') as f:
#    train_anno = json.load(f)


img              = cv2.imread('train/3/2.png', -1)

#Reduce sensor's hot pixels noise
median           = cv2.medianBlur(img, 5)

#Reduce background illumination which may be caused by light pollution or cloud
blur             = cv2.GaussianBlur(median,(51,51),0)
img_debackground = median.astype(np.int16) - blur.astype(np.int16)*1
img_debackground = img_debackground.clip(min=0)
img_debackground = img_debackground.astype(np.uint8)


blur = cv2.GaussianBlur(img_debackground,(3,3),0)
_ , th =cv2.threshold(img_debackground,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#Apply dilating then closing (MORPH_CLOSE) for connecting the intermittent lines 
#caused by denoising algorithm
#Impotant: only apply MORPH_CLOSE if star traits are not dense!
kernel = np.ones((8,8),np.uint8)
closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
kernel = np.ones((1,1),np.uint8)
dilate = cv2.morphologyEx(closing, cv2.MORPH_DILATE, kernel)

cv2.imwrite('stars.png', dilate)
cv2.waitKey(0)
