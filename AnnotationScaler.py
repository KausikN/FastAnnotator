'''
Used to scale the size of all bounding boxes
'''

# Imports
import os
import cv2
import matplotlib.pyplot as plt

import XMLSupport

# Main Functions
def BBScaler(Data, Scale, Padding, selectionPrefix):
    if not type(Data['annotation']['object']) == type([]):
        if Data['annotation']['object']['name'].startswith(selectionPrefix) or selectionPrefix == '':
            PixChange = (
                        (int(Data['annotation']['object']['bndbox']['xmax']) - int(Data['annotation']['object']['bndbox']['xmin'])) * (Scale[0]-1)/2,
                        (int(Data['annotation']['object']['bndbox']['ymax']) - int(Data['annotation']['object']['bndbox']['ymin'])) * (Scale[1]-1)/2
                    )
            Data['annotation']['object']['bndbox']['xmin'] = str(int(int(Data['annotation']['object']['bndbox']['xmin']) - PixChange[0] - Padding[0]))
            Data['annotation']['object']['bndbox']['xmax'] = str(int(int(Data['annotation']['object']['bndbox']['xmax']) + PixChange[0] + Padding[0]))
            Data['annotation']['object']['bndbox']['ymin'] = str(int(int(Data['annotation']['object']['bndbox']['ymin']) - PixChange[1] - Padding[1]))
            Data['annotation']['object']['bndbox']['ymax'] = str(int(int(Data['annotation']['object']['bndbox']['ymax']) + PixChange[1] + Padding[1]))
    else:
        for i in range(len(Data['annotation']['object'])):
            if Data['annotation']['object'][i]['name'].startswith(selectionPrefix) or selectionPrefix == '':
                PixChange = (
                        (int(Data['annotation']['object'][i]['bndbox']['xmax']) - int(Data['annotation']['object'][i]['bndbox']['xmin'])) * (Scale[0]-1)/2,
                        (int(Data['annotation']['object'][i]['bndbox']['ymax']) - int(Data['annotation']['object'][i]['bndbox']['ymin'])) * (Scale[1]-1)/2
                    )
                Data['annotation']['object'][i]['bndbox']['xmin'] = str(int(int(Data['annotation']['object'][i]['bndbox']['xmin']) - PixChange[0] - Padding[0]))
                Data['annotation']['object'][i]['bndbox']['xmax'] = str(int(int(Data['annotation']['object'][i]['bndbox']['xmax']) + PixChange[0] + Padding[0]))
                Data['annotation']['object'][i]['bndbox']['ymin'] = str(int(int(Data['annotation']['object'][i]['bndbox']['ymin']) - PixChange[1] - Padding[1]))
                Data['annotation']['object'][i]['bndbox']['ymax'] = str(int(int(Data['annotation']['object'][i]['bndbox']['ymax']) + PixChange[1] + Padding[1]))
    return Data

def AnnotationScaler(Data, Scale, Padding, selectionPrefix):
    if not type(Data['annotation']['object']) == type([]):
        if Data['annotation']['object']['name'].startswith(selectionPrefix) or selectionPrefix == '':
            Data['annotation']['object']['bndbox']['xmin'] = str(int((int(Data['annotation']['object']['bndbox']['xmin']) * Scale[0]) - Padding[0]))
            Data['annotation']['object']['bndbox']['xmax'] = str(int((int(Data['annotation']['object']['bndbox']['xmax']) * Scale[0]) - Padding[0]))
            Data['annotation']['object']['bndbox']['ymin'] = str(int((int(Data['annotation']['object']['bndbox']['ymin']) * Scale[1]) - Padding[1]))
            Data['annotation']['object']['bndbox']['ymax'] = str(int((int(Data['annotation']['object']['bndbox']['ymax']) * Scale[1]) - Padding[1]))
    else:
        for i in range(len(Data['annotation']['object'])):
            if Data['annotation']['object'][i]['name'].startswith(selectionPrefix) or selectionPrefix == '':
                Data['annotation']['object'][i]['bndbox']['xmin'] = str(int((int(Data['annotation']['object'][i]['bndbox']['xmin']) * Scale[0]) - Padding[0]))
                Data['annotation']['object'][i]['bndbox']['xmax'] = str(int((int(Data['annotation']['object'][i]['bndbox']['xmax']) * Scale[0]) - Padding[0]))
                Data['annotation']['object'][i]['bndbox']['ymin'] = str(int((int(Data['annotation']['object'][i]['bndbox']['ymin']) * Scale[1]) - Padding[1]))
                Data['annotation']['object'][i]['bndbox']['ymax'] = str(int((int(Data['annotation']['object'][i]['bndbox']['ymax']) * Scale[1]) - Padding[1]))
    return Data

# Driver Code
# Params
mainPath = 'Alabama_Second_page/Clean/'
filenames = ['355020729_2_no.xml']
selectionPrefix = ''
Scale = (1705/2550, 2195/3299)#(1694/2550, 2194/3299)
Padding = (-50, -25)
save_prefix = '_Scaled'

for filename in filenames:
    # Read XML
    Data = XMLSupport.XMLFile2Dict(mainPath + filename)

    # Change Values
    Data = AnnotationScaler(Data, Scale, Padding, selectionPrefix)

    # Write to File
    savePath = os.path.splitext(filename)[0] + save_prefix + os.path.splitext(filename)[1]
    XMLSupport.Dict2XMLFile(Data, mainPath + savePath)

    # Make Image
    # name = os.path.splitext(filename)[0]
    # I = cv2.imread(mainPath + os.path.splitext(filename)[0] + ".jpg")
    # I = cv2.resize(I, (1684, 2187))
    # cv2.imwrite(mainPath + os.path.splitext(filename)[0] + "_N" + ".jpg", I)