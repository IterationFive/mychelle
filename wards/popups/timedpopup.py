'''
Created on Apr 8, 2024

@author: IterationFive
'''

from wards import Window



class TimedPopup(Window):
    '''
    classdocs
    '''


    def __init__(self, parent, message, timeout=2000,
                 border=True, margin=0,
                 style=None, borderstyle=None):
        '''
        Constructor
        '''
        
        message = message.split('\n')
        height = len( message )
        width = 0
        
        for line in message:
            if len(line) > width:
                width = len(line)
        top, bottom, left, right = self.calculate_margins(border, margin)
        height += top + bottom
        width += left + right
                
        y_home = int( ( parent.y_outer - height ) / 2 )
        x_home = int( ( parent.x_outer - width  ) / 2 )
        
        y_home, x_home = parent.window_coords( y_home, x_home)
        
        Window.__init__(self, parent.screen, height, width, 
                        y_home=y_home, x_home=x_home, 
                        border=border, margin=margin )
        
        if style is not None:
            self.name_style('default', style )
        if borderstyle is not None:
            self.name_style('border', borderstyle )
        self.show()
        y = 0
        
        for line in message:
            x = int( (self.x_inner - len(line) ) / 2 )
            self.add_string(y, x, line, style=style)
            y+=1
            
        self.refresh()
        self.nap(timeout)
        self.hide() 
        