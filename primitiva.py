import cv2 as cv
import numpy as np
img = np.ones((500, 500, 3), dtype=np.uint8)*255
cv.rectangle(img,(0,500),(500,0),(0,128,128),-1)
cv.line(img, (10,5),(0, 100), (0,0,0), 3)
cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows