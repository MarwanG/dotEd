# -*- coding: utf-8 -*-

from controller.Controller import Controller


class TextGraphController(Controller):
    '''The TextGraphController class defines a controller to manage
       a Graph (model)/TextGraphView (view).
    
    
    Argument(s):
    model (Model): Model of the controller
    view (View): View of the controller
    '''


    def __init__(self, model, view):
        # Parent constructor(s)
        Controller.__init__(self, model, view)

    def update(self, dictArgsNode, dictArgsEdge):
        '''Update the view.
        
        Argument(s):
        dictArgsNode (Dictionary[]): dictionary of arguments of the node
        dictArgsEdge (Dictionary[]): dictionary of arguments of the edge
        ''' 
        if dictArgsNode: 
            self.view.updateNode(dictArgsNode)
        else:
            self.view.updateEdge(dictArgsEdge)
