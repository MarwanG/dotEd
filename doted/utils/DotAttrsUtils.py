# -*- coding: utf-8 -*-

import re

from enumeration.NodeArgs import NodeArgs
from enumeration.NodeDotAttrs import NodeDotAttrs


class DotAttrsUtils(object):
    '''The DotAttrsUtils class defines a set of functions for dot attributes.
    
    Attribute(s):
    realNumberPattern (str): Pattern for a negative/positive number
    '''


    realNumberPattern = "\s*-?\d+\.?\d*\s*"
    
    @staticmethod
    def formatLabel(label):
        '''Format the dot label attribute.
        
        Argument(s)
        label (str): Label
        '''
        # Must add quotes if there are spaces or EOL
        if ' ' in label or '\n' in label:
            return '"' + label.replace('\n', '\\n') + '"'
        
        return label
            
    @staticmethod
    def extractLabel(labelAttr):
        '''Extract label from a dot label attribute.
        
        Argument(s):
        labelAttr (str): Dot label attribute 
        '''
        # If it starts with a quote, then the label is between quotes : we
        # don't take these quotes
        if labelAttr[0] == '"':
            return labelAttr[1:len(labelAttr) - 1].replace('\\n', '\n')
        
        return labelAttr
    
    @staticmethod
    def formatPos(x, y):
        '''Format the dot pos attribute with x and y coordinates.
        
        Argument(s)
        x (float): x coordinate
        y (float): y coordinate
        '''
        return '"' + str(x) + ',' + str(y) + '"'

    @staticmethod
    def extractPos(posAttr):
        '''Extract x and y coordinates from a dot pos attribute.
        
        Argument(s):
        posAttr (str): Dot pos attribute 
        '''
        result = re.findall(DotAttrsUtils.realNumberPattern, posAttr)
        
        # posAttr if valid if we have two numbers
        if (len(result) < 2):
            return None
        
        return {
            NodeArgs.x: float(result[0]),
            NodeArgs.y: float(result[1])
        }

    @staticmethod
    def checkAttrsForm(dictAttrs):
        '''Return true if attributes in dictAttrs are in valid form.
        
        Argument(s):
        dictAttrs (Dictionary[]): Dictionary of attributes 
        ''' 
        for attr in dictAttrs.keys():
            if attr == NodeDotAttrs.pos.value:
                if not re.search("^\"" + DotAttrsUtils.realNumberPattern +
                                 "," + DotAttrsUtils.realNumberPattern +
                                 "\"$", dictAttrs[attr]):
                    return False
             
        return True
