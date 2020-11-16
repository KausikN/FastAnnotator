'''
XML Code Generator
'''

# Imports
from xml.etree import cElementTree as ElementTree
import xmltodict

# Main Functions
# XML Parsing
class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

def XMLFile2Dict(filepath):
    # Method 1
    # tree = ElementTree.parse(filepath)
    # root = tree.getroot()
    # xmldict = XmlDictConfig(root)

    # Method 2
    xmldict = xmltodict.parse(open(filepath, 'r').read())

    return xmldict

def Dict2XMLFile(Data, filepath):
    xmltodict.unparse(Data, open(filepath, 'w'))

# XML Generation
def GenerateBoxesCode(formatCode, name_prefix, boxCount, boxSize, startPos, nextWidth):
    code = []
    curPos = (startPos[0], startPos[1])
    for i in range(boxCount):
        fC = '\n'.join(formatCode)
        name = name_prefix + str(i+1)
        fC = fC.replace('/name', name)
        fC = fC.replace('/x0', str(curPos[0]))
        fC = fC.replace('/x1', str(curPos[0]+boxSize[0]))
        fC = fC.replace('/y0', str(curPos[1]))
        fC = fC.replace('/y1', str(curPos[1]+boxSize[1]))
        curPos = (curPos[0]+nextWidth[0], curPos[1]+nextWidth[1])
        code.append(fC)
    return '\n'.join(code)
        

# Driver Code
# formatCode = [
#     '<object>',
#     '   <name>/name</name>',
#     '   <pose>Unspecified</pose>',
#     '   <truncated>0</truncated>',
#     '   <difficult>0</difficult>',
#     '   <bndbox>',
#     '       <xmin>/x0</xmin>',
#     '       <ymin>/y0</ymin>',
#     '       <xmax>/x1</xmax>',
#     '       <ymax>/y1</ymax>',
#     '   </bndbox>',
#     '</object>'
# ]

# name_prefix = 'value_9_'
# boxCount = 17
# startPos = (5, 407)
# boxSize = (67, 73)
# nextWidth = (68, 0)

# code = GenerateBoxesCode(formatCode, name_prefix, boxCount, boxSize, startPos, nextWidth)
# print(code)
# open('code.txt', 'w').write(code)