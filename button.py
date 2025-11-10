import pygame, sys


class Interactive_button(pygame.sprite.Sprite):
    def __init__(self,location:tuple,
                font:pygame.font.SysFont,
                text='',
                button_surf = None,
                hover_button_surf = None,
                text_color="#FFFFFF",
                color="#0091FF", 
                hover_color="#03FECC",
                size=(0,0)):
        super().__init__()
        
        self.location = location
        self.font = font
        self.text = text
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.size = (0,0)

        #button size
        proper_size = self.setSize()
        if size != (0,0):
            try:
                if size[0] < proper_size[0] or size[1] < proper_size[1]:
                    raise SizeInvalidException
                else:
                    self.size = size
            except:
                print('interactive button size invalid')
                sys.exit()
        else:
            self.size = proper_size


        self.text_surf = self.setText()

        #surface
        if button_surf == None:
            self.button_surf = pygame.Surface(self.size)
            self.button_rect = self.button_surf.fill(self.color)
            self.button_rect.center = self.location
        else:
            self.button_surf = button_surf
            self.button_rect = self.button_surf.get_rect(center=self.location)

        if hover_button_surf == None:
            self.hover_button_surf = pygame.Surface((self.size[0]+20,self.size[1]+20))
            self.hover_button_rect = self.hover_button_surf.fill(self.hover_color)
            self.hover_button_rect.center = self.location
        else:
            self.hover_button_surf = hover_button_surf
            self.hover_button_rect = self.hover_button_surf.get_rect(center=self.location)

        #actual surf and rect
        self.image = self.button_surf
        self.rect = self.button_rect

    
    def setSize(self):
        font_size = self.font.size(self.text)
        return (font_size[0]+30, font_size[1]+30)
    
    def setText(self):
        return self.font.render(self.text,False,self.text_color)

    def update(self, screen:pygame.Surface):
        screen.blit(self.text_surf, self.text_surf.get_rect(center=self.location))

        #check mouse hover
        if self.is_hovered():
            self.image = self.hover_button_surf
            self.rect = self.hover_button_rect
        else:
            self.image = self.button_surf
            self.rect = self.button_rect
            

    def is_pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mouse_pos):
            return True
        return False

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

class SizeInvalidException:
    pass