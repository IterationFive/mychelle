'''
Created on Feb 14, 2023

@author: IterationFive
'''
import curses
from wards import ( Container, Keymaster, codex,
                    VERTICAL, HORIZONTAL, # @UnusedImport
                    LEFT, RIGHT, # @UnusedImport 
                    TOP, BOTTOM,  # @UnusedImport
                    MIDDLE, CENTER, CENTRE) # @UnusedImport
class Screen(Keymaster, Container):
    '''
    The Screen object encapsulates and manages the cursewin 
    that is the main curses screen.  It also serves as the 
    repository for the dictionaries of colors, glyphs, and 
    attributes, and handles all color management.
    
    Note that color management, while made easier to access,
    still has all the limitations of curses.
    '''
    
    def __init__(self, y_size=None, x_size=None, 
                 x_align=CENTER, y_align=TOP, 
                 orientation = VERTICAL, spacing=0, 
                 border=False, margin=0,  
                 codex=codex):
        '''
        :param y_size:
        :param x_size:
            int or None, default None
            The vertical and horizontal size of the screen;
            if None will use the existing screen size.  Note
            that this will resize the terminal/shell cursewin
            where possible.
        :param x_align:
            LEFT, RIGHT, MIDDLE, CENTER, CENTRE
            How the contents are aligned on the screen
            horizontally.  Note: The last three options
            are identical.
        :param y_align:
            TOP, MIDDLE, BOTTOM, CENTER, CENTRE
            How the contents are aligned on the screen
            vertically.  Note: The last three options
            are identical.
        :param orientation:
            VERTICAL, HORIZONTAL
            How managed content is arranged on the
            screen
        :param spacing:
            int
            The number of lines/characters between
            managed content
        :param border:
            True, False, list, or string
            False        no border
            True         standard lined border
            list/string  will be passed to rectangle as the 
                          'char' parameter            
        :param margin:
            int or tuple
            integer sets a uniform border on all four sides, 
            or use one or more tuples as follows:
            ( left_and_right, top_and_bottom )
            ( (left, right), (top, bottom) )
            ( (left, right), top_and_bottom )
            ( left_and_right, (top, bottom) )
        :param fg:
            string or None
            The default foreground color.  If None, will 
            inherit from container.
        :param bg:
            string or None
            The default background color.  If None, will 
            inherit from container.
        :param codex:
            A package or dictionary containing dictionaries 
            for attributes, colors, and glyphs. 

        '''
        self.cursewin = curses.initscr() # @UndefinedVariable
        self.screen = self
        self.window = self
        self.cursor_off() #establishes cursor_state
        self.noecho() # establishes echo_state
        self.curses = curses  
        
        if x_size is not None and y_size is not None:
            # we've specified both height and width; 
            # change the terminal size
            curses.resize_term(y_size, x_size)#  @UndefinedVariable
        elif y_size is None and x_size is None:
            # don't need to change anything, but we still 
            # need to know what they ARE            
            y_size, x_size = self.cursewin.getmaxyx()
        else:
            # we've specified only ONE dimension. we don't 
            # know why, but we believe in flexibility.
            y_current, x_current = self.cursewin.getmaxyx()
            
            if x_size is None:
                curses.resize_term( y_size, # @UndefinedVariable
                                    x_current ) 
                x_size = x_current
            else:
                curses.resize_term( y_current, # @UndefinedVariable
                                    x_size) 
                y_size = y_current
                
        if curses.can_change_color(): # @UndefinedVariable 
            curses.start_color() # @UndefinedVariable 
            self.available_colors = {}
            self.colors = {
                'black':0, 
                'red':curses.COLOR_RED, # @UndefinedVariable 
                'green':curses.COLOR_GREEN, # @UndefinedVariable 
                'yellow':curses.COLOR_YELLOW, # @UndefinedVariable 
                'blue':curses.COLOR_BLUE, # @UndefinedVariable 
                'magenta':curses.COLOR_MAGENTA,# @UndefinedVariable 
                'cyan':curses.COLOR_CYAN, # @UndefinedVariable 
                'white':curses.COLOR_WHITE }# @UndefinedVariable 
            
            self.import_color_codex(codex)
            
            self.color_pairs = {'count':1, 
                                'black':{'white':0},
                                'special':{} }
            self.colours = self.colors
            self.colour_pairs = self.color_pairs
            self.available_colours = self.available_colors
            
        self.attr = {}
        self.import_attr_codex(codex)
            
        self.glyphs  = {}
        self.import_glyph_codex(codex)
        # we're going to move this into a codex later
        # and create a few different border options.
        self.borderset = [ 
            curses.ACS_VLINE, # @UndefinedVariable 
            curses.ACS_VLINE, # @UndefinedVariable
            curses.ACS_HLINE, # @UndefinedVariable 
            curses.ACS_HLINE, # @UndefinedVariable
            curses.ACS_ULCORNER, # @UndefinedVariable 
            curses.ACS_URCORNER, # @UndefinedVariable
            curses.ACS_LLCORNER, # @UndefinedVariable 
            curses.ACS_LRCORNER ] # @UndefinedVariable 
        
        self.keys= codex.KEYS
        self.padtranslation = codex.PADTRANSLATION
        
        Keymaster.__init__(self, self.cursewin, 
            keys=codex.KEYS, padtranslation=codex.PADTRANSLATION)
                
        # we inherit methods from Window, but don't use its 
        # constructor, instead going back to Container 
        # directly
        
        
        Container.__init__(self, None, y_size, x_size,
                    y_minimum=y_size, x_minimum=x_size, 
                    y_align=y_align, x_align=x_align, 
                    orientation=orientation, spacing=spacing, 
                    border=border, margin=margin)
        
        self.default_local_style('default', 'white,black')

    def cursor_off(self):
        '''
        Turns the cursor off.  Global effect.
        '''
        curses.curs_set(0)# @UndefinedVariable
        self.cursor_state = 0
        
    def cursor_on(self):
        '''
        Turns the cursor on, as the standard blinking _.  
        Global effect.
        '''
        curses.curs_set(1)# @UndefinedVariable
        self.cursor_state = 1
        
    def cursor_block(self):
        '''
        Turns the cursor on, as a block.  Global effect.
        '''
        curses.curs_set(2)# @UndefinedVariable
        self.cursor_state = 2
        
    def cursor_set(self, state):
        '''
        Allows on to set the cursor state directly.
        :param state: int
            0 - off
            1 - blinking _
            2 - block
        '''
        curses.curs_set(state)# @UndefinedVariable
        self.cursor_state = state
            
    def echo(self, state=True):
        '''
        Turns keyboard echo on.
        :param state: boolean, default True
            if this is False, keyboard echo will be 
            turned off.
        '''
        if state:
            curses.echo()# @UndefinedVariable
            self.echo_state = True
        else:
            curses.noecho()# @UndefinedVariable
            self.echo_state = False
            
    def noecho(self):
        '''
        Disables keyboard echo.
        '''
        self.echo(False)
        
    def show(self):
        self.cursewin.touchwin() #@UndefinedVariable
        Container.show(self)
        
    def hide(self):
        self.visible = False
        curses.endwin()  # @UndefinedVariable 
    
    def rgb256_to_1k(self, r,g,b):
        '''
        Converts RGB256 colors to the native RGB1000 
        of curses.
        
        returns r,g,b
        :param r: red 0-255
        :param g: green 0-255
        :param b: blue 0-255
        '''
        if r != 0: r = int(r * 3.92) + 1
        if g != 0: g = int(g * 3.92) + 1
        if b != 0: b = int(b * 3.92) + 1
        return r,g,b
    
    def hex_to_rgb1k(self, hex_string):
        '''
        Converts a hexadecimal color to a the native RGB1000
        of curses.
        
        returns r,g,b
        
        :param hex_string: string.  MUST be a string.
        '''
        if hex_string[0] == '#': hex_string = hex_string[1:]
        if len( hex_string ) == 6:
            r = int( hex_string[0:2], 16 )
            g = int( hex_string[2:4], 16 )
            b = int( hex_string[4:6], 16 )
            return self.rgb256_to_1k(r, g, b)
    
    def set_rgb1k_color(self, name, r, g, b):
        '''
        Configures a color, given in RGB1000, for use by 
        curses. For internal use; the recommended way to
        add a new color is to define it.
        
        :param name:  The name the color will be called by.
        :param r: red 0-1000
        :param g: green 0-1000
        :param b: blue 0-1000
        '''
        if hasattr( self, 'colors'):
            name = name.lower()
            if name in self.colors:
                curses.init_color( # @UndefinedVariable
                    self.colors[name], r, g, b)
            else:
                curses.init_color( # @UndefinedVariable
                    len( self.colors ), r, g, b) 
                self.colors[name] = len( self.colors )
        
    def define_rgb1k_color(self, name, r,g,b):
        '''
        Adds a color, given in RGB1000, to the dictionary 
        of available colors, but does not configure it for 
        use.  This is the recommended way to add colors.   
        
        :param name:  The name the color will be called by.
        :param r: red 0-1000
        :param g: green 0-1000
        :param b: blue 0-1000
        '''
        self.available_colors[name] = (r,g,b)
            
    def define_rgb256_color(self, name, r,g,b):
        '''
        Adds a color, given in RGB256, to the dictionary of 
        available colors, but does not configure it for use.
        This is the recommended way to add RGB256 colors.   
        
        :param name:  The name the color will be called by.
        :param r: red 0-256
        :param g: green 0-256
        :param b: blue 0-256
        '''
        self.define_rgb1k_color(name, *self.rgb256_to_1k(r, g, b))
        
    def define_hex_color(self, name, hex_string ):
        '''
        Adds a color, given as a hexadecimal string, to the 
        dictionary of available colors, but does not 
        configure it for use.  This is the recommended way 
        to add hexadecimal colors.   
        
        :param name:  The name the color will be called by.        
        :param hex_string: string.  MUST be a string
        '''
        self.define_rgb1k_color(name, *self.hex_to_rgb1k(hex_string))
        
    def import_rgb1k_colors(self, color_dict ):
        '''
        Adds a dictionary of RGB1000 colors to the list of 
        available colors.
        
        :param color_dict: a dictionary of RGB1000 colors
        '''
        for color in color_dict:
            self.define_rgb1k_color(color, 
                                    color_dict[color]['r'],
                                    color_dict[color]['g'],
                                    color_dict[color]['b'])
    
    def import_rgb256_colors(self, color_dict ):
        '''
        Adds a dictionary of RGB256 colors to the list of 
        available colors.
        
        :param color_dict: a dictionary of RGB256 colors
        '''
        for color in color_dict:
            self.define_rgb256_color(color, 
                                    color_dict[color]['r'],
                                    color_dict[color]['g'],
                                    color_dict[color]['b']) 
    
    def import_hex_colors(self, color_dict ):
        '''
        Adds a dictionary of hexadecimal  colors to the list 
        of available colors.
        
        :param color_dict: a dictionary of hexadecimal colors
        '''
        for color in color_dict:
                self.define_hex_color(color, color_dict[color]) 
        
    def import_color_codex(self, codex ):
        '''
        checks a module or object for dictionaries of colors 
        in RGB1000, RGB256, and hexadecimal format, then 
        imports those colors into available format 
        
        :param codex:  module/object 
            a module, or any object, with properties that 
            include dictionaries named 'hex_string', 
            'rgb_256', and/or 'rgb_1000'
        '''
        if hasattr(codex, 'hex_string'):
            self.import_hex_colors(codex.hex_string )
        if hasattr(codex, 'rgb_256'):
            self.import_rgb256_colors(codex.rgb_256)
        if hasattr(codex, 'rgb_1000'):
            self.import_rgb1k_colors(codex.rgb_1000)
            
        
    def import_attr_codex(self, codex):
        '''
        imports the list of character cell attributes from a
        module or object.  
        
        :param codex: 
            a module or object with a dictionary called 
            'attributes' containing curses character cell 
            attributes. 
        '''
        if hasattr(codex, 'attributes'):
            attributes = codex.attributes
            for attr in attributes:
                if ( type(attributes[attr]) == str 
                     and attributes[attr][0:2] == 'A_'):
                    self.attr[attr] =  (
                        getattr(curses, attributes[attr]) )
                else:
                    self.attr[attr] = attributes[attr]
        
    def import_glyph_codex(self, codex ):
        '''
        Imports a dictionarty of glyphs from an object or 
        module.
        :param codex:
            an object or module with a dictionary 
            named 'glyphs'
        '''
        if hasattr(codex, 'glyphs'):
            glyphs = codex.glyphs
        
        for glyph in glyphs:
            if ( type(glyphs[glyph]) == str 
                 and glyphs[glyph][0:4] == 'ACS_'):
                self.glyphs[glyph] = getattr(curses, glyphs[glyph])
            else:
                self.glyphs[glyph] = glyphs[glyph]
    
    def load_defined_color(self, name ):
        '''
        Loads a color from the list of available colors into 
        curses.
        
        :param name: string - the color to load
        '''
        if name in self.available_colors:
            self.set_rgb1k_color(name, *self.available_colors[name])
            return True
        else:
            return False

    def color_pair(self, fg, bg=None):
        '''
         Returns the ID of the color pair.
         
         If the color pair has not been defined, 
         will define it.
         
         If one of the colors has not been loaded,
         will load it.
        
        :param fg: string
            The desired text color
        :param bg: string or None
            The background color.  If None, the default 
            background will be used.        
        
        '''
        if bg is None: bg = self.get_bg()
        if (bg not in self.colors 
             and self.load_defined_color( bg ) is False):
            # color is not defined and can't be loaded
            bg = self.get_bg()
        if (fg not in self.colors 
            and self.load_defined_color( fg ) is False):
            # color is not defined and can't be loaded
            fg = self.get_fg()
        if bg not in self.color_pairs:
            self.color_pairs[bg]={}
        if fg not in self.color_pairs[bg]:
            #create new pair
            curses.init_pair(  # @UndefinedVariable
                    self.color_pairs['count'], 
                    self.colors[fg], 
                    self.colors[bg] )
            self.color_pairs[bg][fg] = self.color_pairs['count']
            self.color_pairs['count'] += 1
        return curses.color_pair(  # @UndefinedVariable 
            self.color_pairs[bg][fg] )