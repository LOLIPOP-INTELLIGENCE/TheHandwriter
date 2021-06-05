import pygame

# function to always make sure that the resolution of the final image is less than 1800 px
def preprocess( _surf ):

    ceil = lambda _a, _b: ( _a + _b - 1 ) // _b
    flor = lambda _a, _b : _a // _b

    _surf = pygame.image.load( _surf )
    width, height = list( _surf.get_size() ).copy()

    if width < height:
        _surf           = pygame.transform.rotate( _surf, 90 )
        width, height   = height, width

    scale       = ceil( width, 1800 )
    new_width   = int( width // scale )
    new_height  = int( height // scale )

    _surf = pygame.transform.smoothscale( _surf, (new_width, new_height) )
    pygame.image.save( _surf, 'scanner\\scan_final_.jpg' )

pygame.init()

preprocess( 'scanner\\scan2.jpg' )
