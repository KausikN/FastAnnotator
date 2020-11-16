'''
Some preprocessing on forms
'''
# Imports
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pickle

from tqdm import tqdm

# Main Functions
def DescribePixelValues(I):
    values = []
    for v in range(256):
        values.append(0)

    for i in tqdm(range(I.shape[0])):
        for j in range(I.shape[1]):
            values[I[i, j]] += 1
    return values

def BinariseImage(I, threshold=128, invert=False):
    if I.ndim > 2:
        I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    if invert:
        I_b = (I < threshold)
    else:
        I_b = (I >= threshold)
    return I_b

# Selects Pixels with atleast minNeighbours nearby pixels in window
def RegionThresholding(I, W=np.ones((3, 3)), minNeighbours=1):
    I_rt = I.copy()
    for i in tqdm(range(I.shape[0])):
        for j in range(I.shape[1]):
            nMatches = 0
            if I[i, j]:
                for wi in range(-int(W.shape[0]/2), -int(W.shape[0]/2)+W.shape[0]-1):
                    for wj in range(-int(W.shape[1]/2), -int(W.shape[1]/2)+W.shape[1]-1):
                        if W[wi, wj] and I[i+wi, j+wj] and not (wi == 0 and wj == 0):
                            nMatches += 1
                if nMatches < minNeighbours:
                    I_rt[i, j] = 0
    return I_rt

# Finds Similar Window using Correlation
def BinaryCorrelation(I, W):
    I_cor = np.zeros((I.shape[0]-W.shape[0]+1, I.shape[1]-W.shape[1]+1))
    for i in tqdm(range(0, I.shape[0]-W.shape[0]+1)):
        for j in range(0, I.shape[1]-W.shape[1]+1):
            matches = 0
            I_cor[i, j] = np.count_nonzero(I[i:i+W.shape[0], j:j+W.shape[1]] == W[:, :])
    I_cor = I_cor.astype(int)
    return I_cor

def DescribeValues(I, maxVal):
    values = []
    for v in range(maxVal):
        values.append(0)

    for i in tqdm(range(I.shape[0])):
        for j in range(I.shape[1]):
            values[I[i, j]] += 1
    return values

def PruneNearbyPositions(I_specifier, ReplacementSize, overwriteLimit):
    visitedPixels = np.zeros((I_specifier.shape[0], I_specifier.shape[1]))
    for i in tqdm(range(I_specifier.shape[0])):
        for j in range(I_specifier.shape[1]):
            if I_specifier[i, j]:
                if np.count_nonzero(visitedPixels[i:i+ReplacementSize[0], j:j+ReplacementSize[1]]) > (1-overwriteLimit)*ReplacementSize[0]*ReplacementSize[1]:
                    I_specifier[i, j] = False
                else:
                    # Block Pixels
                    visitedPixels[i:i+ReplacementSize[0], j:j+ReplacementSize[1]] = 1
    return I_specifier

def CutPositions(I_specifier, ReplacementImg, ReplacementSize, replacementType='Part'):
    I_disp = np.zeros((I_specifier.shape[0]+ReplacementSize[0]-1, I_specifier.shape[1]+ReplacementSize[1]-1))

    for i in tqdm(range(I_specifier.shape[0])):
        for j in range(I_specifier.shape[1]):
            if I_specifier[i, j]:
                if replacementType == 'Part':
                    I_disp[i:i+ReplacementSize[0], j:j+ReplacementSize[1]] = ReplacementImg[i:i+ReplacementSize[0], j:j+ReplacementSize[1]]
                elif replacementType == 'Full':
                    I_disp[i:i+ReplacementSize[0], j:j+ReplacementSize[1]] = ReplacementImg
    return I_disp

def BoundingBox(Image, pos, window_size, radius=1, color=[0, 0, 0]):
    I = Image.copy()
    window_size = [window_size[0], window_size[1]]
    for wi in range(len(window_size)):
        if pos[wi] + window_size[wi] > Image.shape[wi]:
            window_size[wi] = Image.shape[wi] - pos[wi]
    
    if I.ndim == 2:
        for i in [pos[0], pos[0] + window_size[0]]:
            for p in range(pos[1], pos[1] + window_size[1]):
                I[i, p] = color[0]
                #print("Markx:", i, p, color[0])
        for j in [pos[1], pos[1] + window_size[1]]:
            for p in range(pos[0], pos[0] + window_size[0]):
                I[p, j] = color[0]
                #print("Marky:", p, j, color[0])
    elif I.ndim == 3:
        for i in [pos[0], pos[0] + window_size[0]]:
            for p in range(pos[1], pos[1] + window_size[1]):
                I[i, p, :] = color[:I.shape[2]]
        for j in [pos[1], pos[1] + window_size[1]]:
            for p in range(pos[0], pos[0] + window_size[0]):
                I[p, j, :] = color[:I.shape[2]]

    for ri in range(1, radius+1):
        I = BoundingBox(I, [pos[0]+ri, pos[1]+ri], [window_size[0]-(2*ri), window_size[1]-(2*ri)], radius=0, color=color)
    return I

def ceil(a):
    if (a-float(int(a))) > 0:
        return a + 1
    return a

