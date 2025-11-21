import pygame, sys
from button import Interactive_button

class Characters_info(Interactive_button):
    def __init__(self,
                location,
                font,
                text='',
                button_surf=None, 
                hover_button_surf=None, 
                text_color="#FFFFFF", 
                color="#0091FF", 
                hover_color="#03FECC", 
                size=(0,0),
                info_text:list[str]=[],
                ):
        super().__init__(location, font, text, button_surf, hover_button_surf, text_color, color, hover_color, size)

        self.info_text = info_text
        self.info_text_location = (600,240)

    def update(self, screen):
        super().update(screen)

        if super().is_hovered():
            font = pygame.font.SysFont('impact',22)
            for i in range(len(self.info_text)):
                temp_surf = font.render(self.info_text[i],False,"#616161FF")
                temp_rect = temp_surf.get_rect(topleft=(self.info_text_location[0],self.info_text_location[1]+i*20))
                screen.blit(temp_surf, temp_rect)





class Characters_menu:
    def __init__(self, screen:pygame.Surface):
        self.screen = screen
        self.image = pygame.image.load('assets/character_menu.png').convert()
        self.image = pygame.transform.scale(self.image, (900,400))
        self.rect = self.image.get_rect(topleft=(0,0))

        back_button = pygame.image.load("UI/back_button.png").convert_alpha()
        back_button = pygame.transform.scale(back_button,(120,50))

        self.back_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(80,50),
            font=pygame.font.Font(None,40),
            text='',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            button_surf=back_button,
            hover_button_surf=back_button
        ))

        credits_button = pygame.image.load("UI/credit_button.png").convert_alpha()
        credits_button = pygame.transform.scale(credits_button,(120,60))

        self.credits_button = pygame.sprite.GroupSingle(Interactive_button(
            location=(830,50),
            font=pygame.font.Font(None,40),
            text='',
            text_color="#FFFFFF",
            color="#5D5D5D",
            hover_color="#A7A7A7",
            button_surf=credits_button,
            hover_button_surf=credits_button
        ))

        #characters
        self.characters = pygame.sprite.Group()

        yellow_glow_surf = pygame.image.load("UI/yellow2.png").convert_alpha()
        self.yellow_glow_surf = pygame.transform.scale(yellow_glow_surf,(140,140))
        arrow_surf = pygame.image.load("UI/arrow.png").convert_alpha()
        self.arrow_surf = pygame.transform.scale(arrow_surf,(28,40))

        temp = self.set_character_surf("birdani/kiwi_bird_1.png")
        self.characters.add(Characters_info(
            location=(100,300),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=temp[0],
            hover_button_surf=temp[1],
            info_text=["attack=5", "attack speed=0.8", "hp=40", "move speed=2.0", "attack range=40"]
        ))

        temp = self.set_character_surf("birdani/kiwi_bird_attack_1.png")
        self.characters.add(Characters_info(
            location=(270,300),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=temp[0],
            hover_button_surf=temp[1],
            info_text=["attack=8", "attack speed=0.5", "hp=25", "move speed=1.0", "attack range=150"]
        ))

        temp = self.set_character_surf("birdani/kiwi_boss_1.png")
        self.characters.add(Characters_info(
            location=(440,300),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=temp[0],
            hover_button_surf=temp[1],
            info_text=["attack=30", "attack speed=0.5", "hp=150", "move speed=1.0", "attack range=40"]
        ))

        temp = self.set_character_surf("mushrooms/mushroom_walk_1.png")
        self.characters.add(Characters_info(
            location=(300,100),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=temp[0],
            hover_button_surf=temp[1],
            info_text=["hp=10", "score when killed=20", "money when killed=1"]
        ))

        temp = self.set_character_surf("mushrooms/mushroom2_walk_1.png")
        self.characters.add(Characters_info(
            location=(440,100),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=temp[0],
            hover_button_surf=temp[1],
            info_text=["hp=25", "score when killed=50", "money when killed=3"]
        ))

        temp = self.set_character_surf("mushrooms/mushroom3_walk_1.png")
        self.characters.add(Characters_info(
            location=(580,100),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=temp[0],
            hover_button_surf=temp[1],
            info_text=["hp=40", "score when killed=80", "money when killed=3"]
        ))

        temp = self.set_character_surf("mushrooms/mushroom4_walk_1.png")
        self.characters.add(Characters_info(
            location=(720,100),
            font=pygame.font.SysFont(None,40),
            text="",
            button_surf=temp[0],
            hover_button_surf=temp[1],
            info_text=["hp=15", "score when killed=30", "money when killed=1"]
        ))


    def set_character_surf(self, path:str):
        hover_surf=self.yellow_glow_surf.copy()
        blah_surf = pygame.image.load(path).convert_alpha()
        blah_surf = pygame.transform.scale(blah_surf,(90,90))
        hover_surf.blit(blah_surf,(25,25))
        hover_surf.blit(self.arrow_surf,(56,0))
        return [blah_surf, hover_surf]


    def draw(self):
        self.screen.blit(self.image, self.rect)

        self.back_button.draw(self.screen)
        self.back_button.update(self.screen)

        self.credits_button.draw(self.screen)
        self.credits_button.update(self.screen)

        self.characters.draw(self.screen)
        self.characters.update(self.screen)

        return 'characters_menu'


    def if_button_pressed(self):
        if self.back_button.sprite.is_pressed():
            return 'start menu'
        if self.credits_button.sprite.is_pressed():
            return 'credits'
        else:
            return 'characters_menu'