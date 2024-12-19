import cv2 
import numpy as np
width, heigth = 1000, 1000
img =np.ones((heigth, width, 3), dtype=np.uint8)*255

a, b = 150, 150 
k = 1
theta_increment = 0.05
max_theta = 2*np.pi
center_x, center_y = width // 2, heigth // 2
theta = 0
while True:
    img =np.ones((heigth, width, 3), dtype=np.uint8)*255
    for t in np.arange(0,theta, theta_increment):
        r = a + b * np.cos(k*t)
        x = int(center_x + r * np.cos(t))
        y = int(center_y + r * np.cos(t))
        cv2.circle(img,(x , y),2,(100,0,255),2)
        cv2.circle(img,(x+2 , y+2),2,(255,0,255),2)
        
        
    cv2.imshow("Parametric animation", img)
    theta += theta_increment
    if cv2.waitKey(30) & 0xFF == 27:
            break
        
        
cv2.destroyAllWindows
            


