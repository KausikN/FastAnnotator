'''
Used to search annotations
'''

# Imports
import os
import cv2
import matplotlib.pyplot as plt

import XMLSupport

# Main Functions
def AnnotationSearch_CAPSKEYS(Data):
    CapsKeys = []
    if not type(Data['annotation']['object']) == type([]):
        if Data['annotation']['object']['name'] == Data['annotation']['object']['name'].upper():
            CapsKeys.append(Data['annotation']['object']['name'])
    else:
        for i in range(len(Data['annotation']['object'])):
            if Data['annotation']['object'][i]['name'] == Data['annotation']['object'][i]['name'].upper():
                CapsKeys.append(Data['annotation']['object'][i]['name'])
    return CapsKeys


# Driver Code
# Params
AutoDetectFiles = True

mainPath = 'set1_type2/'
filenames = []#['281209273_6_no.xml']
if AutoDetectFiles:
    for (dirpath, dirnames, fnames) in os.walk(mainPath):
        for fname in fnames:
            if os.path.splitext(fname)[-1] == '.xml':
                filenames.append(fname)
        break

for filename in filenames:
    # Read XML
    Data = XMLSupport.XMLFile2Dict(mainPath + filename)

    CapsKeys = AnnotationSearch_CAPSKEYS(Data)

    if len(CapsKeys) > 0:
        print(filename)

    # Make Image
    # name = os.path.splitext(filename)[0]
    # I = cv2.imread(mainPath + os.path.splitext(filename)[0] + ".jpg")
    # I = cv2.resize(I, (1684, 2187))
    # cv2.imwrite(mainPath + os.path.splitext(filename)[0] + "_N" + ".jpg", I)

# print(keyChecksFiles)