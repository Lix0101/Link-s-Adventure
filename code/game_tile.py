import pygame 
from game_set import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		y_offset=HIT_OFFSET[sprite_type]
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos)

		if sprite_type == 'boss':
			self.hitbox = self.rect.inflate(y_offset,y_offset)
		else:
			self.hitbox = self.rect.inflate(0,y_offset)