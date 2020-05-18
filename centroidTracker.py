# modules
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

class CentroidTracker():
    def __init__(self, maxDisappeared=50):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        
        self.maxDisppeared = maxDisappeared
    
    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        # The number of times the object has disappeared
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1
        
    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]
    
    def update(self, rects):
        # in case there's no objects in the frame
        if len(rects) == 0:
            # mark all existing tracked objects as disappeared
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                
                
                # if the consequtive number of disappeared times
                # reached the max number, deregister
                if self.disappeared[objectID] > self.maxDisppeared:
                    self.deregister(objectID)
                
        # in case of detecting rects in the frame
        ## initialize an array of input centriods for the current frame
        inputCentroids = np.zeros((len(rects), 2), dtype='int')
        
        # loop over the bouding box rectangels
        for i, (startX, startY, endX, endY) in enumerate(rects):
            # calc the centroids
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)
        
        # if there's no currently an trakced objects
        # register all the input centroids
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])
        else: # matching the input centroids to existing object
            # get a list of the IDs and centroids
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())
            
            
            # compute the distance between each pair of object centroids and input centroids
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            
            
            ### Our goal is to have the index values with the smallest corresponding distance at the front of the lists.
            # the smallest value in each row, sort the row indexes based on the minimum values
            rows = D.min(axis=1).argsort()
            # find the smallest value in each column, sort boased on ordered rows
            cols = D.argmin(axis=1)[rows]
            
            
            usedRows = set()
            usedCols = set()
            
            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue 
                
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0
                
                usedRows.add(row)
                usedCols.add(col)
                
            # compute both the row and column index we have not yet examined
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)
            
            
            # in case the number of object centroids is equal or greater than the number of input centroids
            # check to see if some of these objects have potentially disappeared
            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1
                    
                    if self.disappeared[objectID] > self.maxDisppeared:
                        self.deregister(objectID)
                
            # the number of input centroids is greater than the number of existing object centroids
            # we have new objects
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])
                
        return self.objects

































            