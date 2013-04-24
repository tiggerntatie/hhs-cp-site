# Base class for all actors in the platform game.

import pygame
from pygame.locals import *

class Actor(object):

	# Initialize this actor with dimensions and the list of all actors in the game.
	def __init__(self, x, y, width, height, actor_list):
		self.type = "Actor"
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.actors = actor_list
		self.color = (0,0,0)
		
	# String representation of this actor.
	def __str__(self):
		return "{0} ({1}, {2}) {3}x{4}".format(self.type, self.x, self.y, self.width, self.height)
		
	# Returns true if this actor overlaps with another actor. False otherwise.
	def is_overlapping(self, actor):
		return (self.x < actor.x + actor.width) and (self.x + self.width > actor.x) and (self.y < actor.y + actor.height) and (self.y + self.height > actor.y)

	# Returns a list of all actors that this actor overlaps (optionally, filter by actor type).
	def overlapping_actors(self, actor_type = None):
		overlapping = []
		for actor in self.actors:
			if self.is_overlapping(actor) and (actor_type == None or isinstance(actor, actor_type)):
				overlapping.append(actor)
		return tuple(overlapping)
		
	# Draw the actor to the window, with optional x and y offsets.
	def draw(self, display, x_offset = 0.0, y_offset = 0.0):
		pygame.draw.rect(display, self.color, (int(self.x + x_offset), int(self.y + y_offset), int(self.width), int(self.height)))

	# Code that this actor will perform every frame. Returns whether the actor survived the timestep.
	def timestep(self):
		# Override this function in subclasses to perform actions every timestep.
		return True
		
	# Destroy the actor.
	def destroy(self):
		self.actors.remove(self)