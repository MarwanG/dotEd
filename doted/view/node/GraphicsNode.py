# -*- coding: utf-8 -*-

from PyQt5.Qt import QMarginsF, Qt
from PyQt5.QtWidgets import QGraphicsItem, QMenu

from enumeration.NodeArgs import NodeArgs
from enumeration.NodeDotAttrs import NodeDotAttrs
from utils.DotAttrsUtils import DotAttrsUtils
from view.edge.GraphicsSemiEdge import GraphicsSemiEdge
from view.node.GraphicsTextNode import GraphicsTextNode


class GraphicsNode(object):
    '''The GraphicsNode class defines a base class for a graphics node.
    
    Argument(s):
    id (str): ID of the node
    graphicsGraphView (GraphicsGraphView): View

    Attribute(s):
    id (str): ID of the node
    graphicsGraphView (GraphicsGraphView): View
    graphicsTextNode (GraphicsTextNode): Text (label) of the node
    semiEdge (GraphicsSemiEdge): Line between a graphics node and cursor mouse
    sceneRectHasBeenUpdated (bool): Flag to check if the scene rect has been
                                    updated
    isMoving (bool): Flag to check if a node is moving
    lastX (float): Last x coordinate of the node 
    lastY (float): Last y coordinate of the node
    contextMenu (QMenu): Context menu to edit attributes
    '''


    def __init__(self, id, graphicsGraphView):
        self.id = id;
        self.graphicsGraphView = graphicsGraphView
        
        # Init graphics text node
        self.graphicsTextNode = GraphicsTextNode()
        (self.graphicsTextNode.boundingRect().
                               marginsAdded(QMarginsF(10, 10, 10, 10)))
        
        self.semiEdge = None
        self.sceneRectHasBeenUpdated = False
        
        self.isMoving = False        
        self.lastX = None
        self.lastY = None
        
        self.contextMenu = QMenu()
        # Edit label
        editLabelAction = self.contextMenu.addAction("Edit label")
        editLabelAction.triggered.connect(self.onEditLabel)
    
    def edit(self, dictArgsNode):
        '''Edit all attributes of the node.
        
        Argument(s):
        dictArgsNode (Dictionary[]): Dictionary of arguments of the node
        '''
        self.editLabel(dictArgsNode)
        self.editPos(dictArgsNode)
    
    def editLabel(self, dictArgsNode):
        '''Edit the label.
        
        Argument(s):
        dictArgsNode (Dictionary[]): Dictionary of arguments of the node
        '''
        # Get ID as default label
        label = self.id
        
        # Take value label if it exists
        if (NodeDotAttrs.label.value in dictArgsNode[NodeArgs.dotAttrs] and
            dictArgsNode[NodeArgs.dotAttrs][NodeDotAttrs.label.value]):
                label = DotAttrsUtils.extractLabel(
                            (dictArgsNode[NodeArgs.dotAttrs]
                             [NodeDotAttrs.label.value]))
         
        # Update the text if needed
        if label != self.graphicsTextNode.toPlainText():
            self.graphicsTextNode.setPlainText(label)
    
    def editPos(self, dictArgsNode):
        '''Edit the position.
        
        Argument(s):
        dictArgsNode (Dictionary[]): Dictionary of arguments of the node
        '''
        posChanged = False
        
        # Update x
        if self.x() != dictArgsNode[NodeArgs.x]:
            posChanged = True
            self.setX(dictArgsNode[NodeArgs.x])
        
        # Update y
        if self.y() != dictArgsNode[NodeArgs.y]:
            posChanged = True
            self.setY(dictArgsNode[NodeArgs.y])
        
        # If there was an update
        if posChanged:
            self.graphicsGraphView.updateEdgesOfNode(self)
            
            # Center scene on the node if needed
            if self.graphicsGraphView.updateSceneRect(self):
                self.graphicsGraphView.centerOn(self)
    
    def onEditLabel(self):
        '''Callback function when editing the label.'''
        self.graphicsTextNode.editLabel()
    
    def centerTextInShape(self):
        '''Center the text in the shape.'''
        pass
    
    def getFocus(self, id):
        '''Indicate when node get the focus to highlight him in textual view.
        
        Argument(s):
        id (str): ID of the node
        '''
        self.graphicsGraphView.controller.onSelectItem(id)
        
    def mouseMoveEvent(self, event):
        '''Handle mouse move event.
        
        Argument(s):
        event (QGraphicsSceneMouseEvent): Graphics scene mouse event
        '''        
        # Move the node
        if event.modifiers() == Qt.ControlModifier:
            QGraphicsItem.mouseMoveEvent(self, event)
            
            # Update coordinates of each edge of the current node
            self.graphicsGraphView.updateEdgesOfNode(self)
            
            self.isMoving = True
            self.lastX = event.scenePos().x()
            self.lastY = event.scenePos().y()
            
            # Update scene rect if needed
            if self.graphicsGraphView.updateSceneRect(self):
                self.sceneRectHasBeenUpdated = True
                    
        # Update coordinates of the line
        if self.semiEdge is not None:
            self.semiEdge.update(event.scenePos())
    
    def mousePressEvent(self, event):
        '''Handle mouse press event.
        
        Argument(s):
        event (QGraphicsSceneMouseEvent): Graphics scene mouse event
        '''
        QGraphicsItem.mousePressEvent(self, event)
        
        # Create the semi-edge and get the focus
        if event.buttons() == Qt.LeftButton:
            self.getFocus(self.id)
            self.semiEdge = GraphicsSemiEdge(event.scenePos(), self)
            self.scene().addItem(self.semiEdge)
        elif event.buttons() == Qt.RightButton:
            self.contextMenu.popup(event.screenPos())
        
    def mouseReleaseEvent(self, event):
        '''Handle mouse release event.
        
        Argument(s):
        event (QGraphicsSceneMouseEvent): Graphics scene mouse event
        '''
        QGraphicsItem.mouseReleaseEvent(self, event)
        
        # Notify other view(s) to update position of the node
        if self.isMoving:
            self.isMoving = False
            dicDotAttrs = {}
            dicDotAttrs[NodeDotAttrs.pos.value] = (DotAttrsUtils.formatPos(
                                        self.lastX,
                                        self.lastY))
            self.graphicsGraphView.controller.onEditNode(self.id, dicDotAttrs)
            self.getFocus(self.id)
        
        # Center scene on the node if needed
        if self.sceneRectHasBeenUpdated:
            self.graphicsGraphView.centerOn(self)
            self.sceneRectHasBeenUpdated = False
        
        # Construct edge if a semi edge is built
        if self.semiEdge is not None:
            # Remove the semi edge
            self.scene().removeItem(self.semiEdge)
            self.semiEdge = None
         
            # Filter item on the mouse and only get GraphicsNode
            items = [item for item in self.scene().items(event.scenePos())
                     if isinstance(item, GraphicsNode) and item != self]
            if items:
                # Create edge
                self.graphicsGraphView.controller.onCreateEdge(self.id,
                                                          items[0].id)
                
    def mouseDoubleClickEvent(self, event):
        '''Handle mouse double click event.
        
        Argument(s):
        event (QGraphicsSceneMouseEvent): Graphics scene mouse event
        '''
        # Double click on the text of the node to edit text
        self.graphicsTextNode.editLabel()
