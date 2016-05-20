# -*- coding: utf-8 -*-

from enumeration.UpdateModeView import UpdateModeView
from observer.Observer import Observer


class Controller(Observer):
    '''The Controller class defines a base class for controllers.
    
    
    Argument(s):
    model (Subject): Model of the controller
    view (View): View of the controller
    
    Attribute(s):
    model (Graph): Model of the Graph in dotEd application
    view (View): View of the controller
    '''


    def __init__(self, model, view):
        # Parent constructor(s)
        Observer.__init__(self, model)
        
        self.model = model
        self.view = view
        self.view.setController(self)
    
    def update(self, dictArgsNode, dictArgsEdge, updateModeView):
        '''Update the view.
        
        Argument(s):
        dictArgsNode (Dictionary[]): Dictionary of arguments of the node
        dictArgsEdge (Dictionary[]): Dictionary of arguments of the edge
        updateModeView (UpdateModeView) : Update mode
        '''
        # Update node
        if dictArgsNode:
            if updateModeView == UpdateModeView.add:
                self.view.addNode(dictArgsNode)
            elif updateModeView == UpdateModeView.edit:
                self.view.editNode(dictArgsNode)
            elif updateModeView == UpdateModeView.remove:
                self.view.removeNode(dictArgsNode)
        
        # Update edge
        else:
            if updateModeView == UpdateModeView.add:
                self.view.addEdge(dictArgsEdge)
            elif updateModeView == UpdateModeView.edit:
                self.view.editEdge(dictArgsEdge)
            elif updateModeView == UpdateModeView.remove:
                self.view.removeEdge(dictArgsEdge)
