import pygame
from button import Interactive_button

class MainMenu:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/main_menu_bg.png').convert()
        self.image = pygame.transform.scale(self.image, (1200,600))
        self.rect = self.image.get_rect(topleft = (0,0))

        self.back_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(1100,100),
            font=pygame.font.Font(None,50),
            text='Back',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            size=(150,75)
        ))

    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.back_button.draw(self.screen)
        self.back_button.update(self.screen)

        if self.back_button.sprite.is_pressed():
            return 'start menu'
        else:
            return 'main_menu'