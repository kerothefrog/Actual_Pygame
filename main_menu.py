import pygame
from button import Interactive_button

class MainMenu:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/main_menu_bg.png').convert()
        self.image = pygame.transform.scale(self.image, (900,400))
        self.rect = self.image.get_rect(topleft = (0,0))

        self.back_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(800,100),
            font=pygame.font.Font(None,40),
            text='Back',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7"
        ))
        
        self.play_demo_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(450,200),
            font = pygame.font.Font(None,40),
            text='play demo level',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7"
        ))

    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.back_button.draw(self.screen)
        self.play_demo_button.draw(self.screen)
        self.back_button.update(self.screen)
        self.play_demo_button.update(self.screen)

        return 'main_menu'

    def if_button_pressed(self):
        if self.back_button.sprite.is_pressed():
            return 'start menu'
        if self.play_demo_button.sprite.is_pressed():
            return 'gameplay'
        else:
            return 'main_menu'