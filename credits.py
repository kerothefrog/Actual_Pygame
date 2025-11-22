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
            location=(100,50),
            font=pygame.font.Font(None,30),
            text='',
            button_surf=back_button,
            hover_button_surf=back_button
        ))

        self.font = pygame.font.Font("assets/NotoSansTC-VariableFont_wght.ttf",25)
        self.texts = [
            "Made by 黃紹洋, 鄭佑明, 郭峻愷, 葉丙祥",
            "artist: 郭峻愷",
            "Huge thanks to Angus beef for", 
            "help on illustrations"
        ]
        self.texts_location = (300,50)


    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.back_button.draw(self.screen)
        self.back_button.update(self.screen)

        for i in range(len(self.texts)):
            temp_surf = self.font.render(self.texts[i],False,"#616161FF")
            temp_rect = temp_surf.get_rect(topleft=(self.texts_location[0],self.texts_location[1]+i*30))
            self.screen.blit(temp_surf, temp_rect)

        return 'credits'

    def if_button_pressed(self):
        if self.back_button.sprite.is_pressed():
            return 'characters_menu'
        else:
            return 'credits'