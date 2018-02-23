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

isFirstFrame = True
n = 10
index = 0
nFotogramas = []

shader = 0
out = 0
_a = 1/n
isFirstN = True
bg_img = cv2.imread('nature_bg_640x480.jpg')

while(True):
    isDisponible, fotograma = captura.read()
    
    if (isDisponible == True):
        cv2.imshow('Camera', fotograma)
        segmented_img = app.Segmentation.BasicSegmentation(fotograma, 10)
        cv2.imshow('Segmentation', segmented_img)
        '''
        fotograma_gris = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)
        
        # Checks the first video frame
        if (isFirstFrame):
            shader = np.zeros(fotograma_gris.shape, np.uint8)
            out = np.zeros(fotograma_gris.shape, np.uint8)
            isFirstFrame = False
        
        
        # shader = cv2.absdiff(lastFotograma, fotograma)
        
        if (index < n and isFirstN):
            res = _a*fotograma_gris
            shader += res.astype(np.uint8)
        elif (index >= n):                
            index = 0
            nFotogramas = []
            out = shader
            # shader = np.zeros(fotograma.shape, np.uint8)
            isFirstN = False
            
            
        diff = cv2.absdiff(out, fotograma_gris)
        a, mask1 = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        focus = cv2.bitwise_and(fotograma, fotograma, mask=mask1)
        bg_mask = cv2.bitwise_and(bg_img, bg_img, mask=1-mask1)
        res = cv2.add(focus, bg_mask);
        
        #res = shader.astype(np.uint8)
        cv2.imshow('Prmedio', mask1 )
        cv2.imshow('Diff', diff)
        index = index + 1
        '''
        
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

