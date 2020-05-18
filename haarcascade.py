# OpenCV Python program to detect cars in video frame 
# import libraries of python OpenCV  
import cv2 
import numpy as np
from nms import non_max_suppression_fast
  
# capture frames from a video 
cap = cv2.VideoCapture('3.mp4') 
#cap = cv2.VideoCapture('Case2.avi') 
#cap = cv2.VideoCapture('Case1.wmv') 

# Trained XML classifiers describes some features of some object we want to detect 
car_cascade = cv2.CascadeClassifier('haarcascade_cars.xml') 
  

# all points
points = []
CXP, CYP = 0, 0
# loop runs if capturing has been initialized. 
while True: 
    # reads frames from a video 
    ret, frames = cap.read() 
    
    if ret:
        # convert to gray scale of each frames 
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY) 
          
    
        # Detects cars of different sizes in the input image 
        cars = car_cascade.detectMultiScale(gray, 1.03, 5, minSize=(50, 50)) 
        
        cars = non_max_suppression_fast(cars, 0.1)
        

        
        # To draw a rectangle in each cars 
        for (x,y,w,h) in cars: 
            # Calculating the centroid
            cX = int(x + 0.5 * w)
            cY = int(y + 0.5 * h)
            
            # speed
            speed = np.sqrt((cX-CXP)**2+(cY-CYP)**2)
            speed = np.floor(speed)
            
            # update
            CXP, CYP = cX, cY
            
            # Drawing the centroid
            cv2.drawMarker(frames, (cX, cY), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,line_type=cv2.LINE_8)
            # Drawing the bounding boxes
            cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 2)
             # print angles and speeds
            cv2.putText(frames, "S:"+str(speed), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,.5, (51,51, 0), 1)

            points.append((cX, cY))
        
        for p in points:
                cv2.drawMarker(frames, p, (0, 255, 255), cv2.MARKER_CROSS, markerSize=2, thickness=1,line_type=cv2.LINE_AA)

        
        # Display frames in a window  
        cv2.imshow('video2', frames) 
           
         # Wait for Esc key to stop 
        if cv2.waitKey(33) == 27: 
             break
      
# De-allocate any associated memory usage 
cv2.destroyAllWindows() 