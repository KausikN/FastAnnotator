'''
Script to Shift the Annotations by some amount
'''

# Imports
import os
import cv2
import matplotlib.pyplot as plt

import XMLSupport

# Main Functions
def BBShifter(Data, Shift, selectionPrefix):
    if not type(Data['annotation']['object']) == type([]):
        if Data['annotation']['object']['name'].startswith(selectionPrefix) or selectionPrefix == '':
            Data['annotation']['object']['bndbox']['xmin'] = str(int(Data['annotation']['object']['bndbox']['xmin']) + Shift[0])
            Data['annotation']['object']['bndbox']['xmax'] = str(int(Data['annotation']['object']['bndbox']['xmax']) + Shift[0])
            Data['annotation']['object']['bndbox']['ymin'] = str(int(Data['annotation']['object']['bndbox']['ymin']) + Shift[1])
            Data['annotation']['object']['bndbox']['ymax'] = str(int(Data['annotation']['object']['bndbox']['ymax']) + Shift[1])
    else:
        for i in range(len(Data['annotation']['object'])):
            if Data['annotation']['object'][i]['name'].startswith(selectionPrefix) or selectionPrefix == '':
                Data['annotation']['object'][i]['bndbox']['xmin'] = str(int(Data['annotation']['object'][i]['bndbox']['xmin']) + Shift[0])
                Data['annotation']['object'][i]['bndbox']['xmax'] = str(int(Data['annotation']['object'][i]['bndbox']['xmax']) + Shift[0])
                Data['annotation']['object'][i]['bndbox']['ymin'] = str(int(Data['annotation']['object'][i]['bndbox']['ymin']) + Shift[1])
                Data['annotation']['object'][i]['bndbox']['ymax'] = str(int(Data['annotation']['object'][i]['bndbox']['ymax']) + Shift[1])
    return Data

# Driver Code
# Params
mainPath = 'Alabama_Second_page/Clean/'
filenames = ['357883885_2_no.xml']
selectionPrefix = ''
Shift = (-11, 11)
save_prefix = '_Shifted'

for filename in filenames:
    # Read XML
    Data = XMLSupport.XMLFile2Dict(mainPath + filename)

    # Change Values
    Data = BBShifter(Data, Shift, selectionPrefix)

    # Write to File
    savePath = os.path.splitext(filename)[0] + save_prefix + os.path.splitext(filename)[1]
    XMLSupport.Dict2XMLFile(Data, mainPath + savePath)
    # os.remove(mainPath + filename)