import pygame, sys
from button import Interactive_button


class StartMenu:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/start_menu_bg.png').convert()
        self.image = pygame.transform.scale(self.image, (1200,600))
        self.rect = self.image.get_rect(topleft=(0,0))

        self.play_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,200),
            font=pygame.font.Font(None,50),
            text='Play',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            size=(150,75)
        ))

        self.quit_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,300),
            font=pygame.font.Font(None,50),
            text='Quit',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            size=(150,75)
        ))

        self.setting_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,400),
            font=pygame.font.Font(None,50),
            text='Settings',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            size=(200,75)
        ))

    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.play_button.draw(self.screen)
        self.play_button.update(self.screen)

        self.quit_button.draw(self.screen)
        self.quit_button.update(self.screen)

        self.setting_button.draw(self.screen)
        self.setting_button.update(self.screen)

        if self.play_button.sprite.is_pressed():
            return 'main_menu'
        elif self.quit_button.sprite.is_pressed():
            pygame.quit()
            sys.exit()
        elif self.setting_button.sprite.is_pressed():
            return 'settings'
        else:
            return 'start menu'