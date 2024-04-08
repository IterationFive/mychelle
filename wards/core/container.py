'''
Created on Feb 19, 2023

@author: IterationFive
'''

from wards import Ward
from wards import TOP, BOTTOM, RIGHT, CENTER, MIDDLE
from wards import MIN, MAX, AUTO, VERTICAL

class Container(Ward):
    
    def __init__(self, *args, 
                  y_align=TOP, x_align=CENTER, 
                  orientation = VERTICAL, spacing=0,
                  **kwargs):
        
        self.y_align = y_align
        self.x_align = x_align
        self.spacing = spacing
        self.orientation = orientation
        
        self.managed_wards = []
        
        Ward.__init__(self, *args, **kwargs)

    def manage_contents(self):
               
        if self.orientation == VERTICAL:
            available_space = self.y_inner
        else:
            available_space = self.x_inner
            
        autominimum = 0 
        # the minimum size of the largest 
        # AUTO on the alignment axis
        offminimum = 0 
        # the minimum size of the largest 
        # AUTO on the off-axis
        autocount = 0 
        # the number of wards set to auto (+ extra spans)
        maxcount = 0 
        # the number of wards set to MAX
        spacers = -1 
        # the number of spaces between wards.  
        
        for ward in self.managed_wards:
            if ward.visible is None:
                continue
            
            y_min, x_min = ward.get_minimums()
            if self.orientation == VERTICAL:
                
                if ward.x_setting == AUTO and x_min > offminimum:
                    offminimum = x_min
                
                if ward.y_setting > 0:
                    #static size configuration
                    ward.y_outer = ward.y_setting
                    available_space -= ward.y_setting
                    spacers += 1
                elif ward.y_setting == MIN:
                    #use the minimum
                    ward.y_outer = y_min
                    available_space -= y_min
                    spacers += 1
                elif ward.y_setting == AUTO:
                    #this is trickier, as we won't know 
                    #until we're done
                    if autominimum < y_min:
                        # track the Largest minimum of 
                        # AUTO wards
                        autominimum = y_min
                    
                    # account for the use of the span feature
                    autocount += ward.span 
                    spacers += ward.span
                else:
                    # account for the mimimum size of each 
                    # MAX ward; additional padding will 
                    # happen later
                    spacers += 1
                    maxcount += 1
                    available_space -= y_min
                    
            else:
                
                # this is just the same as the above, but the
                # axes are switched  
                
                if ward.y_setting == AUTO and y_min > offminimum:
                    offminimum = y_min                  
                    
                if ward.x_setting > 0:
                    ward.x_outer = ward.x_setting
                    available_space -= ward.x_setting
                    spacers += 1
                elif ward.x_setting == MIN:
                    ward.x_outer = x_min
                    available_space -= x_min
                    spacers += 1
                elif ward.x_setting == AUTO:
                    
                    x_min = int( x_min / ward.span)
                    
                    if autominimum < x_min:
                        autominimum = x_min
                    autocount += ward.span
                    spacers += ward.span
                else:
                    spacers += 1
                    maxcount += 1
                    available_space -= x_min
                        
        # okay, now we know how much space to give 
        # to each AUTO ward.  
        available_space -= autominimum * autocount
        
        # how big are spaces?
        
        if self.spacing > 0:
            #static spacing size
            space = self.spacing
            available_space -= spacers * self.spacing 
        elif maxcount > 0:
            #setting a ward to max on the axis of orientation
            #causes AUTO and MAX spacing to zero out
            space = 0
        elif self.spacing == AUTO:
            # add an extra space before and after
            space = int( available_space / ( spacers + 2 ) )
            available_space -= spacers * ( space + 2 ) 
        elif self.spacing == MAX:
            space = int( available_space / spacers )
            available_space -= spacers * space 
        else:
            #misconfigured.  No space for you.
            space = 0
            
        if maxcount > 0:
            # divide the remaining space among the MAX wards
            maxpad = int( available_space / maxcount )
            available_space -= maxcount * maxpad
            
        # okay, let's go through them again, and position them.
        
        if available_space != 0:
            #we've got space left over, or we've hit a 
            #negative. we're going to need to offset 
            #our starting point according to alignment.
            
            #note that if there's a negative, parts of wards 
            #will not display-- which part depends on the 
            #alignment.
            
            if self.orientation == VERTICAL:
                
                if self.y_align == MIDDLE:
                    next_position = int( available_space / 2 )
                elif self.y_align == BOTTOM:
                    next_position = available_space
                else:
                    #top aligned
                    next_position = 0
            else:
                #getting deja vu?
                
                if self.x_align == CENTER:
                    next_position = int( available_space / 2 )
                elif self.x_align == RIGHT:
                    next_position = available_space
                else:
                    #left aligned
                    next_position = 0
        else:
            next_position = 0 
        
        if self.spacing == AUTO:
            # we're putting in an extra space here
            next_position += space    
        
        for ward in self.managed_wards:
            if ward.visible is None:
                continue
            
            top, bottom, left, right = ward.set_margins()
            
            x_margin = left + right
            y_margin  = top + bottom 
            
            if self.orientation == VERTICAL:
                #off axis sizing is easy
                if ward.x_setting > 0:
                    ward.x_outer = ward.x_setting
                elif ward.x_setting == MAX:
                    ward.x_outer = self.x_inner
                elif ward.x_setting == AUTO:
                    ward.x_outer = offminimum
                else:
                    ward.x_outer = ward.x_minimum
                    
                ward.x_inner = ward.x_outer - x_margin
                    
                #positioning is also easy  
                    
                if self.x_align == CENTER:
                    x = ( int( self.x_inner / 2 ) 
                        -  int( ward.x_outer / 2 ))
                elif self.x_align == RIGHT:
                    x = self.x_inner - ward.x_outer
                else:
                    x = 0
                
                ward.y_home, ward.x_home = next_position, x
                
                if ward.y_setting > 0:
                    ward.y_outer = ward.y_setting
                elif ward.y_setting == AUTO:
                    # account for extra span and 
                    # absorbed space(s)
                    ward.y_outer = ( ( autominimum * ward.span ) 
                                + ( ( ward.span - 1 ) * space ) )
                elif ward.y_setting == MAX:
                    ward.y_outer = ward.y_minimum + maxpad
                else:
                    ward.y_outer = ward.y_minimum
                    
                next_position += ward.y_outer + space 
            
            else: # the same, but horizontal
                
                if ward.y_setting > 0:
                    ward.y_outer = ward.y_setting
                elif ward.y_setting == MAX:
                    ward.y_outer = self.y_inner
                elif ward.y_setting == AUTO:
                    ward.y_outer = offminimum
                else:
                    ward.y_outer = ward.y_minimum
                    
                ward.y_inner = ward.y_outer - y_margin
                    
                #positioning is also easy  
                    
                if self.y_align == MIDDLE:
                    y = ( int ( self.y_inner / 2 ) 
                            - int( ward.y_outer / 2 ))
                elif self.y_align == BOTTOM:
                    y = self.size - ward.y_outer
                else:
                    y = 0
                    
                ward.y_home, ward.x_home = y, next_position
                
                if ward.x_setting > 0:
                    ward.x_outer = ward.x_setting
                elif ward.x_setting == AUTO:
                    # account for extra span and
                    # absorbed space(s)
                    ward.x_outer = ( ( autominimum * ward.span ) 
                                + ( ( ward.span - 1 ) * space ) )
                elif ward.x_setting == MAX:
                    ward.x_outer = ward.x_minimum + maxpad
                else:
                    ward.x_outer = ward.x_minimum
                
                next_position += ward.x_outer + space
                 
            ward.show()            
    
    def get_minimums(self):
        if self.x_setting > 0 and self.y_setting > 0:
            return self.x_setting, self.y_setting

        top, bottom, left, right = self.set_margins()
        
        if self.spacing > 0:
            spacing = self.spacing
        else:
            spacing = 0
        
        y_contents, x_contents = 0,0
        autosize = 0
        autocount = 0
        count = 0

        for ward in self.managed_wards:
            if ward.visible is None:
                continue
                
            y_ward, x_ward = ward.get_minimums()
                
                
            if self.orientation == VERTICAL:
                if x_ward > x_contents:
                    x_contents = x_ward
                if ward.y_setting == AUTO:
                    count += ward.span
                    if ward.span > 1: y_ward = int( y_ward/2)
                    if y_ward > autosize: autosize = y_ward
                    autocount += 1
                else: 
                    y_contents += y_ward
                    count += 1
            else:
                if y_ward > y_contents:
                    y_contents = y_ward
                if ward.x_setting == AUTO:
                    count += ward.span
                    if ward.span > 1: x_ward = int( x_ward/2)
                    if x_ward > autosize: autosize = x_ward
                    autocount += 1
                else: 
                    x_contents += x_ward
                    count += 1
                    
        if self.orientation == VERTICAL:
            y_contents += ( (autocount*autosize)+
                            ((autocount+count)*spacing) )
        else:
            x_contents += ( (autocount*autosize)+
                            ((autocount+count)*spacing) )
            
        y_contents += top + bottom
        x_contents += left + right
             
        if self.x_setting > 0:
            x = self.x_setting
        elif ( self.x_minimum is not None
                and self.x_minimum > x_contents) :
            x = self.x_minimum
        else:
            x = x_contents

        if self.y_setting > 0:
            y = self.y_setting
        elif ( self.y_minimum is not None 
               and self.y_minimum > y_contents):
            y = self.y_minimum
        else:
            y = y_contents            
    
        return y, x
    
    def show(self):
        Ward.show(self)
        self.manage_contents()
        