def NormaliseToRange(I, Range=(0, 255)):
    I_g = I.copy()
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1], 1))
    
    maxVal = np.max(np.max(I_g, axis=1), axis=0)
    minVal = np.min(np.min(I_g, axis=1), axis=0)

    minmaxRange = maxVal - minVal

    for i in range(I_g.shape[0]):
        for j in range(I_g.shape[1]):
            for c in range(I_g.shape[2]):
                I_g[i, j, c] = (((I_g[i, j, c] - minVal[c]) / minmaxRange) * (Range[1] - Range[0])) + Range[0]

    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))

    return I_g

# Driver Code
# Params
path = 'test.jpg'
Window_path = 'test_Window.jpg'
imgSizeRel = 1

# Path Processing
dirpath = os.path.split(path)[0]
filename_Full = os.path.basename(path)
filename_noExt = os.path.splitext(filename_Full)[0]
file_Ext = os.path.splitext(filename_Full)[1]

# Read Image
I = cv2.imread(path, 0)

if not imgSizeRel == 1:
    I = cv2.resize(I, (int(I.shape[1]*imgSizeRel), int(I.shape[0]*imgSizeRel)))

############################################# PREPROCESS #######################################################
# Describe Values
# ValueCounts = DescribePixelValues(I)
# for i in range(256):
#     if ValueCounts[i] > 0:
#         print(i, ":", ValueCounts[i])
# plt.bar(range(256), ValueCounts)
# plt.show()

# Binary Thresholding
threshold = 200
invert = True
"""
I_b = BinariseImage(I, threshold, invert)

# Region Based Thresholding
Window_RT = np.ones((3, 3))
minNeighbours = 2

I_rt = I_b#RegionThresholding(I_b, Window_RT, minNeighbours)

# Display
plt.subplot(1, 3, 1)
plt.imshow(I, 'gray')
plt.subplot(1, 3, 2)
plt.imshow(I_b*255, 'gray')
plt.subplot(1, 3, 3)
plt.imshow(I_rt*255, 'gray')
plt.show()

# Save
cv2.imwrite(os.path.join(dirpath, filename_noExt + "_Bin" + file_Ext), I_b*255)
# cv2.imwrite(os.path.join(dirpath, filename_noExt + "_RegionThresholding" + file_Ext), I_rt*255)

############################################# CORRELATION #######################################################

# Load Data
I_rt = cv2.imread(os.path.join(dirpath, filename_noExt + "_RegionThresholding" + file_Ext))
if not imgSizeRel == 1:
    I_rt = cv2.resize(I_rt, (int(I_rt.shape[1]*imgSizeRel), int(I_rt.shape[0]*imgSizeRel)))
I_rt = BinariseImage(I_rt, threshold, False)


# Params
Window = cv2.imread(Window_path, 0)
if not imgSizeRel == 1:
    Window = cv2.resize(Window, (int(Window.shape[1]*imgSizeRel), int(Window.shape[0]*imgSizeRel)))

Window = BinariseImage(Window, threshold, True)
plt.subplot(1, 2, 1)
plt.imshow(Window*255)
plt.subplot(1, 2, 2)
plt.imshow(I_rt*255)
plt.show()

I_cor = BinaryCorrelation(I_rt, Window)

# Describe Corr Image
ValueCounts = DescribeValues(I_cor, Window.shape[0]*Window.shape[1])
for i in range(len(ValueCounts)):
    if ValueCounts[i] > 0:
        print(i, ":", ValueCounts[i])
plt.bar(range(Window.shape[0]*Window.shape[1]), ValueCounts)
plt.show()

# Save Data
pickle.dump(I_cor, open(os.path.join(dirpath, filename_noExt + "_CorrImg.p"), 'wb'))
pickle.dump(ValueCounts, open(os.path.join(dirpath, filename_noExt + "_ValueCounts.p"), 'wb'))
"""
############################################## PROCESS ###############################################
# Load Data
Window = cv2.imread(Window_path, 0)
I_cor = pickle.load(open(os.path.join(dirpath, filename_noExt + "_CorrImg.p"), 'rb'))
ValueCounts = pickle.load(open(os.path.join(dirpath, filename_noExt + "_ValueCounts.p"), 'rb'))

# Params
corr_threshold = 0.68
overwriteLimit = 1

# Normalise I_cor
I_cor = I_cor.astype(float) / (Window.shape[0]*Window.shape[1])

# Apply Threshold
I_cor_thresholded = I_cor >= corr_threshold
ThresholdPassCount = np.count_nonzero(I_cor_thresholded)
print("ThresholdPassCount:", ThresholdPassCount, "/", I_cor.shape[0]*I_cor.shape[1])

# Display Areas
ReplacementSize = (Window.shape[0], Window.shape[1])

I_cor_thresholded = PruneNearbyPositions(I_cor_thresholded, ReplacementSize, overwriteLimit)
print("Pruned ThresholdPassCount:", np.count_nonzero(I_cor_thresholded), "/", I_cor.shape[0]*I_cor.shape[1])

I_disp = CutPositions(I_cor_thresholded, Window, ReplacementSize, replacementType='Full') * 255
plt.imshow(I_disp)
plt.show()

cv2.imwrite(os.path.join(dirpath, filename_noExt + "_DetectedPos" + file_Ext), I_cor_thresholded*255)
cv2.imwrite(os.path.join(dirpath, filename_noExt + "_CutPos" + file_Ext), I_disp)