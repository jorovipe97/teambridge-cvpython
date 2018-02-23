# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:57:43 2018

@author: Jose Villalobos
"""

import numpy as np
import cv2

class Segmentation:
    
    frameCount = 0
    isFirstN = True
    meanBg = 0
    
    '''
    This method is intended to be used inside the video loop,
    return an image where all that puts over image after the first n frames
    will be to draw white (255)
    '''
    @staticmethod
    def BasicSegmentation(img, framesForCalculateBg):
        # Converts the input image to gray scale
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        meanbg = gray_frame
        n = framesForCalculateBg
        # This variable will be used for calculate the mean of the bg
        _a = 1/n
        
        # Calcules the background
        if Segmentation.frameCount < n and Segmentation.isFirstN:
            res = _a*gray_frame
            Segmentation.meanBg += res.astype(np.uint8)
        else:
            Segmentation.isFirstN = False
            meanbg = Segmentation.meanBg.astype(np.uint8)
            
        diff = cv2.absdiff(meanbg, gray_frame)
        a, segmentation = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        
        Segmentation.frameCount += 1
        return segmentation
        
    @staticmethod
    def ResetStaticFields():
        Segmentation.actualFrame = 0
        Segmentation.isFirstN = True
        Segmentation.meanBg = 0
        
        
        
        
        
        
        
    
