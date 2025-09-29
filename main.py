import pygame, sys
from starting_background import StartMenu
from settings import Settings
from main_menu import MainMenu
from credits import Credits

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("31426")
clock = pygame.time.Clock()

curr_state = 'start menu'
start_menu = StartMenu(screen)
settings = Settings(screen)
main_menu = MainMenu(screen)
credits = Credits(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    if curr_state == 'start menu':
        curr_state = start_menu.draw()
    elif curr_state == 'main_menu':
        curr_state = main_menu.draw()
    elif curr_state == 'settings':
        curr_state = settings.draw()
    elif curr_state == 'credits':
        curr_state = credits.draw()


    pygame.display.update()
    clock.tick(60)