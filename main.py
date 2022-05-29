
import pygame
import time
from Tetris import Tetris
from TetrisPainter import TetrisPainter
from KeyPressHandler import KeyPressHandler
from Common import Direction

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
running = True
key_press_handler = KeyPressHandler()
ms_until_long_press = 200
ms_elapsed_since_last_key_down = 0
tetris = Tetris(20, 10)
tetris_painter = TetrisPainter(tetris.number_of_rows, tetris.number_of_columns)


def draw_on_update():
    if tetris.has_spawned_figure():
        if tetris.check_rows():
            tetris_painter.score.update(tetris.player.score)
            tetris_painter.redraw_all(tetris.field, tetris.moving_figure)
        else:
            tetris_painter.draw_figure(
                tetris.moving_figure, True)
    else:
        tetris_painter.draw_figure(
            tetris.moving_figure, False)


while running:
    key_press_handler.update_pressed_keys()

    if key_press_handler.is_quit_pressed:
        running = False

    is_new_figure_spawned = False

    for direction in [Direction.RIGHT, Direction.LEFT, Direction.DOWN, Direction.UP]:
        if key_press_handler.is_direction_key_pressed[direction.value]:
            ms_elapsed_now = time.time() * 1000
            # First registered key press
            if ms_elapsed_since_last_key_down == 0:
                ms_elapsed_since_last_key_down = ms_elapsed_now
                tetris.move(direction)
            # Long key press
            elif (ms_elapsed_now - ms_elapsed_since_last_key_down) >= ms_until_long_press:
                tetris.move(direction)

    if not (True in key_press_handler.is_direction_key_pressed):
        ms_elapsed_since_last_key_down = 0

    if tetris.has_moved():
        draw_on_update()

    tetris.update()
    if tetris.has_moved():
        draw_on_update()

    if tetris.is_game_over():
        tetris_painter.redraw_all(tetris.field, tetris.moving_figure)

    tetris_painter.update()
    fpsClock.tick(fps)

pygame.quit()
