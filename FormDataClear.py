'''
Python Script to Clear Data from Form Images
'''

# Imports
import os
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

import XMLSupport

# Main Functions


# Driver Code
# Params
AutoDetectFiles = True

mainPath = 'set1_type2/'
Ext = '.xml'

filenames = []
if AutoDetectFiles:
    for (dirpath, dirnames, fnames) in os.walk(mainPath):
        for fname in fnames:
            if os.path.splitext(fname)[-1] == Ext:
                filenames.append(fname)
        break

else:
    PrefixName = 'Delaware_ops_form1_page'
    N = 5

    for n in range(1, N+1):
        filenames.append(PrefixName + str(n) + Ext)

print("N Files:", len(filenames))

BGColor = 255
selectionPrefix = ''
ClearPadding = (0, 0)
saveExt = '.jpg'
saveSuffix = ''

for filename in filenames:
    # Read File and convert to dict
    DataDict = XMLSupport.XMLFile2Dict(mainPath + filename)
    # print(DataDict)

    # Read Corresponding Image
    imgPath = DataDict['annotation']['path']
    print("Reading", imgPath + "...")
    FormImg = cv2.imread(imgPath, 0)
    FormImg_DataCleared = FormImg.copy()

    # Replace Each Bounding Box by BGColor
    Objects = DataDict['annotation']['object']
    if not type(Objects) == type([]):
        Objects = [Objects]

    for obj in tqdm(Objects):
        # print("Clearing " + obj['name'] + "...")
        if obj['name'].startswith(selectionPrefix):
            xmin = int(obj['bndbox']['xmin']) - 1
            xmax = int(obj['bndbox']['xmax']) - 1
            ymin = int(obj['bndbox']['ymin']) - 1
            ymax = int(obj['bndbox']['ymax']) - 1

            FormImg_DataCleared[ymin+ClearPadding[0]:ymax-ClearPadding[0], xmin+ClearPadding[1]:xmax-ClearPadding[1]] = BGColor

    # Plot and Save Data
    saveName = os.path.splitext(DataDict['annotation']['filename'])[0]
    cv2.imwrite(mainPath + saveName + saveSuffix + saveExt, FormImg_DataCleared)

    # plt.subplot(1, 2, 1)
    # plt.imshow(FormImg, 'gray')
    # plt.subplot(1, 2, 2)
    # plt.imshow(FormImg_DataCleared, 'gray')
    # plt.show()