'''
Created on Feb 4, 2024

@author: IterationFive
'''

from wards.codex.keynames import KEYS, PADTRANSLATION

class Keymaster(object):
    '''
    A simple class to handle keyboard input 
    using a curses cursewin object.
    
    Note that cursor location and keyboard echo 
    are NOT managed by this class, as those
    are output functions.
    
    After creating the object, the method
    .configure_window() should be called 
    to set up timeout and keypad behavior, or 
    any time you wish to change those settings.    
    .get_key_by_ID() or .get_key_by_name()
    can then be used to get a keypress, and
    optionally convert the key to lowercase
    or it's non-keypad equivalent.
    
    As this is a wrapper for curses functionality,
    it shares the limitations of curses.  See
    the provided keymap file (codex.keynames)
    for more information about those limitations.    
     
    '''


    def __init__(self, window, keys=KEYS, 
                 padtranslation=PADTRANSLATION, 
                 timeout=-1, activateKeypad=True):
        '''
        Constructor
        
        :param cursewin:
            A curses cursewin object.
        :param keynames:
            A dictionary of names for non-character keys
        :param padtranslation:
            A dictionary to translate the keys on the numeric 
            keypad to their counterparts on the main keyboard.
        :param timeout:
            integer, default -1
            the number of milliseconds to wait for a keypress
            if -1, will wait indefinitely
        :param activateKeypad:
            boolean, default True
            determines whether the numeric keypad is available 
            for input
        '''
        self.cursewin = window
        self.keys = keys
        self.padtranslation = padtranslation
        self.configure_window(timeout, activateKeypad)
    
    def configure_window(self, timeout=-1, activateKeypad=True):
        '''
        
        Applies the settings to the curses cursewin.  Run
        by the constructor, but can be invoked manually 
        to change settings.
        
        :param timeout:
            integer, default -1
            the number of milliseconds to wait for a keypress
            if -1, will wait indefinitely
        :param activateKeypad:
            boolean, default True
            determines whether the numeric keypad is available 
            for input
        '''
        
        if type( timeout ) != int or timeout < 0 :
            timeout = -1
        
        self.cursewin.keypad( activateKeypad )
        self.cursewin.timeout( timeout )
  
    def reversed_kays(self):
        '''
            provides a dictionary for reverse key
            lookup (getting the ID for the name)
        '''
        r = {}
        for key, keyname in self.keys:
            r[keyname] = key
        return r 
        
    def adjust_key(self, key, translateKeypad=True, 
                   forceLowercase=False ):
        '''
        
        Adjusts the key as desired.  See arguments below.
        
        :param key:
            integer, curses key ID
        :param translateKeypad:
            boolean, default True
            If True, the non-character keys on the
            numeric keypad will be converted to
            their non-keypad equivalents
        :param forceLowercase:
            boolean, default False
            If True, uppercase letters will be
            converted to lowercase
        '''
        
        if translateKeypad and key in self.padtranslation:
            key = self.padtranslation[key]
            
        if forceLowercase and key > 64 and key < 91 : #65-90 is A-Z
            key += 32
            
        return key
        
    
    def get_key_by_ID(self, translateKeypad=True, 
                      forceLowercase=False):
        '''
        
        looks for a single keystroke and returns the key id.
        If a timeout is set and reached without a keystroke,
        will return -1
        
        :param translateKeypad:
            boolean, default True
            If True, the non-character keys on the
            numeric keypad will be converted to
            their non-keypad equivalents
        :param force_lowercase:
            boolean, default False
            If True, uppercase letters will be
            converted to lowercase
        '''
        
        key = self.adjust_key( self.cursewin.getch(), 
                               translateKeypad, forceLowercase )
            
        return key
            
    def get_key_by_name(self, translateKeypad=True, 
                        forceLowercase=False):
        '''
        
        looks for a single keystroke and returns the character 
        or name. If a timeout is set and reached without a 
        keystroke, will return 'none' 
        
        :param translateKeypad:
            boolean, default True
            If True, the non-character keys on the
            numeric keypad will be converted to
            their non-keypad equivalents
        :param force_lowercase:
            boolean, default False
            If True, uppercase letters will be
            converted to lowercase
        '''
        key = self.get_key_by_ID(translateKeypad, forceLowercase)
        
        if key == -1:
            return 'none'
        if key == 0:
            # a number of non-character keys
            # return 0 and cannot be distinguished
            # from each other
            return 'any'       
        if key in self.keys:
            return self.keys[key]
        return chr(key) 
    
    