# -*- coding: utf-8 -*-

# Copyright (c) 2016 UPMC
# This file is part of dotEd.
# 
# dotEd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# dotEd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with dotEd.  If not, see <http://www.gnu.org/licenses/>.

from controller.GraphicsGraphController import GraphicsGraphController
from controller.MainWindowController import MainWindowController
from controller.TextGraphController import TextGraphController
from model.Graph import Graph
from view.widget.GraphicsGraphView import GraphicsGraphView
from view.widget.MainWindow import MainWindow
from view.widget.TextGraphView import TextGraphView


class Doted(object):
    '''The Doted class provides a main application.
    
    
    Attribute(s):
    model (Graph): Model representing the graph
    graphicsGraphView (GraphicsGraphView): Graphic view
    textGraphView (TextGraphView): Textual view
    graphicsGraphController (GraphicsGraphController): Graphic controller
    textGraphController (TextGraphController): Textual controller
    mainWindow (MainWindow): Application view
    mainWindowController (MainWindowController): Application controller
    '''


    def __init__(self):
        # Model
        self.graphModel = Graph()
        
        # Views
        self.graphicsGraphView = GraphicsGraphView()
        self.textGraphView = TextGraphView()

        # Controllers
        self.textGraphController = TextGraphController(
                                                    self.graphModel,
                                                    self.textGraphView)
        self. graphicsGraphController = GraphicsGraphController(
                                                    self.graphModel,
                                                    self.graphicsGraphView,
                                                    self.textGraphController)

        # Main application
        self.mainWindow = MainWindow()
        self.mainWindowController = MainWindowController(
                                                    self.graphModel,
                                                    self.mainWindow,
                                                    self.textGraphController)
        
        # Adding views to main window
        self.mainWindow.addWidgetToSplitter(self.graphicsGraphView)
        self.mainWindow.addWidgetToSplitter(self.textGraphView)

    def run(self):
        '''Run the application.'''
        self.mainWindow.show()
