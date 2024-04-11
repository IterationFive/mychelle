'''
Created on April 4, 2024
@author: IterationFive

'''
import curses
from wards import ( LEFT, CENTER, RIGHT, TOP,  # @UnusedImport
                    MIDDLE, BOTTOM ) # @UnusedImport

class Ward(object):
    '''
    classdocs 
    '''
    def __init__(self, container, y_size, x_size, 
                 y_home=0, x_home=0, 
                 y_minimum=None, x_minimum=None, 
                 border=False, margin=0, span=1,
                 style=None, borderstyle=None):
        '''
        
        :param container: container object or None
            this object's container. 
            
        :param x_size:  int, MIN, MAX, AUTO
        :param y_size:  int, MIN, MAX, AUTO
            The outer dimensions of the ward.
        
        :param x_home:
        :param y_home:
            The position occupied by the upper left hand 
            corner of the ward, as measured by the container
            it is contained within, accounting for margins 
            and border
        
        :param y_minimum:
        :param x_minimum:
            The absolute minimum dimensions that this ward can
            be sized to.
        
        :param border:  True, False, list, or string
            False        no border
            True         standard lined border
            list/string  will be passed to rectangle as the 
                          'char' parameter
                         
        :param margin: int or tuple
            integer sets a uniform border on all four sides, 
            or use one or more tuples as follows:
            ( left_and_right, top_and_bottom )
            ( (left, right), (top, bottom) )
            ( (left, right), top_and_bottom )
            ( left_and_right, (top, bottom) )
            
        :param span: int, default 1
        
            If this ward is configured to be size AUTO on the
            axis of the container's layout, increasing this 
            number will cause this ward to take up the space 
            that would ordinarily be used by this number of 
            auto-sized wards, including the spaces (if any) 
            between.
        '''
        if container is not None:
            self.screen = container.screen
            self.window = container.window
            
        self.container = container
        self.y_home, self.x_home = y_home, x_home
        self.y_setting, self.x_setting = y_size, x_size
        self.y_outer, self.x_outer = y_size, x_size
        self.border = border
        self.margin = margin 
        self.span = span
        if y_size > 0: 
            self.y_minimum = y_size
        else:
            self.y_minimum = y_minimum 
        if x_size > 0: 
            self.x_minimum = x_size
        else:
            self.x_minimum = x_minimum
        
        self.visible = False   
        
        self.styles = {}
        
        if style is not None:
            self.name_style('default', style)
        if borderstyle is not None:
            self.name_style('border', borderstyle)
        
        self.set_margins()
        self.setup()
        
    def setup(self):
        ''' 
        Method for developing child classes that is run once 
        at the end of the constructor.  This is where you 
        want to define styles, setup wards stored within 
        this one, and establish any environment variables.
        
        Output functions will either not work or throw 
        exceptions during setup(). This is intentional; 
        the output environment is not fully initialized until 
        .show() is run.  While starting content can (and 
        should!) be provided here, it should not actually
        be displayed until .update().     
        '''
        pass
    
    def update(self):
        '''
        Another structural method for use in child classes.  
        Is run each time a cursewin is shown after being built, 
        hidden, resized, or moved.  
        '''
        pass
    
    def nap(self, ms):
        '''
        Wrapper for curses.napms().  Pauses processing 
        for the specified number of milliseconds
        :param ms: int
            The specified number of milliseconds.
        '''
        curses.napms(ms)# @UndefinedVariable
            
    def refresh(self):
        '''
        refreshes the screen, assuming self.visible is True
        '''
        if self.is_visible() : 
            if self.container is None:
                self.cursewin.refresh()
            else:
                self.container.refresh()
                
    def move_cursor(self, y, x, offset=True):
        '''
        Places the cursor at the specified position within 
        the ward.
        
        :param x: int
        :param y: int
            The specified position.
        :param offset: boolean
            If True, the coordinates have been adjusted to 
            account  for margins and borders.
        '''
        if offset: y,x = self.remove_offset(y, x)
        if self.container is None:
            self.cursewin.move(y, x)
        else:
            self.container.move_cursor(y, x)
        
    def get_attr(self,name):
        '''
        Returns the numerical value of a curses character 
        cell attribute.
        
        :param name: 
           The configured name for a character cell attribute
        '''
        if name in self.screen.attr:
            return self.screen.attr[name]
        else:
            return 0    
   
    def find_style(self, name=None):
        ''' 
        Checks to see if a style definition exists either 
        locally or by inheritance.  
        If the style does not exist, will look for a custom 
        color pair.
        If neither exists, returns False, otherwise returns 
        a style dictionary.
        '''
        if name is None:
            name = 'default'
        
        if name in self.styles: 
            return self.styles[name]
        # not local, check with container
        if self.container is not None: 
            return self.container.find_style(name)
        #we don't have a container, so we're a window
        #or a screen
        if self != self.screen: 
            return self.screen.find_style(name)
        # if we're here, it's the screen.
        return False
            
            
    def make_style(self, options):
        '''
        Converts a list of strings into a style dictionary.
        
        :param options: string or list 
            a style definition
            
        '''
        if type(options) != list:
            options = options.split(",")
        option = options.pop(0).lower().strip()
        
        style = { 'fg':None, 'bg':None, 'attr':[]}
        # first position is either---
        if option is None: 
            #-- a choice of nothing
            pass 
        check = self.find_style(option)
        if check is not False:
            # -- a named style
            style = {'fg':check['fg'],'bg':check['bg'],'attr':check['attr'].copy()}
        elif (option in self.screen.colors 
              or self.screen.load_defined_color(option) is True):
            # -- a foreground color
            style['fg'] = option
            if len( options ) > 0:
                option = options[0].lower().strip()
                if ( option in self.screen.colors 
                     or self.screen.load_defined_color(option) is True ):
                    style['bg'] = option
                    options.pop(0)
        else:
            # none of the above.
            # put it in the list of attributes
            options.append( option ) 
        for option in options:
            option = option.lower().strip()
            if ( option in self.screen.attr and 
                 option not in style['attr'] ):
                style['attr'].append( option )
        return style
    
    def name_style(self, name, options ):
        '''
        Stores a style definition for easier reference.
        
        :param name:  string
            the name of the style
        :param options: string or list 
            a style definition
        
        '''
        self.styles[name] = self.make_style( options )
    
    def default_local_style(self, name, options ):
        '''
        works like name style, but will not 
        overwrite an existing local style.  Allows 
        for setting default styles in a child 
        constructor after running the parent 
        constructor.
        
        
        :param name:  string
            the name of the style
        :param options: string or list 
            a style definition
        
        '''
        if name not in self.styles:
            self.styles[name] = self.make_style( options )
        
    def style(self, options):
        '''
        This function produces the curses numerical 
        configuration corresponding to style name, color 
        pair, or definition.
        
        :param options: string
            The name of the style or color pair, or the first
            option in a style definition.
        '''
        if type( options ) == int:
            #passthrough
            return options
        if options is None:
            options = 'default'
        options = options.split(",")
        style = self.find_style(options[0].lower().strip())
        if style is True:
            options.pop(0)
        else:
            style = self.make_style(options)
        if style['fg'] is None:
            style['fg'] = 'white'
        if style['bg'] is None:
            style['bg'] = 'black'
                        
        result = self.screen.color_pair(style['fg'],style['bg'])
        
        for at in style['attr']:
            at = at.lower().strip()
            result = result | self.get_attr(at)

        return result
        
    def calculate_margins(self, border, margin ):
        '''
        Uses the border and margin properties to determine 
        the size of the interior of the ward. Stores offsets 
        for later use.
        
        Returns size of margins, including borders, for each 
        side as top, bottom, left, right
        '''
        if border != False:
            bordersize = 1
        else:
            bordersize = 0
            
        if type( margin ) == int: 
            # margin is single number for all sides
            left = right = top = bottom = bordersize + margin
        elif type( margin ) == tuple:
            #margin given as y, x
            if type( margin[0] ) == tuple : 
                # y given as top,bottom
                top = margin[0][0] + bordersize
                bottom = margin[0][1] + bordersize 
            elif type( margin[0] ) == int: 
                # y given for both top & bottom
                top = bottom = margin[0] + bordersize
            
            if type( margin[1] ) == tuple :
                # x given as left, right
                left = margin[1][0] + bordersize
                right = margin[1][1] + bordersize 
            elif type( margin[1] ) == int:
                # x given for both left & right
                left = right = margin[1] + bordersize
        else: 
            # dunno, but no margin
            left = right = top = bottom = bordersize 
               
        return top, bottom, left, right
        
    def set_margins(self):
        '''
        Uses the border and margin properties to determine 
        the size of the interior of the ward. Stores offsets 
        for later use.
        
        Returns size of margins, including borders, for each 
        side as top, bottom, left, right
        '''
        top, bottom, left, right = self.calculate_margins(
            self.border, self.margin)
        
        self.y_offset, self.x_offset = top, left
        
        self.y_inner = self.y_outer - (top+bottom)
        self.x_inner = self.x_outer - (left+right)
               
        return top, bottom, left, right
        
    def remove_offset(self,y,x):
        '''
        Takes a set of interior coordinates (the area inside 
        the margins) and returns the coordinates of that 
        position in the total available area of the ward.
        
        :param y: int: 
            the interior y coordinate
        :param x: int: 
            the interior x coordinate
        '''
        return self.y_offset + y, self.x_offset + x
    
    def container_coords(self,y,x,offset=True): 
        '''
        Takes a set of coordinates and returns the 
        coordinates of that position in the interior area 
        (inside the margins) of the container that contains 
        it.  If this ward is not contained within a 
        container, it will return the coordinates unaltered.
        
        :param y: int: 
            the y coordinate
        :param x: int: 
            the x coordinate
        :param offset: boolean: defaults True
            denotes whether the coordinates given 
            have been offset to account for border 
            and margins.
        '''
        if self.container is None:
            return y,x
        
        if offset: y,x = self.remove_offset(y, x)
        x += self.x_home 
        y += self.y_home 
        return y, x
    
    def window_coords(self,y,x,offset=True): 
        '''
        Takes a set of coordinates and returns the 
        coordinates of that position in the interior area 
        (inside the margins) of the cursewin that contains 
        it.  If this ward is not contained within a 
        cursewin, it will return the coordinates unaltered.
        
        :param y: int: 
            the y coordinate
        :param x: int: 
            the x coordinate
        :param offset: boolean: defaults True
            denotes whether the coordinates given 
            have been offset to account for border 
            and margins.
        '''
        if self.container is None:
            return y,x
        
        if offset: y,x = self.remove_offset(y, x)
        x += self.x_home 
        y += self.y_home 
        return self.container.window_coords(y, x)
    
    def point_in_bounds(self, y, x, offset=True):
        '''
        returns boolean indicating whether the point 
        specified is within the allowed area of the ward.
        
        :param y: int: 
            the y coordinate
        :param x: int: 
            the x coordinate
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will return
            whether the point is within the total area 
            of the ward, rather than the interior area.
        '''
        if offset:
            y_max, x_max = self.y_inner, self.x_inner
        else:
            y_max, x_max = self.y_outer, self.x_outer
        return ( y >= 0 and x >= 0 and y < y_max and x < x_max)
    
    def length_in_bounds(self, y, x, length, offset=True):
        '''
        Determines whether any part of a length is within the 
        allowed area. Returns values for left and right 
        as follows:
        
            False
                no part of this string will fit.
            True
                this string fits completely
            int
                indicates the number of characters on the 
                given side that need to be removed. 
        
        :param y: int: 
            the starting y coordinate
        :param x: int: 
            the starting x coordinate
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will judge 
            whether the length is within the total area 
            of the ward, rather than the interior area.
        '''
            
        if offset: 
            y_limit, x_limit = self.y_inner, self.x_inner
        else: 
            y_limit, x_limit = self.y_outer, self.x_outer
        
        if x >= x_limit or ( x < 0 and 0 - x > length):
            #entire length is out of x bounds
            return False, False
        if y < 0 or y >= y_limit:
            #y is out of bounds
            return False, False
        
        if x < 0: 
            left = 0 - x
        else:
            left = True
            
        if x + length > x_limit:
            right = ( x + length ) - x_limit
        else:
            right = True
            
        return left, right
    
    def glyph(self, glyph):
        '''
        Returns the curses numerical indicator of a special
        character defined as a glyph
        :param glyph: string:
            the named of the defined glyph
        '''
        if glyph in self.screen.glyphs:
            return self.screen.glyphs[glyph]
                
    def add_string(self, y, x, string, 
                   style=None, offset=True):  
        '''
        Outputs a single string of text to the ward's 
        available area. If the ward is not currently visible,
        will do nothing. If the string will not fit in the 
        available area, it will be truncated or ignored.
        
        If the value provided for string is not a str type, 
        it will be converted.  Additionally, if the string 
        contains \n, it will be truncated from that point.
        
        :param y: int: 
            the starting y coordinate
        :param x:
            the starting x coordinate
        :param string: str
            the string to be displayed.
        :param style:
            A style name or definition
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will judge 
            whether the string is within The total area of 
            the ward, rather than the interior area
        '''
        if not self.is_visible():  return False
        string = str( string ).split("\n")[0] # no line breaks
        left, right = self.length_in_bounds(y, x, 
                                            len(string), offset)
        if left is False: return False
        if left is not True:
            string = string[left:]
            x = 0
        if right is not True:
            string = string[:0-right]
        
        # at this point we have a safe string & coords
        
        style = self.style(style)
        y,x = self.container_coords(y, x, offset)
        if self.container is not None:
            return self.container.add_string(y, x, string,style)
        if offset: y,x = self.remove_offset(y, x)
        if ( x + len( string ) == self.x_outer 
             and y == self.y_outer - 1):
            self.cursewin.addstr(y, x, string[0:-1],style)
            self.cursewin.insch( y, self.x_outer - 1, 
                                 string[-1],style)
        else:
            self.cursewin.addstr(y, x, string,style)
        return True   
    
    def add_char(self, y, x, char, style=None, offset=True):
        '''
        Outputs a single character to the screen.
        
        :param y: int: 
            the starting y coordinate
        :param x:
            the starting x coordinate
        :param char: int or string
            int denotes a character code accepted by curses.
            string denotes the label of a glyph, or a single 
            character.
        :param style:
            A style name or definition
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset
            to account for border and margins.  Note that if 
            this is False, this method will judge whether the
            character is within the total area of the ward, 
            rather than the interior area.
        '''
        if  ( type( char ) == str 
                and len( char ) > 1
                and char in self.screen.glyphs ) :
            char = self.screen.glyphs[char]
        style = self.style(style)
        if (not self.is_visible() 
            or not self.point_in_bounds(y, x, offset)):
            return False
        y,x = self.container_coords(y, x, offset)
        if self.container is not None:
            return self.container.add_char(y,x, char, style)
        if offset: y,x = self.remove_offset(y, x)
        if x == self.x_outer - 1 and y == self.y_outer -1:
            self.cursewin.insch(y, x, char, style) 
        else:
            self.cursewin.addch(y, x, char, style)
        return True  
    
    def insert_char(self, y, x, char, 
                    style=None, offset=True):
        '''
        Outputs a single character to the screen, and 
        offsets the characters following it one space 
        to the right.
        
        :param y: int: 
            the starting y coordinate
        :param x:
            the starting x coordinate
        :param char: int or string
            int denotes a character code accepted by curses.
            string denotes the label of a glyph, or a single
            character.
        :param style:
            A style name or definition
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will judge 
            whether the character is within the total area of 
            the ward, rather than the interior area.
        '''
        if ( not self.is_visible() 
             or not self.point_in_bounds(y, x, offset)):
            return False
        y,x = self.container_coords(y, x, offset)
        style = self.style(style)
        if self.container is not None:
            return self.container.insert_char(x,y,char, style)
        if offset: y,x = self.remove_offset(y, x)
        self.cursewin.insch(y, x, char, style) 
        return True       
    
    def hline(self, y, x, length, char=None, 
              style=None, offset=True):
        '''
        Draws a horizontal line within the allowable area.  
        If the
        line exceeds the available bounds, it will be truncated.
        
        :param y: int: 
            the starting y coordinate
        :param x:
            the starting x coordinate
        :param char: int or string
            int denotes a character code accepted by curses.
            string denotes the label of a glyph, or a single 
            character.
        :param style:
            A style name or definition
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will judge 
            whether the character is within the total area of 
            the ward, rather than the interior area.
        
        '''
        if not self.is_visible(): return False 
        if char is None: 
            char = curses.ACS_HLINE #@UndefinedVariable
        if type( char ) == str and char in self.screen.glyphs:
            char = self.screen.glyphs[char]
            style = self.style(style)
            
        left, right = self.length_in_bounds(y,x,length,offset)
        
        if left is False: return None
        if left is not True:
            length -= left
            x = 0
        if right is not True:
            length -= right
            
            
        if self.container is not None:
            y,x = self.container_coords(y,x, offset)
            self.container.hline(y, x, length, char, style)
        else:
            if offset: y,x = self.remove_offset(y, x)
            self.cursewin.hline(y, x, char, length, style)
            
    def vline(self, y, x, length, char=None, 
              style=None, offset=True):
        '''
        Draws a vertical line within the allowable area.  
        If the line exceeds the available bounds, it will be 
        truncated.
        
        :param y: int: 
            the starting y coordinate
        :param x:
            the starting x coordinate
        :param length: int
            the length of the line
        :param char: int or string
            int denotes a character code accepted by curses.
            string denotes the label of a glyph, or a single
             character.
        :param style:
            A style name or definition
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will judge 
            whether the character is within the total area of 
            the ward, rather than the interior area.
        '''
        
        
        if not self.is_visible(): return False
        if char is None: 
            char = curses.ACS_HLINE #@UndefinedVariable
        if ( type( char ) == str 
             and char in self.glyphs):
            char = self.glyphs[char]
        style = self.style(style)

        y_limit, x_limit = self.y_outer, self.x_outer
            
        if x >= x_limit or x < 0 or y >= y_limit:
            return False 
        if y + length >= y_limit:
            length -= ( y + length ) - y_limit

        if self.container is not None:
            y,x = self.container_coords(y, x, offset)
            self.container.vline(y, x, length, char, style)
        else:
            if offset:  y, x = self.remove_offset(y, x)
            self.cursewin.vline(y, x, char, length, style)
            
          
    def rectangle(self, y,x, y_length, x_length,
                  chars=None, style=None, offset=True):
        '''
            Draws a rectangle.
        
        :param x:
            the starting x coordinate
        :param y: int: 
            the starting y coordinate
        :param x_length: int
            the length of the rectangle
        :param y_length: int
            the height of the rectangle
        :param chars: True, list or string
             True:  Standard lined border
             If string or list contains three characters, 
             the first character will be used for the top 
             and bottom, the second character will be used 
             for the sides, and the third will be used for 
             the corners.  If eight characters, they will be 
             used in order of top, bottom, left, right,
             upper left, upper right, lower left, lower right.
        :param style:
            A style name or definition
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will judge 
            whether the line is within the total area of 
            the ward, rather than the interior area.
        '''
        
        if not self.is_visible(): return False 
        if chars is None:
            chars = self.screen.borderset     
        if type( chars ) == str and len( chars ) == 1:
            # one character for all positions
            chars = chars*8
        if type( chars ) in [list,str] and len( chars ) == 3:
            #top/bottom, left/right, corners
            chars = chars[0] * 2 + chars[1] * 2 + chars[2] * 4
        if type( chars ) not in [list,str] or len( chars ) != 8:
            return False
        # we have a valid list or string and can proceed        
        if type( chars ) == list:
            for i in range(0,len(chars)):
                if type( chars[i] ) == str and len( chars[i]) > 1:
                    if chars[i] in self.screen.glyphs:
                        chars[i] = self.screen.glyphs[chars[i]]
                    else:
                        chars[i] = chars[i][0]
        x_end = x_length + x -1
        y_end = y_length + y -1
        x_length -= 2
        y_length -= 2
        style = self.style(style)
        
        self.vline(y + 1, x, y_length, chars[0], style, offset)
        self.vline( y + 1, x_end,y_length, chars[1], style, offset)
        self.hline( y, x + 1, x_length, chars[2], style, offset)
        self.hline( y_end, x + 1, x_length, chars[3], style, offset) 
        self.add_char(y, x, chars[4], style, offset)
        self.add_char(y, x_end, chars[5], style, offset)
        self.add_char(y_end, x, chars[6], style, offset)
        self.add_char(y_end, x_end, chars[7], style, offset)
        
    def draw_border(self):
        '''
        If the border property is not False, invokes 
        .rectangle() to draw a border around the boundaries 
        of the cursewin.
        '''
        if self.border is True:
            chars = self.screen.borderset
        else:
            chars = self.border
        if self.border is not False:
            if ( type( self.border ) == str 
                 and self.border in self.screen.glyphs ):
                char = self.glyph(self.border)
                chars = [char,char,char,char,char,char,char,char]
            self.rectangle( 0, 0, self.y_outer, self.x_outer, 
                            chars, style='border', offset=False)
            
    def wipe(self, y, x, height, width, char=' ', 
             style=None, offset=True):
        '''
        Replaces a specified area with a single character 
        in a specified style. 
        
        :param y: int: 
            the starting y coordinate
        :param x:
            the starting x coordinate
        :param height: int
            the height of the area
        :param width: int
            the width of the area
        :param chars: string
            Either a single character or a glyph label
        :param style:
            A style name or definition
        :param offset: boolean: defaults True
            denotes whether the coordinates given have been 
            offset to account for border and margins.  Note 
            that if this is False, this method will judge 
            whether the area is within the total area of 
            the ward, rather than the interior area.
        '''
        if char in self.screen.glyphs:
            char = self.glyphs( char )
        
        for yy in range(y,y+height):
            for xx in range (x,x+width):
                self.add_char(yy, xx, char, style, offset)

    def clear(self, char=' '):
        '''
        Replaces the entire area of the ward with a blank 
        space.
        '''
        self.wipe(0,0, self.y_outer, 
                  self.x_outer, char, offset=False)
        self.draw_border()
        
    def get_minimums(self):
        '''
        Returns the configured minimum size of the ward.  
        If the ward is not auto-sized, this is set to the 
        size of the ward.
        '''
        return self.y_minimum, self.x_minimum
        
    def is_visible(self):
        '''
        Returns False if the ward is not set to visible, or
        is contained within a container that is not set to 
        visible. Returns True otherwise.
        '''
        if self.visible != True:
            return False
        if self.container is not None:
            # this ward is set to visible, but 
            # is it in a container that is not?
            return self.container.is_visible() 
        else:
            # this is a window or screen
            # so we can take its word for it
            return True     
        
    def show(self):
        '''
        Sets the state of the ward to visible, clears the 
        screen, draws the border, and updates the contents.
        '''
        if self.visible == None:
            # will not auto-enable if disabled
            return 
        self.visible = True
        self.clear()
        
        if hasattr(self, 'adjust_contents'):
            self.adjust_contents()
        
        self.update()
        
    def hide(self, disable=False):
        '''
        Sets the state of the ward to invisible and
        erases the area on the screen.
        '''
        if disable:
            self.visible = None
        else:
            self.visible = False
            
        self.wipe(0,0, self.y_outer, self.x_outer, ' ', offset=False)
        self.refresh()
        