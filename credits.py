import pygame
from button import Interactive_button

class Credits:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/credits_bg.png').convert()
        self.image = pygame.transform.scale(self.image, (900,400))
        self.rect = self.image.get_rect(topleft=(0,0))

        back_button = pygame.image.load("UI/back_button.png").convert_alpha()
        back_button = pygame.transform.scale(back_button,(120,50))


        self.back_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(100,100),
            font=pygame.font.Font(None,40),
            text='',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            button_surf=back_button,
            hover_button_surf=back_button
        ))

    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.back_button.draw(self.screen)
        self.back_button.update(self.screen)

        return 'credits'

    def if_button_pressed(self):
        if self.back_button.sprite.is_pressed():
            return 'characters_menu'
        else:
            return 'credits'