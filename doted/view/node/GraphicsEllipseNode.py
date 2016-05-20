# -*- coding: utf-8 -*-

from PyQt5.Qt import QMarginsF
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem

from view.node.GraphicsNode import GraphicsNode


class GraphicsEllipseNode(GraphicsNode, QGraphicsEllipseItem):
    '''The GraphicsEllipseNode class defines a graphics node as an ellipse 
    containing a text.
    
    
    Argument(s):
    id (str): ID of the node
    graphicsGraphView (GraphicsGraphView): View
    '''


    def __init__(self, id, graphicsGraphView):
        # Parent constructor(s)
        GraphicsNode.__init__(self, id, graphicsGraphView)
        QGraphicsEllipseItem.__init__(self)
        
        # Init text node
        self.graphicsTextNode.setParentItem(self)
        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsSelectable)
        self.centerTextInShape()

    def updateShapeAndEdges(self):
        '''Center the text in the shape and update coordinates of each edge of
           the current node'''
        self.centerTextInShape()
        self.graphicsGraphView.updateEdgesOfNode(self)

    def centerTextInShape(self):
        '''Center the text in the ellipse.'''
        self.setRect(self.graphicsTextNode.boundingRect().
                          marginsAdded(QMarginsF(10, 10, 10, 10)))
