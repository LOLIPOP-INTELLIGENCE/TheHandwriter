import pygame

# function to always make sure that the resolution of the final image is less than 1800 px
def preprocess( _surf ):

    _surf           = pygame.image.load( _surf )
    width, height   = list( _surf.get_size() ).copy()

    if width < height:
        _surf           = pygame.transform.rotate( _surf, 90 )
        width, height   = height, width

    new_width       = 1600
    new_height      = round( ( height * new_width ) / width )

    _surf = pygame.transform.smoothscale( _surf, (new_width, new_height) )
    pygame.image.save( _surf, 'scanner\\scan_final_.jpg' )
