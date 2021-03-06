import pygame
class GUIFonts(object):
    """description of class"""

    _cached_fonts = {}

    def __init__( self ):
        self._cached_text = {}

    def make_font(self, fonts, size):
        available = pygame.font.get_fonts()
        # get_fonts() returns a list of lowercase spaceless font names 
        choices = map(lambda x:x.lower().replace(' ', ''), fonts)
        for choice in choices:
            if choice in available:
                return pygame.font.SysFont(choice, size)
        return pygame.font.Font(None, size)
    
    
    def get_font(self, font_preferences, size):
        #global _cached_fonts
        key = str(font_preferences) + '|' + str(size)
        font = self._cached_fonts.get(key, None)
        if font == None:
            font = self.make_font(font_preferences, size)
            self._cached_fonts[key] = font
        return font

    
    def create_text(self, text, fonts, size, color):
        key = '|'.join(map(str, (fonts, size, color, text)))
        image = self._cached_text.get(key, None)
        if image == None:
            font = self.get_font(fonts, size)
            image = font.render(text, True, color)
            self._cached_text[key] = image
        return image