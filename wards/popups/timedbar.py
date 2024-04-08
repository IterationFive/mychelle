'''
Created on Apr 8, 2024

@author: IterationFive
'''

from wards import Window

class TimedBar(Window):
    '''
    classdocs
    '''


    def __init__(self, parent, message, timeout=2000, style=None):
        '''
        Constructor
        '''
        message = message.split('\n')
        height=len(message)
        
        y_home, x_home = parent.window_coords( 
            parent.y_outer - height, 0 )
        
        Window.__init__(self, parent.screen, height, parent.x_outer, 
                        y_home=y_home, x_home=x_home)
        
        if style is not None:
            self.name_style('default', style )
            
        self.show()
        
        y = 0
        
        for line in message:
            x = int( (self.x_inner - len(line) ) / 2 )
            self.add_string(y, x, line, style=style)
            y+=1
            
        self.refresh()
        self.nap(timeout)
        self.hide()
            