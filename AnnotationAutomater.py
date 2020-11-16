'''
Tools for automating some annotation processes
'''

# Imports
import os
import cv2
import matplotlib.pyplot as plt
import copy

import XMLSupport

# Main Functions
def GenerateColNames(Prefix, StartVal, NCols):
    names = []
    for i in range(NCols):
        names.append(Prefix + str(StartVal + i))
    return names

def AnnotateAuto_Table(Data, FirstRowNames, NRows, RowGap):
    NewObjects = []
    for i in range(len(Data['annotation']['object'])):
        if Data['annotation']['object'][i]['name'] in FirstRowNames:
            curPos = [int(Data['annotation']['object'][i]['bndbox']['ymin']), int(Data['annotation']['object'][i]['bndbox']['ymax'])]
            y_size = int(Data['annotation']['object'][i]['bndbox']['ymax']) - int(Data['annotation']['object'][i]['bndbox']['ymin'])
            for r in range(1, NRows):
                obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                obj['name'] = obj['name'] + "_" + str(r+1)
                curPos[0] += y_size + RowGap
                curPos[1] += y_size + RowGap
                obj['bndbox']['ymin'] = str(curPos[0])
                obj['bndbox']['ymax'] = str(curPos[1])
                NewObjects.append(obj)
            Data['annotation']['object'][i]['name'] = Data['annotation']['object'][i]['name'] + "_" + str(1)
    Data['annotation']['object'].extend(NewObjects)
    return Data

def AnnotateAuto_Array(Data, StartObjName, Gap, N, y=False):
    NewObjects = []
    for i in range(len(Data['annotation']['object'])):
        if Data['annotation']['object'][i]['name'] == StartObjName:
            if y:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['ymin']), int(Data['annotation']['object'][i]['bndbox']['ymax'])]
                y_size = int(Data['annotation']['object'][i]['bndbox']['ymax']) - int(Data['annotation']['object'][i]['bndbox']['ymin'])
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    obj['name'] = obj['name'] + "_" + str(r+1)
                    curPos[0] += y_size + Gap
                    curPos[1] += y_size + Gap
                    obj['bndbox']['ymin'] = str(curPos[0])
                    obj['bndbox']['ymax'] = str(curPos[1])
                    NewObjects.append(obj)
                Data['annotation']['object'][i]['name'] = Data['annotation']['object'][i]['name'] + "_" + str(1)
            else:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['xmin']), int(Data['annotation']['object'][i]['bndbox']['xmax'])]
                x_size = int(Data['annotation']['object'][i]['bndbox']['xmax']) - int(Data['annotation']['object'][i]['bndbox']['xmin'])
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    obj['name'] = obj['name'] + "_" + str(r+1)
                    curPos[0] += x_size + Gap
                    curPos[1] += x_size + Gap
                    obj['bndbox']['xmin'] = str(curPos[0])
                    obj['bndbox']['xmax'] = str(curPos[1])
                    NewObjects.append(obj)
                Data['annotation']['object'][i]['name'] = Data['annotation']['object'][i]['name'] + "_" + str(1)
            break
    Data['annotation']['object'].extend(NewObjects)
    return Data

def AnnotateAuto_ValueSet(Data, KeyNames, Gap, N, y=False):
    NewObjects = []
    KeyNos = []
    for kn in KeyNames:
        KeyNos.append(kn.split('_')[1])
    for i in range(len(Data['annotation']['object'])):
        if Data['annotation']['object'][i]['name'].split('_')[1] in KeyNos:
            if y:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['ymin']), int(Data['annotation']['object'][i]['bndbox']['ymax'])]
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    NameSplitup = obj['name'].split('_')
                    obj['name'] = NameSplitup[0] + "_" + str(int(NameSplitup[1]) + r*len(KeyNames))
                    if len(NameSplitup) > 2:
                        obj['name'] = obj['name'] + "_" + '_'.join(NameSplitup[2:])
                    curPos[0] += Gap
                    curPos[1] += Gap
                    obj['bndbox']['ymin'] = str(curPos[0])
                    obj['bndbox']['ymax'] = str(curPos[1])
                    NewObjects.append(obj)
            else:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['xmin']), int(Data['annotation']['object'][i]['bndbox']['xmax'])]
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    NameSplitup = obj['name'].split('_')
                    obj['name'] = NameSplitup[0] + "_" + str(int(NameSplitup[1]) + r*len(KeyNames))
                    if len(NameSplitup) > 2:
                        obj['name'] = obj['name'] + "_" + '_'.join(NameSplitup[2:])
                    curPos[0] += Gap
                    curPos[1] += Gap
                    obj['bndbox']['xmin'] = str(curPos[0])
                    obj['bndbox']['xmax'] = str(curPos[1])
                    NewObjects.append(obj)
    Data['annotation']['object'].extend(NewObjects)
    return Data

