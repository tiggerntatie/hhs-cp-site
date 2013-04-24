import pygame
from pygame.locals import *


class PygameApp(object):
	"""
	Class that encapsulates a basic pygame application.
	"""
	def __init__(self, screensize = (400,400), fullscreen = False, title = 'PygameApp Window', framerate = 60):
		"""
		Argument to initializer is the desired screen size and/or desire for full screen
		"""
		# save copies of the creation arguments
		self.screensize = screensize
		self.fullscreen = fullscreen
		self.title = title
		self.fps = framerate
		pygame.init()  # every pygame app must start here
		self.clock = pygame.time.Clock() # make a clock object to manage a frame rate
		# open a window different ways, depending on fullscreen setting
		if self.fullscreen:
			# find out what the current display capabilities are
			self.displayinfo = pygame.display.Info()
			self.screensize = (self.displayinfo.current_w, self.displayinfo.current_h)
			self.display = pygame.display.set_mode(self.screensize, FULLSCREEN)
		else:
			self.display = pygame.display.set_mode(self.screensize) # create a window
			pygame.display.set_caption(self.title)
		self.setbackground((0,0,0))

	def setbackground(self, color):
		self.display.fill(color)
		self.background = self.display.copy()

	def run(self):
		"""
		Begin display loop. Optional argument sets the frames per second desired.
		"""
		running = True
		# repeat the display loop
		while running:
			# get events
			for event in pygame.event.get():
				if event.type != QUIT:
					self.handle_event(event)							# let the user event handler deal with it
				else:
					running = False
			# do any regular, periodic processing
			self.elapsedms = self.clock.tick(self.fps)
			self.poll()
			pygame.display.update()
		# fell out of loop
		self.quit()

	def quit(self):
		"""
		Close up and quit. Override this method as desired.
		"""
		pygame.quit()


	def handle_event(self, event):
		"""
		Deal with any events OTHER than QUIT, which is handled elsewhere. This method SHOULD
		be overridden in your own application.
		"""
		pass

	def poll(self):
		pass