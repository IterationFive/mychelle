'''
Created on Feb 13, 2023

@author: IterationFive
'''
import curses
from wards import Ward, Container, Keymaster
from wards import CENTER, TOP, VERTICAL # @UnusedImport

class Window(Keymaster, Container):
    '''
    A Window ward creates and encapsulates a curses cursewin 
    object and manages its entire area.  
    
    Its constructor has most of the same parameters as 
    Ward's, with the following exceptions.
    
        'container' has been replaced with 'screen'.  All 
        Window wards must link to (or be themselves) a Screen
        ward, and Window ward cannot be in a container.
        
        'x_minimum', 'y_minimum', and 'span' have been 
        removed, as Window wards are not automatically sized.
            
    The following methods extend or replace those in Ward.
    
        Window.show()
        Window.hide()
        
    The following methods have been added.
    
        Window.Window()
        Window.Subwindow()
        Window.getKeyID()
        Window.getKey()
    
    
    '''
    def __init__(self, screen, y_size=None, x_size=None, 
                    y_home=0, x_home=0, 
                    keys=None, padtranslation=None,
                    **kwargs):
        '''
        
        :param screen: a Screen Object
        
        :param y_size: int or None
        :param x_size: int or None
            The dimensions of the cursewin.  If both 
            are None, then the cursewin will be fullscreen.
        
        :param y_home: int
        :param x_home: int
            The location the top left corner of the cursewin
            occupies on the parent screen.  These coordinates
            are NOT offset for borders and margins.  If you want
            to use coordinates that are offset, just feed them
            to screen.remove_offset().
            
            If both y_size and x_size are None,
            x_home and y_home will be ignored.
            
        :param border:
        :param margin:
        :param fg:
        :param bg:
            These properties are identical to those in the 
            Ward class and are passed along without 
            inspection through Container.
            
        :param keys: 
        :param padtranslation:
            see KeyMaster
            by default inherits these from the screen.
        '''
        
        self.screen = screen
        self.window = self
        
        if y_size is None and x_size is None:
            y_size = screen.y_outer
            x_size = screen.x_outer
            y_home, x_home = 0,0 # just in case
        elif y_size is None: y_size = screen.y_inner
        elif x_size is None: x_size = screen.x_inner
            
        self.cursewin = curses.newwin( # @UndefinedVariable 
            y_size, x_size, y_home, x_home)
        
        if keys is None:
            keys= screen.keys
        if padtranslation is None:
            padtranslation= screen.padtranslation
            
        Keymaster.__init__(self, self.cursewin,
                           keys=keys, padtranslation=padtranslation)
        
        Container.__init__(self, None, y_size, x_size, 
                        y_home=y_home, x_home=x_home, 
                        **kwargs )
    def show(self):
        '''
        Extends Ward.show() by executing the curses 
        touchwin() method.
        '''
        self.cursewin.touchwin()
        Ward.show(self)
        
    def hide(self, replacement=None):
        '''
            Replaces Ward.hide() with the equivalent 
            functionality for a curses window.  Unlike 
            Ward.hide(), does not erase the window 
            before putting it away.
            
        :param replacement:
            optional.  another window object that will be 
            brought to the forefront instead.  If not 
            specified, defaults to the parent screen.
        '''
        
        self.visible = False
        
        if replacement is not None:
            replacement.cursewin.touchwin()
            replacement.refresh()
        else:
            self.screen.cursewin.touchwin()
            self.screen.refresh()