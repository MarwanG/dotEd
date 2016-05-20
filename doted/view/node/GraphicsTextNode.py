# -*- coding: utf-8 -*-

from pydot_ng import graph_from_dot_data

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QGraphicsTextItem, QMessageBox

from enumeration.NodeDotAttrs import NodeDotAttrs
from utils.DotAttrsUtils import DotAttrsUtils


class GraphicsTextNode(QGraphicsTextItem):
    '''The GraphicsTextNode class defines the text of a GraphicsNode.


    Argument(s):
    label (str): Label of the node (default "")
    '''


    def __init__(self, label=""):
        # Parent constructor(s)
        QGraphicsTextItem.__init__(self, label)

    def keyPressEvent(self, event):
        '''Handle key pressed event.

        Argument(s):
        event (QKeyEvent): Key event
        '''
        QGraphicsTextItem.keyPressEvent(self, event)
        self.parentItem().updateShapeAndEdges()
  
    def editLabel(self):
        '''Edit label.'''
        # Enable edit text
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        
        # Go to edit mode text
        self.setFocus()        

    def focusOutEvent(self, event):
        '''Handle focus out event.

        Argument(s):
        event (QFocusEvent ): Focus event
        '''
        QGraphicsTextItem.focusOutEvent(self, event)
        
        # Create a fake node to test if label is valid with pydot
        fakeNode = ("fake[" + NodeDotAttrs.label.value +
                    "=" + self.toPlainText() + "]")
        pydotGraph = graph_from_dot_data("graph{" + fakeNode+ "}")
        
        # Label is valid: we can do the update
        if pydotGraph:
            dicDotAttrs = {
                   NodeDotAttrs.label.value:
                            DotAttrsUtils.formatLabel(self.toPlainText())
                   }
            
            # Update text in other views
            node = self.parentItem()
            node.graphicsGraphView.controller.onEditNode(node.id, dicDotAttrs)
            
            # Disable edit text
            self.setTextInteractionFlags(Qt.NoTextInteraction)
        
        # Label is invalid: force user to write a correct label
        else:
            QMessageBox.warning(None, "Syntax error",
                                "The label is invalid.")
            self.setFocus()
        
    def contextMenuEvent(self, event):
        '''Handle context menu event.
        
        Argument(s):
        event (QGraphicsSceneContextMenuEvent): Graphics scene context menu 
                                                event
        '''
        # Disable context menu (right click)
        pass

    def setPlainText(self, text):
        '''Sets the item's text to text.
        
        Argument(s):
        text (str): New text
        '''
        QGraphicsTextItem.setPlainText(self, text)
        self.parentItem().updateShapeAndEdges()
