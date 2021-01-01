import pygame
from helpers import load_image


class Checkbox:
	def __init__(self, screen, x, y, size=40, checked=False, box_color="#c2c1bf", tick_color="#1BD40E"):
		self.screen = screen
		self.x = x
		self.y = y
		self.size = size
		self.checked = checked
		self.box_color = box_color
		self.tick_color = tick_color

		self.checkboxRect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.tick = pygame.Surface((self.size, self.size))

	def update(self):
		pygame.draw.rect(self.screen, (150, 150, 150), self.checkboxRect)

		if self.checked:
			self.tick.fill(pygame.Color(self.box_color))
			pygame.draw.polygon(self.tick, pygame.Color(self.tick_color), (
				(self.size * 0.3, self.size),
				(0, self.size * 0.6),
				(self.size * 0.2, self.size * 0.5),
				(self.size * 0.3, self.size * 0.7),
				(self.size * 0.8, 0),
				(self.size, self.size * 0.15)
			))
			self.screen.blit(self.tick, (self.x, self.y))

	def onCheckbox(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				x, y = pygame.mouse.get_pos()

				if self.checkboxRect.collidepoint((x, y)):
					self.changeState()

	def changeState(self):
		if self.isChecked():
			self.uncheck()
		else:
			self.check()

	def isChecked(self):
		return self.checked

	def check(self):
		self.checked = True

	def uncheck(self):
		self.checked = False
