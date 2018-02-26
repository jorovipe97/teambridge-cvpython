# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:57:43 2018

@author: Jose Villalobos

@description: These modules are mean to be used inside the video loop
"""

import numpy as np
import cv2

from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import osc_bundle_builder

IP_OUT = '127.0.0.1'
PORT_OUT = 9000

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
        

class NoiseReduction:
    
    '''
    https://en.wikipedia.org/wiki/Opening_(morphology)
    Mathematical morphology
    The opening is the dilatation of the erotion of a set (image).
    
    Manual abouts using kernels
    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    
    The structuring element is also known as kernel
    '''
    @staticmethod
    def Opening(img, kernel, _iterations):
        erotion = cv2.erode(img, kernel, iterations=_iterations)
        dilatation = cv2.dilate(erotion, kernel, iterations=_iterations)
        
        return dilatation
    
    '''
    The closing is the erotion of the dilatation of a set (image).
    '''
    @staticmethod
    def Closing(img, kernel, _iterations):
        dilatation = cv2.dilate(img, kernel, iterations=_iterations)
        erotion = cv2.erode(dilatation, kernel, iterations=_iterations)
        
        return erotion
    
class ROIGenerator:
    
    @staticmethod
    def DivideImageIn3Columns(img):
        try:
            h, w = img.shape
        except:
            print("Maybe the passed image is not gray scale")
        
        deltaWidth = int(w/3)
        
        # Select all the rows and the columns from 0 to deltaWidth
        left = img[: , :deltaWidth]
        # Select all the rows and the columns from deltaWidth (exclusive) to 2*deltaWidth (inclusive)
        center = img[: , deltaWidth+1:2*deltaWidth]
        # Select all the rows and the columns from 2*deltaWidth (exclusive) to the last column (inclusive)
        right = img[: , (2*deltaWidth)+1:]
        
        return (left, center, right)
        
        
class FeaturesCalculator:
    
    @staticmethod
    def GetArea(img):
        m = cv2.moments(img)
        
        return m['m00'] # This is the area
    
    @staticmethod
    def GetAreas(*images):
        res = []
        try:
            for img in images:
                res.append(FeaturesCalculator.GetArea(img))
        except:
            print('May you dont passed an image')
        
        return np.array(res)
                
    
    @staticmethod
    def GetCentroid(img):
        m = cv2.moments(img)
        
        area = m['m00']
        
        # If momentum is too little. It does not calcule the centroid coordinate
        if (area < 1):
            return
        
        centroid_x = m['m10']/area
        centroid_y = m['m01']/area
        
        # Return x and y coordinate of the centroid
        return [centroid_x, centroid_y]
    
    @staticmethod
    def GetCentroids(*images):
        res = []
        try:
            for img in images:
                res.append(FeaturesCalculator.GetCentroid(img))
        except:
            print('May you dont passed an image - GetCentroids')
        
        print(res)
        return res

class Sender:
    prevActiveRegion = -1
    
    def __init__(self):
        Sender.prevActiveRegion = -1
        self.client = udp_client.SimpleUDPClient(IP_OUT, PORT_OUT)
        self.activeregion_address = '/teambridge/activeregion'
        self.maskimg_address = '/teambridge/img'
    
    def SendActiveRegionOptimized(self, actualActiveRegion):
        if (actualActiveRegion != Sender.prevActiveRegion):
            # Sends the actual region only if different to the previous active region
            self.client.send_message(self.activeregion_address, actualActiveRegion);
            Sender.prevActiveRegion = actualActiveRegion
            # print('Osc Sended')
    
    # This modules is not working fine
    def SendGrayImage(self, img):
        #bundle = osc_bundle_builder.OscBundleBuilder()
        #msg = osc_message_builder.OscMessageBuilder(address=self.maskimg_address)
        #msg.build()
        self.client.send_message(self.maskimg_address, cv2.imencode('.jpg', img)[1].tostring())
            
            
        

class ActiveRegion:
    nothing = -1
    left = 0
    center = 1
    right = 2
                
        
        
        
        
    
