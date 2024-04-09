'''
Created on Apr 8, 2024

@author: IterationFive
'''

from wards import Container, Ward, Field # @UnusedImport
from wards import TOP, BOTTOM, RIGHT, CENTER, MIDDLE  # @UnusedImport
from wards import MIN, MAX, AUTO, VERTICAL  # @UnusedImport


class ButtonMenu(Container):
    '''
    classdocs
    '''

    def __init__(self, *args, 
                 style='default', borderstyle='default', 
                 buttonstyle='reverse', buttonborder='reverse', 
                 **kwargs):
                
        self.items = []
        self.selection = -1
        self.buttonborder = True
        self.buttonmargin = 0
        self.selectedborder = True 
        self.buttonalign = CENTER
        self.selection_keys = [' ', 'enter', 'padenter']
        self.abort_keys = ['escape','backspace' ]
        
        Container.__init__(self, *args, **kwargs)

        self.default_local_style('button', style )
        self.default_local_style('button border', borderstyle)
        self.default_local_style('selected button', buttonstyle)
        self.default_local_style('selected border', buttonborder )
        
    def show(self):
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
                button.name_style( 'default', 'selected button')
                button.name_style( 'border', 'selected border')                
            else:                
                button.name_style( 'default', 'button')
                button.name_style( 'border', 'button border')
                
            self.managed_wards.append(button)
            
        Container.show(self)
        
    def select(self):
        b = self.managed_wards[self.selection]
        b.name_style( 'border', 'selected border')
        b.name_style( 'default', 'selected button' )
        b.show()
             
    def deselect(self):
        b = self.managed_wards[self.selection]
        b.name_style( 'border', 'button border')
        b.name_style( 'default', 'button' )
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
