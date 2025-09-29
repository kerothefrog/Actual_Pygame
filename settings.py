import pygame, sys
from button import Interactive_button

class Settings:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/setting_menu_bg.jpg').convert()
        self.image = pygame.transform.scale(self.image, (1200,600))
        self.rect = self.image.get_rect(topleft=(0,0))

        self.back_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(100,100),
            font=pygame.font.Font(None,50),
            text='Back',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
        ))

        self.credits_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(1000,500),
            font=pygame.font.Font(None,50),
            text='Credits',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
        ))

    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.back_button.draw(self.screen)
        self.back_button.update(self.screen)

        self.credits_button.draw(self.screen)
        self.credits_button.update(self.screen)

        return 'settings'


    def if_button_pressed(self):
        if self.back_button.sprite.is_pressed():
            return 'start menu'
        if self.credits_button.sprite.is_pressed():
            return 'credits'
        else:
            return 'settings'