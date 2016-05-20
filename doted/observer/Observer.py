# -*- coding: utf-8 -*-


class Observer(object):
    '''The Observer class defines an observer. 
    
    
    Argument(s):
    subject (Subject): Observer subscribe to subject
    '''
    
    
    def __init__(self, subject):
        subject.addObserver(self)
    
    def update(self):
        '''Update the observer.'''
        pass
