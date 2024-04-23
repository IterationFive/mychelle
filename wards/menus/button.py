'''
Created on Apr 11, 2024

@author: IterationFive
'''


from wards import Container, Field, Window # @UnusedImport
from wards import TOP, BOTTOM, RIGHT, CENTER, MIDDLE  # @UnusedImport
from wards import MIN, MAX, AUTO, VERTICAL  # @UnusedImport

class ButtonMenu(object):
    '''
    classdocs
    '''


    def __init__(self, *args, 
                 items=None,
                 buttonstyle=None, 
                 buttonborderstyle=None,
                 selectedstyle=None, 
                 selectedborderstyle=None,
                 buttonborder=True, 
                 selectedborder=True,
                 buttonalign=CENTER, 
                 buttonmargin=0,
                 selection = -1,  
                 **kwargs):
        '''
        
        :param buttonstyle:
            The default style for a button
        :param buttonborderstyle:
            The button border style
        :param selectedstyle:
            Default style for a selected button
        :param selectedborderstyle:
            Selected button border style
        :param buttonborder:
            True, False, or config  
        :param selectedborder:
            True, False or config.
        :param buttonalign:
            LEFT, RIGHT, CENTER
        '''
        '''
        Constructor
        '''
        super().__init__( *args, **kwargs )
        
        if items is None:
            items = []
        if selectedstyle is None:
            selectedstyle = 'reverse'
        
        self.items = items
        self.buttonstyle = buttonstyle
        self.buttonborderstyle = buttonborderstyle
        self.selectedstyle = selectedstyle
        self.selectedborderstyle = selectedborderstyle
        self.buttonborder = buttonborder
        self.selectedborder = selectedborder
        self.buttonalign = buttonalign
        self.buttonmargin = buttonmargin
        self.selection = selection
        
        self.selection_keys = [' ', 'enter', 'padenter']
        self.abort_keys = ['escape','backspace' ]
        
        


    def build_contents(self):
        self.managed_wards = []
        self.buttonkeys = {}
        
        for i in range(0,len(self.items)):

            if type(self.items[i]) == str:
                item = self.items[i]
            else:
                item = self.items[i][0]
                self.buttonkeys[self.items[i][1]] = i
                
            button = Field(self, 
                    MIN, MAX, 0,0, 
                    margin = self.buttonmargin,
                    border = self.buttonborder,
                    align = self.buttonalign,
                    contents=item) 
            
            if i == self.selection:                
                button.name_style( 'default', self.selectedstyle )
                button.name_style( 'border',  self.selectedborderstyle)                
            else:
                button.name_style( 'default', self.buttonstyle)
                button.name_style( 'border', self.buttonborderstyle)
                
            self.managed_wards.append(button)
            
    def show(self,*args):
        if len (self.managed_wards) == 0:
            self.build_contents()
        super().show(*args)
        
    def select(self):
        b = self.managed_wards[self.selection]
        b.name_style( 'default', self.selectedstyle )
        b.name_style( 'border', self.selectedborderstyle )
        b.show()
             
    def deselect(self):
        b = self.managed_wards[self.selection]
        if self.buttonstyle == 'default' or self.buttonstyle is None:
            # the definition of 'default' may have been 
            # overriden
            b.styles['default'] = self.find_style('default')
        else:          
            b.name_style( 'default', self.buttonstyle )
        b.name_style( 'border', self.buttonborderstyle)
        b.show()    

    def get_selection(self, selection=None,
                        translateKeypad=True, 
                        forceLowercase=True,
                        navkeys=True):
        
        if selection is not None:
            self.selection = selection
            
        self.show()
        
        while True:
            key = self.window.get_key_by_name(
                translateKeypad, forceLowercase )
            
            if key == 'down' and navkeys == True:       
                if self.selection < len( self.items ) - 1 :
                    self.deselect()
                    self.selection += 1
                    self.select()
            elif key == 'up' and navkeys == True:
                if self.selection > 0:
                    self.deselect()
                    self.selection -= 1
                    self.select()
            elif key in self.buttonkeys:
                self.deselect()
                self.selection = self.buttonkeys[key]
                self.select()
                return self.buttonkeys[key]
            elif key in self.abort_keys:
                self.deselect()
                if selection is not None:
                    self.selection = selection
                    self.select()
                    return selection
                else:
                    return False                
            elif key in self.selection_keys:
                return self.selection

class ButtonMenuBox(ButtonMenu,Container):
    pass

class ButtonMenuWindow(ButtonMenu,Window):
    pass

