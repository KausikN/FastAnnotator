'''
Describe Images
'''

# Imports
import os
import cv2
import numpy as np

# Main Functions
def ImagesSizesCount_Range(paths, ranges):
    RangeCounts = [0]*len(ranges)
    for path in paths:
        I = cv2.imread(path, 0)
        for i in range(len(RangeCounts)):
            if I.shape[0] >= ranges[i][0][0] and I.shape[1] <= ranges[i][0][1]:
                if I.shape[1] >= ranges[i][1][0] and I.shape[1] <= ranges[i][1][1]:
                    RangeCounts[i] += 1
        del I
    return RangeCounts

def ImageAnnotationsDoneCount(paths):
    DoneCount = 0
    FinishedPaths = []
    PendingPaths = []
    for path in paths:
        finished = False
        for imgext in ['.jpg', '.png']:
            if path.endswith(imgext):
                xmlpath = path[:-len(imgext)] + '.xml'
                if os.path.isfile(xmlpath):
                    DoneCount += 1
                    FinishedPaths.append(path)
                    finished = True
                    break
        if not finished:
            PendingPaths.append(path)
    return DoneCount, FinishedPaths, PendingPaths

# Driver Code
# Params
AutoDetectFiles = True

mainPath = 'Alabama_Second_page/Clean/'
filepaths = []
if AutoDetectFiles:
    for (dirpath, dirnames, fnames) in os.walk(mainPath):
        for fname in fnames:
            if os.path.splitext(fname)[-1] in ['.jpg', '.png']:
                filepaths.append(mainPath + fname)
        break

# # Describe Sizes
# Ranges = [([3000, 4000], [2000, 3000]), ([2000, 3000], [1000, 2000])]

# print("Total Files:", len(filepaths))

# RangeCounts = ImagesSizesCount_Range(filepaths, Ranges)

# for ran, rancount in zip(Ranges, RangeCounts):
#     print(ran, ":", rancount)

# Describe Count of Done Annotations
DoneCount, FinishedPaths, PendingPaths = ImageAnnotationsDoneCount(filepaths)
print("Finished Annotations for", DoneCount, "/", len(filepaths))

# Describe pending Image Sizes
# Describe Sizes
Ranges = [([3000, 4000], [2000, 3000]), ([2000, 3000], [1000, 2000])]

RangeCounts = ImagesSizesCount_Range(PendingPaths, Ranges)

print("Pending Annotations Image Size Counts:")
for ran, rancount in zip(Ranges, RangeCounts):
    print(ran, ":", rancount)