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
                 border=True,
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
        super().__init__( *args, border=border, **kwargs )
        
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
            
            if key in self.buttonkeys:
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
            elif navkeys == True: 
                if ( self.selection < len( self.items ) - 1
                     and ( 
                     ( self.orientation == VERTICAL and key == 'down') 
                     or
                     ( self.orientation != VERTICAL and key == 'right') ) ):
                    self.deselect()
                    self.selection += 1
                    self.select()
                elif ( self.selection > 0
                     and ( 
                     ( self.orientation == VERTICAL and key == 'up') 
                     or
                     ( self.orientation != VERTICAL and key == 'left') ) ):
                    self.deselect()
                    self.selection -= 1
                    self.select()

class ButtonMenuBox(ButtonMenu,Container):
    pass

class ButtonMenuWindow(ButtonMenu,Window):
    
    
    def __init__(self, parent, 
                items = None,
                buttonborder=True, 
                buttonmargin=0, 
                border = True,
                margin = 0, 
                orientation = VERTICAL,
                spacing=0,
                **kwargs):
        top, bottom, left, right = self.calculate_margins(border, margin)
        
        width = left + right
        height = top + bottom
        
        
        top, bottom, left, right = self.calculate_margins(
            buttonborder, buttonmargin)
        
        bwidth = 0
        bheight = 0
        
        for i in items:
            lines = i[0].split('\n')
        
            if orientation == VERTICAL:
                bheight += top + bottom + len( lines ) + spacing
                for line in lines:
                    if len(line) + left +right  > bwidth :
                        bwidth = len( line ) + left + right 
            else:
                w = 0
                for line in lines:
                    if len(line) > w:
                        w = len(line)
                bwidth += w + left + right + spacing
                if top+bottom+len(lines) > bheight:
                    bheight = top+bottom+len(lines)
                    
        if orientation == VERTICAL:
            bheight -= spacing
        else:
            bwidth -= spacing
            
        height += bheight
        width += bwidth            
        
        y_home = int( ( parent.y_outer - height ) / 2 )
        x_home = int( ( parent.x_outer - width  ) / 2 )
        
        y_home, x_home = parent.window_coords( y_home, x_home )
        
        ButtonMenu.__init__(self, parent.screen, height, width, 
                        y_home=y_home, x_home=x_home, 
                        border=border, margin=margin,
                        orientation = VERTICAL,
                        spacing=0,
                        buttonborder=buttonborder, 
                        buttonmargin=buttonmargin, 
                        items = items,
                        **kwargs)
        

