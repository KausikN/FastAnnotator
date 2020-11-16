'''
Used to rename annotations
'''

# Imports
import os
import cv2
import matplotlib.pyplot as plt

import XMLSupport

# Main Functions
def AnnotationRename_Replace(Data, to_replace, replace_with, selectionPrefix):
    if not type(Data['annotation']['object']) == type([]):
        if Data['annotation']['object']['name'].startswith(selectionPrefix) or selectionPrefix == '':
            Data['annotation']['object']['name'] = Data['annotation']['object']['name'].replace(to_replace, replace_with)
    else:
        for i in range(len(Data['annotation']['object'])):
            if Data['annotation']['object'][i]['name'].startswith(selectionPrefix) or selectionPrefix == '':
                Data['annotation']['object'][i]['name'] = Data['annotation']['object'][i]['name'].replace(to_replace, replace_with)
    return Data

def AnnotationRename_KeyCheck(Data, keyCheckName, equalOnly=True):
    if not type(Data['annotation']['object']) == type([]):
        if equalOnly:
            if Data['annotation']['object']['name'] == keyCheckName:
                return True
        elif keyCheckName in Data['annotation']['object']['name']:
            return True
    else:
        for i in range(len(Data['annotation']['object'])):
            if equalOnly:
                if Data['annotation']['object'][i]['name'] == keyCheckName:
                    return True
            elif keyCheckName in Data['annotation']['object'][i]['name']:
                return True
    return False

def AnnotationRename_ReplaceFull(Data, replacements):
    if not type(Data['annotation']['object']) == type([]):
        for k in replacements.keys():
            if Data['annotation']['object']['name'] == k:
                Data['annotation']['object']['name'] = replacements[k]
    else:
        for i in range(len(Data['annotation']['object'])):
            for k in replacements.keys():
                if Data['annotation']['object'][i]['name'] == k:
                    Data['annotation']['object'][i]['name'] = replacements[k]
    return Data

def ReadReplacementFile(path):
    text = open(path, 'r').readlines()
    replacements = {}
    for line in text:
        if ':' in line:
            replacements[line.split(':')[0].strip()] = line.split(':')[1].strip()
    return replacements

def WriteKeyNamesToFile(Data, path):
    names = []
    if not type(Data['annotation']['object']) == type([]):
        names.append(Data['annotation']['object']['name'] + "\n")
    else:
        for i in range(len(Data['annotation']['object'])):
            names.append(Data['annotation']['object'][i]['name'] + "\n")

    open(path, 'w').writelines(names)

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

selectionPrefix = ''
# to_replace = ' '
# replace_with = '_'
# keyCheckName = ' '
# equalOnly = False
save_prefix = ''

keynamePath = 'RenameTest/' + 'Replacements_5.txt'

# keyChecksFiles = []

for filename in filenames:
    # Read XML
    Data = XMLSupport.XMLFile2Dict(mainPath + filename)

    # Change Values
    # Data = AnnotationRename_Replace(Data, to_replace, replace_with, selectionPrefix)
    # keyCheck = AnnotationRename_KeyCheck(Data, keyCheckName, equalOnly)
    # if keyCheck:
    #     keyChecksFiles.append(filename)

    # Write KeyNames
    # WriteKeyNamesToFile(Data, keynamePath)
    replacements = ReadReplacementFile(keynamePath)
    Data = AnnotationRename_ReplaceFull(Data, replacements)

    # Write to File
    savePath = os.path.splitext(filename)[0] + save_prefix + os.path.splitext(filename)[1]
    XMLSupport.Dict2XMLFile(Data, mainPath + savePath)

    # Make Image
    # name = os.path.splitext(filename)[0]
    # I = cv2.imread(mainPath + os.path.splitext(filename)[0] + ".jpg")
    # I = cv2.resize(I, (1684, 2187))
    # cv2.imwrite(mainPath + os.path.splitext(filename)[0] + "_N" + ".jpg", I)

# print(keyChecksFiles)