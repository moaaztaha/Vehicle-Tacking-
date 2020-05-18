# modules
import numpy as np
import cv2

# capture frames from a video 
#cap = cv2.VideoCapture('3.mp4') 
#cap = cv2.VideoCapture('Case2.avi') 
cap = cv2.VideoCapture('Case1.wmv') 


# Initializing Background Subtractor
sub = cv2.createBackgroundSubtractorMOG2()

# last centroid for only one car
CXP, CYP = 0, 0

# the tracked points of all the cars to be drawn
points = []

while True:
    # reading frames from the video
    ret, frame = cap.read()
    
    if not ret: #if vid finish
        break
    

    # Turnning image to gray scale    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converts image to gray
    #cv2.imshow("gray", gray)
        
    # Applying background subtraction
    no_ground = sub.apply(gray)
    #cv2.imshow("no_ground", no_ground) 
        
    # kernel to apply to the morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closing = cv2.morphologyEx(no_ground, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("closing", closing)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    #cv2.imshow("opening", opening)
    
    # removing shadows
    _, bins = cv2.threshold(opening, 30, 255, cv2.THRESH_BINARY)  
    #cv2.imshow("retvalbin", bins)

    dilation = cv2.dilate(bins, kernel)
    #cv2.imshow("dilation", dilation)


    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    minarea = 2000
    # max area for contours, can be quite large for buses
    maxarea = 50000
    # vectors for the x and y locations of contour centroids in current frame
    cxx = np.zeros(len(contours))
    cyy = np.zeros(len(contours))
    
    for i in range(len(contours)):  # cycles through all contours in current frame
        # using hierarchy to only count parent contours instead of non-maximum suppression
        if hierarchy[0, i, 3] == -1:  
            area = cv2.contourArea(contours[i])  # area of contour
            if minarea < area < maxarea:  # area threshold for contour
                # calculating centroids of contours
                cnt = contours[i]
                M = cv2.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                
                # calculating the speed for a single car
                speed = np.sqrt((cx-CXP)**2+(cy-CYP)**2)
                speed = np.floor(speed)
                
                # update current centroid to be used in the next frame
                CXP, CYP = cx, cy
                
                # collect the tracking points
                points.append((cx, cy))
                
                # calculating the angle of contours
                _,_,angle = cv2.fitEllipse(cnt)
                angle = np.floor(angle)
                
                # Getting the location, height and width of the contour
                x, y, w, h = cv2.boundingRect(cnt)
                # draw a rectangle around contour
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Draw the centroid of the contour
                cv2.drawMarker(frame, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,line_type=cv2.LINE_8)
                # print angles and speeds
                cv2.putText(frame, "D:"+str(angle)+","+"S:"+str(speed), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,.5, (51,51, 0), 1)

    # Draw the tracking points for all cars
    for p in points:
        cv2.drawMarker(frame, p, (0, 255, 255), cv2.MARKER_CROSS, markerSize=2, thickness=1,line_type=cv2.LINE_AA)



    # show the final frame
    cv2.imshow("Final Output", frame)
    # ESCAPE key to stop
    key = cv2.waitKey(20)
    if key == 27:
       break
   
cap.release()
cv2.destroyAllWindows()