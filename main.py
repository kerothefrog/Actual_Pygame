import pygame, sys
from starting_menu import StartMenu
from settings import Settings
from main_menu import MainMenu
from credits import Credits
from gameplay import play_game

def get_class(state:str):
    if state == 'start menu':
        return start_menu
    elif state == 'settings':
        return settings
    elif state == 'main_menu':
        return main_menu
    elif state == 'credits':
        return credits
    elif state == 'gameplay':
        play_game(screen=screen)
        state = 'main_menu'
        return main_menu
    else:
        raise ValueError('Invalid state')

pygame.init()
screen = pygame.display.set_mode((900, 400))
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                curr_state = get_class(curr_state).if_button_pressed()


    curr_state = get_class(curr_state).draw()

    pygame.display.update()
    clock.tick(60)