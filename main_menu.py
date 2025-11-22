import pygame
from button import Interactive_button

class MainMenu:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/main_menu_bg.png').convert()
        self.image = pygame.transform.scale(self.image, (900,400))
        self.rect = self.image.get_rect(topleft = (0,0))

        back_button = pygame.image.load("UI/back_button.png").convert_alpha()
        back_button = pygame.transform.scale(back_button,(120,50))


        self.back_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(800,300),
            font=pygame.font.SysFont(None,40),
            text='',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            button_surf=back_button,
            hover_button_surf=back_button
        ))
        

        #flags
        flag_surf = pygame.image.load("UI/flag.png").convert_alpha()
        flag_surf = pygame.transform.scale(flag_surf,(50,50))
        yellow_glow_surf = pygame.image.load("UI/yellow.png").convert_alpha()
        yellow_glow_surf = pygame.transform.scale(yellow_glow_surf,(90,90))
        yellow_glow_surf.blit(flag_surf,(20,20))

        self.level_1_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(80,95),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=flag_surf,
            hover_button_surf=yellow_glow_surf,
            size=(90,90)
        ))

        self.level_2_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(280,220),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=flag_surf,
            hover_button_surf=yellow_glow_surf,
            size=(90,90)
        ))

        self.level_3_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(460,95),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=flag_surf,
            hover_button_surf=yellow_glow_surf,
            size=(90,90)
        ))

        self.level_4_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(540,260),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=flag_surf,
            hover_button_surf=yellow_glow_surf,
            size=(90,90)
        ))

        #boss level
        skele_surf = pygame.image.load("UI/skeleton.png").convert_alpha()
        skele_surf = pygame.transform.scale(skele_surf,(50,50))
        yellow_glow_surf = pygame.image.load("UI/yellow.png").convert_alpha()
        yellow_glow_surf = pygame.transform.scale(yellow_glow_surf,(90,90))
        yellow_glow_surf.blit(skele_surf,(20,20))

        self.boss_level_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(740,140),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=skele_surf,
            hover_button_surf=yellow_glow_surf,
            size=(90,90)
        ))

    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.back_button.draw(self.screen)
        self.back_button.update(self.screen)

        self.level_1_button.draw(self.screen)
        self.level_1_button.update(self.screen)
        self.level_2_button.draw(self.screen)
        self.level_2_button.update(self.screen)
        self.level_3_button.draw(self.screen)
        self.level_3_button.update(self.screen)
        self.level_4_button.draw(self.screen)
        self.level_4_button.update(self.screen)

        self.boss_level_button.draw(self.screen)
        self.boss_level_button.update(self.screen)


        return 'main_menu'

    def if_button_pressed(self):
        if self.back_button.sprite.is_pressed():
            return 'start menu'
        
        if self.level_1_button.sprite.is_pressed():
            return 'gameplay1'
        if self.level_2_button.sprite.is_pressed():
            return 'gameplay2'
        if self.level_3_button.sprite.is_pressed():
            return 'gameplay3'
        if self.level_4_button.sprite.is_pressed():
            return 'gameplay4'
        
        if self.boss_level_button.sprite.is_pressed():
            return 'gameplay5'
        else:
            return 'main_menu'