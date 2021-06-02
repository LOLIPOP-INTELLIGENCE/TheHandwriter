import pygame

pygame.init()

img = pygame.image.load('scanner\\scan2.jpg')
dim = list(img.get_size()).copy()

dim[0] /= 2
dim[1] /= 2

dim[0] = int(dim[0])
dim[1] = int(dim[1])

img = pygame.transform.smoothscale(img, dim)
img = pygame.transform.rotate(img, 90)

pygame.image.save(img, 'scanner\\scan2_.jpg')