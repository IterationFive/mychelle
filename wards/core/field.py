'''
Created on Mar 31, 2024

@author: IterationFive
'''

from wards import Ward, LEFT, RIGHT, CENTER # @UnusedImport 

class Field(Ward):
    '''
    A Field object is designed to hold a single piece of
    information, which it will automatically display anytime
    update() is called.  
    
    If a field size is being managed by a container, and minimum
    sizes are not manually specified, the minimums will be calculated
    based on the contents, border, and margins.  
    '''


    def __init__(self, *args, 
                 contents='', align=LEFT, 
                 **kwargs):
        '''
        Constructor
        
        The following parameters are inherited from 
        Ward, and most of them are passed to its
        constructor without interaction.
        
        
        :param container: container object or None
        :param x_size: int, MIN, MAX, AUTO
        :param y_size: int, MIN, MAX, AUTO        
        :param x_home: int
        :param y_home: int
        :param y_minimum: int or None
        :param x_minimum: int or None
        :param border:  True, False, list, or string
        :param margin: int or tuple
        :param span: int, default 1
        
        
        
        The following parameters have been added:
        
        :param contents: string 
            The data this field displays to begin.
        :param align: LEFT (default), RIGHT, or CENTER
            How the data is aligned within its alloted
            space.
            
        '''
        self.contents = contents
        self.align = align
        
                
                
        Ward.__init__(self, *args, **kwargs )
        
    def get_minimums(self):
        '''
            Returns either the specified minimums,
            or calculates them based on the contents,
            margin, and borders.
        '''
        
        contents = self.contents.split('\n')
        
        if self.y_minimum is None:
            y_minimum = len(contents)
        else:
            y_minimum = self.y_minimum
        
        if self.x_minimum is None:
            x_minimum = 1
            
            for line in contents:
                if len(line) > x_minimum:
                    x_minimum= len(line)
        else:
            x_minimum = self.x_minimum
            
        left, right, top, bottom = self.calculate_margins( 
                                        self.border, 
                                        self.margin )
        
        if self.y_minimum is None:
            y_minimum += top + bottom
        
        if self.x_minimum is None:
            x_minimum += left + right 
    
        return y_minimum, x_minimum
    
    
    
    
    def update(self):
        '''
        Replaces Ward.update().  Populates the field with the data.
        '''
        y = 0
        self.clear()
        contents = self.contents.split('\n')
        for line in contents:
            if self.align == RIGHT:
                self.add_string( y, self.x_inner - len(line), line)
            elif self.align == CENTER :
                self.add_string( y, 
                    int( ( ( self.x_inner - len(line) ) /2 ) ) , line )
            else:
                self.add_string(y,0,line)
            y += 1
        self.refresh()
        
    def set_contents(self, contents, align=None, refresh=True):
        '''
        Changes the contents of the field.
        
        :param contents: string
            The new contents.            
        :param align: LEFT, RIGHT, or CENTER
            resets the alignment property
        :param refresh: boolean, defaults True
            If true, will update the contents on the 
            screen.  Note that this will not resize
            the field; that has to be done at 
            the container level.
        '''
        if align is not None:
            self.align=align
        if type( contents == str):
            self.contents = contents.split('\n')
        else:
            self.contents = contents
            
        if refresh: self.update()