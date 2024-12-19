import numpy as np
import cv2 as cv
import math

img = cv.imread('C:/Users/Sauce/Desktop/phyton', 1)
x, y = img.shape
translated_img = np.zeros((x, y), dtype=np.uint8)
dx, dy = 10, 10

for i in range(x):
    for j in range(y):
        new_x = i + dy
        new_y = j + dx
        if 0 <= new_x < x and 0 <= new_y < y:
            translated_img[new_x, new_y]
            
rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)
xx, yy = rotated_img.shape
cx, cy = int(x // 2), int (y // 2)

angle = 60
thehta = math.radians(angle) 

for i in range (x):
    for j in range (y):
        new_rx = int((j - cx)* math.cos(thehta)-(i -cy)*math.sin(thehta)+cx)
        new_ry = int((j - cx)* math.sin(thehta)+(i -cy)*math.cos(thehta)+cy)       
            
cv.imshow('original', img)
cv.imshow('modificada', translated_img)
cv.waitKey(0)
cv.destroyAllWindows()