import pygame


class Checkbox:
	def __init__(self, screen, x, y, size=40, checked=False):
		self.screen = screen
		self.x = x
		self.y = y
		self.size = size
		self.offset = self.size // 8
		self.checked = checked

		self.checkboxRect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.crossRect = pygame.Rect(self.x + self.offset, self.y + self.offset, self.size - 2 * self.offset, self.size - 2 * self.offset)
	
	def update(self):
		pygame.draw.rect(self.screen, (150, 150, 150), self.checkboxRect)

		if self.checked:
			pygame.draw.rect(self.screen, (75, 75, 75), self.crossRect)

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
