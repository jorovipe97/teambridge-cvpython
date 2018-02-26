# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 13:42:29 2018

@author: Jose VIllalobos
"""
import numpy as np
import cv2
import modules_cv as app

captura = cv2.VideoCapture(0)
#img = cv2.imread('tucan.jpg', cv2.IMREAD_COLOR)
#print(img.shape)

bg_img = cv2.imread('nature_bg_640x480.jpg')


# Initializes an app sender
appSender = app.Sender()

while(True):
    isDisponible, fotograma = captura.read()
    
    if (isDisponible == True):
        cv2.imshow('Camera', fotograma)
        
        # Flips the image for avoid inverted movement perception in user
        fotograma = cv2.flip(fotograma, 1); # 0 Flipx in x-axis, 1 flips in y-axis, -1 flips in both axis
        
        # Basic segmentation
        segmented_img = app.Segmentation.BasicSegmentation(fotograma, 10)
        
        # Noise Reduction
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (10, 10))
        noise_reduction_img = app.NoiseReduction.Opening(segmented_img, kernel, 3)
        
        # ROI generator
        leftimg, centerimg, rightimg = app.ROIGenerator.DivideImageIn3Columns(noise_reduction_img)
        
        # GAME LOGIC -------------------------------
        
        leftimg_area, centerimg_area, rightimg_area = app.FeaturesCalculator.GetAreas(leftimg, centerimg, rightimg)
        # l, c, r = app.FeaturesCalculator.GetCentroids(leftimg, centerimg, rightimg)
        
        '''
        The goal of this section is calculate in what region of the screen is the player
        We need to know how to deal with two players
        
        Of the 3 regions we need to know which is the active region
        
        Thecnique for know if a region is active.
        
        * The area in the region should be greater than 40 million
        * If two regions have an area greater than 40 million. Then, the region with the biggest area is the active one
        
        NOTE: The centroid is not needed for this algorithm
        '''
        areas_arr = [leftimg_area, centerimg_area, rightimg_area]
        
        activeRegion = app.ActiveRegion.nothing
        
        indexOfMaxArea = np.argmax(areas_arr)
        # if the bigger area is greater than 4 million then that index is the active region
        if (areas_arr[indexOfMaxArea] > 4E6):
            if (indexOfMaxArea == app.ActiveRegion.left):
                activeRegion = app.ActiveRegion.left
                #print('The left is the active region')
            elif (indexOfMaxArea == app.ActiveRegion.center):
                activeRegion = app.ActiveRegion.center
                #print('The center is the active region')
            elif (indexOfMaxArea == app.ActiveRegion.right):
                activeRegion = app.ActiveRegion.right
                #print('The right is the active region')
            else:
                activeRegion = app.ActiveRegion.nothing
                #print('There is no active region')
        
        # Sender Module
        appSender.SendActiveRegionOptimized(activeRegion)
        
        cv2.imshow('Left', leftimg)
        cv2.imshow('Center', centerimg)
        cv2.imshow('Right', rightimg)
        
    else:
        print('Camera not available')
        app.Segmentation.ResetStaticFields()
    
    # Waits for 25ms
    wait = 0xFF & cv2.waitKey(10)
    if (wait == ord('q') or wait == ord('Q')):
        print('Here we go')
        break

captura.release()
cv2.destroyAllWindows()