def AnnotateAuto_KeySet(Data, Names, Gap, N, y=False):
    NewObjects = []
    for i in range(len(Data['annotation']['object'])):
        if Data['annotation']['object'][i]['name'] in Names:
            if y:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['ymin']), int(Data['annotation']['object'][i]['bndbox']['ymax'])]
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    obj['name'] = obj['name'].split('_')[0] + "_" + str(int(obj['name'].split('_')[1]) + r*len(Names))
                    curPos[0] += Gap
                    curPos[1] += Gap
                    obj['bndbox']['ymin'] = str(curPos[0])
                    obj['bndbox']['ymax'] = str(curPos[1])
                    NewObjects.append(obj)
            else:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['xmin']), int(Data['annotation']['object'][i]['bndbox']['xmax'])]
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    obj['name'] = obj['name'].split('_')[0] + "_" + str(int(obj['name'].split('_')[1]) + r*len(Names))
                    curPos[0] += Gap
                    curPos[1] += Gap
                    obj['bndbox']['xmin'] = str(curPos[0])
                    obj['bndbox']['xmax'] = str(curPos[1])
                    NewObjects.append(obj)
    Data['annotation']['object'].extend(NewObjects)
    return Data

def AnnotateAuto_KeySet_Updated(Data, StartNo, Separator, Gap, N, y=False):
    NewObjects = []
    for i in range(len(Data['annotation']['object'])):
        if Data['annotation']['object'][i]['name'].startswith(str(StartNo) + Separator):
            if y:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['ymin']), int(Data['annotation']['object'][i]['bndbox']['ymax'])]
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    obj['name'] = str(StartNo+r) + Separator + Separator.join(obj['name'].split(Separator)[1:])
                    curPos[0] += Gap
                    curPos[1] += Gap
                    obj['bndbox']['ymin'] = str(curPos[0])
                    obj['bndbox']['ymax'] = str(curPos[1])
                    NewObjects.append(obj)
            else:
                curPos = [int(Data['annotation']['object'][i]['bndbox']['xmin']), int(Data['annotation']['object'][i]['bndbox']['xmax'])]
                for r in range(1, N):
                    obj = dict(copy.deepcopy(Data['annotation']['object'][i]))
                    obj['name'] = str(StartNo+r) + Separator + Separator.join(obj['name'].split(Separator)[1:])
                    curPos[0] += Gap
                    curPos[1] += Gap
                    obj['bndbox']['xmin'] = str(curPos[0])
                    obj['bndbox']['xmax'] = str(curPos[1])
                    NewObjects.append(obj)
    Data['annotation']['object'].extend(NewObjects)
    return Data

# Driver Code
# Params
mainPath = 'set1_type2/'
filenames = ['281209273_6_no.xml']
RowGap = 5
NRows = 5
save_prefix = '_SetAuto'

# # Row Names Generation
# RowPrefix = 'value_'
# StartPos = 1
# NCols = 5
# FirstRowNames = GenerateColNames(RowPrefix, StartPos, NCols)

# # Repeated Set Generation
# SetPrefix = 'key_'
# StartPos = 121
# EndPos = 127
# SetNames = []
# for i in range(StartPos, EndPos+1):
#     SetNames.append(SetPrefix + str(i))
# SetGap = 50
# N_Sets = 4
# y_Set = True

# Updated Key Set Generation
StartNo = 1
Separator = ' '
SetGap = 218
N_Sets = 4
y_Set = True

for filename in filenames:
    # Read XML
    Data = XMLSupport.XMLFile2Dict(mainPath + filename)

    # Automate Tables
    # Data = AnnotateAuto_Table(Data, FirstRowNames, NRows, RowGap)

    # Automate Repeated Set
    Data = AnnotateAuto_KeySet_Updated(Data, StartNo, Separator, SetGap, N_Sets, y_Set)
    # Data = AnnotateAuto_KeySet(Data, SetNames, SetGap, N_Sets, y_Set)
    # Data = AnnotateAuto_ValueSet(Data, SetNames, SetGap, N_Sets, y_Set)

    # Write to File
    savePath = os.path.splitext(filename)[0] + save_prefix + os.path.splitext(filename)[1]
    XMLSupport.Dict2XMLFile(Data, mainPath + savePath)