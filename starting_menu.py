import pygame, sys
from button import Interactive_button


class StartMenu:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/start_menu_bg.png').convert()
        self.image = pygame.transform.scale(self.image, (900,400))
        self.rect = self.image.get_rect(topleft=(0,0))

        play_button = pygame.image.load("UI/play_button.png").convert_alpha()
        play_button = pygame.transform.scale_by(play_button,0.5)

        self.play_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,100),
            font=pygame.font.Font(None,40),
            text='',
            button_surf=play_button,
            hover_button_surf=play_button
        ))

        quit_button = pygame.image.load("UI/quit_button.png").convert_alpha()
        quit_button = pygame.transform.scale_by(quit_button,0.5)

        self.quit_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,200),
            font=pygame.font.Font(None,40),
            text='',
            button_surf=quit_button,
            hover_button_surf=quit_button
        ))

        character_button = pygame.image.load("UI/character_button.png").convert_alpha()
        character_button = pygame.transform.scale_by(character_button,0.5)

        self.character_menu = pygame.sprite.GroupSingle(Interactive_button(
            location=(200,300),
            font=pygame.font.Font(None,40),
            text='',
            button_surf=character_button,
            hover_button_surf=character_button
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