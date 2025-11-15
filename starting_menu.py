import pygame, sys
from button import Interactive_button


class StartMenu:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/start_menu_bg.png').convert()
        self.image = pygame.transform.scale(self.image, (900,400))
        self.rect = self.image.get_rect(topleft=(0,0))

        play_button = pygame.image.load("UI/play_button.png").convert_alpha()
        play_button = pygame.transform.scale(play_button,(120,60))

        self.play_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,100),
            font=pygame.font.Font(None,40),
            text='',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            button_surf=play_button,
            hover_button_surf=play_button
        ))

        self.quit_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,200),
            font=pygame.font.Font(None,40),
            text='Quit',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7"
        ))

        self.character_menu = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,300),
            font=pygame.font.Font(None,40),
            text='Characters',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7"
        ))

    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.play_button.draw(self.screen)
        self.play_button.update(self.screen)

        self.quit_button.draw(self.screen)
        self.quit_button.update(self.screen)

        self.character_menu.draw(self.screen)
        self.character_menu.update(self.screen)

        return 'start menu'


    def if_button_pressed(self):
        if self.play_button.sprite.is_pressed():
            return 'main_menu'
        elif self.quit_button.sprite.is_pressed():
            pygame.quit()
            sys.exit()
        elif self.character_menu.sprite.is_pressed():
            return 'characters_menu'
        else:
            return 'start menu'