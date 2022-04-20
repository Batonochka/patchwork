import sys
import pygame
import boardgame as bg
import pygame_constants as const
import numpy as np

"""
Документация в этом куске *кхм* кода будет теперь на русском,
потому что я заколебался до резонанса писать ее в гугле на русском и здесь 
на ломаном английском, а потом еще его и обратно расшифровывать,
чтобы хоть что-то понять спустя 3 недели ААААААААААА
"""
FIELD_WIDTH, FIELD_HEIGHT = const.FIELD_WIDTH, const.FIELD_HEIGHT
WIDTH, HEIGHT = const.WIDTH, const.HEIGHT
Player1 = bg.Person('player', '1')
Player2 = bg.Person('player', '2')
TimeBoard = bg.TimeBoard(Player1, Player2)
FPS = 30
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
block_size = 50
mini_block_size = 10
otstup = 10
mini_otstup = 1
text_otstup = 25

# рисует квадратики и делает это как надо
def draw_block(block_pos, color, block_size):
    x, y = block_pos[0], block_pos[1]
    pygame.draw.rect(screen, color, pygame.Rect(x, y, block_size, block_size))


def draw_patch(mouse_position, patch, insert=False):
    try:
        if TimeBoard.turn is True:
            player = TimeBoard.player1
            field_cor = (otstup, otstup)
        else:
            player = TimeBoard.player2
            field_cor = (otstup * 2 + (otstup + block_size) * FIELD_WIDTH, otstup)
        for block_num in range(FIELD_WIDTH):
            block_cor = field_cor[0] + (block_size + otstup) * block_num
            if block_cor > mouse_position[0]:
                break
        for line_num in range(FIELD_HEIGHT):
            line_cor = field_cor[1] + (block_size + otstup) * line_num
            if line_cor > mouse_position[1]:
                break
        if insert is False:
            board_without_patch, tile_board = player.field.try_insert_patch(block_num, line_num, patch)
        else:
            board_without_patch = player.field.board
            player.field.insert_tile(block_num, line_num, patch)
            tile_board = player.field.board
        for line_ind in range(FIELD_HEIGHT):
            for block_ind in range(FIELD_WIDTH):
                if board_without_patch[line_ind][block_ind]:
                    color = RED
                elif tile_board[line_ind][block_ind]:
                    color = BLUE
                else:
                    color = GREEN
                x_cor = field_cor[0] + (block_size + otstup) * block_ind
                y_cor = field_cor[1] + (block_size + otstup) * line_ind
                draw_block((x_cor, y_cor), color, block_size)
        if insert:
            return np.array_equal(board_without_patch, tile_board)
    except BaseException as exception:
        pass




def draw_limiters():
    x = otstup * 2 + (otstup + block_size) * FIELD_WIDTH * 2
    y = otstup + (otstup + block_size) * FIELD_HEIGHT
    pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT), 1)
    pygame.draw.line(screen, WHITE, (0, y), (x, y), 1)


def draw_possible_patches(possible_patch_list, choosen_patch):
    pygame.draw.rect(screen, BLACK, (otstup * 3 + (otstup + block_size) * FIELD_WIDTH * 2, otstup,
                                     WIDTH, HEIGHT))
    data_position_x = otstup * 3 + (otstup + block_size) * FIELD_WIDTH * 2
    f1 = pygame.font.Font(None, 36)
    dynamic_y = 0
    for patch_ind in range(len(possible_patch_list)):
        patch = possible_patch_list[patch_ind]
        if patch is choosen_patch:
            color = RED
        else:
            color = GREEN
        for line_ind in range(patch.height):
            for block_ind in range(patch.width):
                if patch.configuration[line_ind][block_ind]:
                    x_cor = data_position_x + (mini_otstup+mini_block_size)*block_ind
                    y_cor = otstup + dynamic_y + (mini_otstup+mini_block_size)*line_ind
                    draw_block((x_cor, y_cor), color, mini_block_size)
        screen.blit(f1.render(f'income: {patch.income}', True, WHITE),
                    (data_position_x, dynamic_y + text_otstup + patch.height * (mini_block_size + mini_otstup)))
        screen.blit(f1.render(f'price: {patch.price}', True, WHITE),
                    (data_position_x, dynamic_y + 2 * text_otstup + patch.height * (mini_block_size + mini_otstup)))
        screen.blit(f1.render(f'time: {patch.time_token}', True, WHITE),
                    (data_position_x, dynamic_y + 3 * text_otstup + patch.height * (mini_block_size + mini_otstup)))
        dynamic_y += 4 * text_otstup + patch.height * (mini_block_size + mini_otstup)
        # константы пока константы, понятия не имею, как их считать, но они как-то зависят от шрифта


def draw_Field():
    pygame.draw.rect(screen, BLACK, (otstup, otstup,
                                     otstup + (block_size+otstup)*FIELD_WIDTH*2,
                                     (block_size+otstup)*FIELD_HEIGHT))
    player_field = TimeBoard.player1.field.board
    for line_ind in range(FIELD_HEIGHT):
        for block_ind in range(FIELD_WIDTH):
            if player_field[line_ind][block_ind]:
                color = RED
            else:
                color = GREEN
            x, y = block_ind, line_ind
            x_cor = otstup + (otstup + block_size) * block_ind
            y_cor = otstup + (otstup + block_size) * line_ind
            draw_block((x_cor, y_cor), color, block_size=block_size)
    player_field = TimeBoard.player2.field.board
    for line_ind in range(FIELD_HEIGHT):
        for block_ind in range(FIELD_WIDTH):
            if player_field[line_ind][block_ind]:
                color = RED
            else:
                color = GREEN
            x, y = block_ind, line_ind
            x_cor = otstup * 2 + (otstup + block_size) * (block_ind + FIELD_WIDTH)
            y_cor = otstup + (otstup + block_size) * line_ind
            draw_block((x_cor, y_cor), color, block_size=block_size)


def draw_players_info():
    text_position_y = 2 * otstup + (otstup + block_size) * FIELD_HEIGHT
    text_position_x = otstup
    pygame.draw.rect(screen, BLACK, (text_position_x, text_position_y,
                                     otstup + 2 * (otstup + block_size) * FIELD_WIDTH,
                                     HEIGHT))
    f1 = pygame.font.Font(None, 36)
    players = [TimeBoard.player1, TimeBoard.player2]
    for player in players:
        screen.blit(f1.render(f'{player.full_name}', True, WHITE),
                    (text_position_x, text_position_y))
        screen.blit(f1.render(f'buttons: {player.buttons}', True, WHITE),
                    (text_position_x, text_position_y + text_otstup))
        screen.blit(f1.render(f'income: {player.income}', True, WHITE),
                    (text_position_x, text_position_y + 2 * text_otstup),)
        if player.have_7x7_bonus:
            bonus = 'Yes'
        else:
            bonus = 'No'
        screen.blit(f1.render(f'gained 7x7 bonus tile: {bonus}', True, WHITE),
                    (text_position_x, text_position_y + 3 * text_otstup))
        text_position_x += otstup + (otstup + block_size) * FIELD_WIDTH


def draw_winner(winner):
    screen.fill((0, 0, 0))
    f2 = pygame.font.Font(None, 60)
    screen.blit(f2.render(f'The winner is {winner}', True, WHITE),
                 (200, 540))

if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    screen.fill((0, 0, 0))
    pygame.display.set_caption("PATCHWORK boardgame")
    clock = pygame.time.Clock()
    running = True
    PATCHES_without_last = bg.PATCHES_without_last
    LAST_TILE = bg.LAST_TILE
    patch_1x1 = bg.patch_1x1
    game_patch_list = bg.make_game_patch_list(PATCHES_without_last, LAST_TILE)
    patch_list = game_patch_list[:3]
    chosen_patch = None
    winner = None
    current_player = TimeBoard.player1
    pygame.init()
    draw_Field()
    draw_limiters()
    draw_possible_patches(patch_list, None)
    draw_players_info()
    clock.tick(FPS)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    TimeBoard.pass_turn()
                    winner = TimeBoard.check_winner()
                    if winner is not None:
                        running = False
                        draw_winner(winner)
                    chosen_patch = None
                    TimeBoard.check_turn()
                    draw_Field()
                    draw_possible_patches(patch_list, chosen_patch)
                    draw_players_info()
                    if TimeBoard.turn:
                        current_player = TimeBoard.player1
                    else:
                        current_player = TimeBoard.player2
                if event.key == pygame.K_1:
                    if current_player.buttons >= patch_list[0].price:
                        chosen_patch = patch_list[0]
                    if current_player.patches_1x1_num >= 1:
                        chosen_patch = patch_1x1
                    draw_possible_patches(patch_list, chosen_patch)
                    mouse_position = pygame.mouse.get_pos()
                    draw_Field()
                    draw_patch(mouse_position, chosen_patch)
                if event.key == pygame.K_2:
                    if current_player.buttons >= patch_list[1].price:
                        chosen_patch = patch_list[1]
                    if current_player.patches_1x1_num >= 1:
                        chosen_patch = patch_1x1
                    draw_possible_patches(patch_list, chosen_patch)
                    mouse_position = pygame.mouse.get_pos()
                    draw_Field()
                    draw_patch(mouse_position, chosen_patch)
                if event.key == pygame.K_3:
                    if current_player.buttons >= patch_list[2].price:
                        chosen_patch = patch_list[2]
                    if current_player.patches_1x1_num >= 1:
                        chosen_patch = patch_1x1
                    draw_possible_patches(patch_list, chosen_patch)
                    mouse_position = pygame.mouse.get_pos()
                    draw_Field()
                    draw_patch(mouse_position, chosen_patch)
                if event.key == pygame.K_SPACE and chosen_patch is not None:
                    chosen_patch.mirror()
                    draw_possible_patches(patch_list, chosen_patch)
                    mouse_position = pygame.mouse.get_pos()
                    draw_Field()
                    draw_patch(mouse_position, chosen_patch)
                if event.key == pygame.K_RIGHT and chosen_patch is not None:
                    chosen_patch.rotation90(3)
                    draw_possible_patches(patch_list, chosen_patch)
                    mouse_position = pygame.mouse.get_pos()
                    draw_Field()
                    draw_patch(mouse_position, chosen_patch)
                if event.key == pygame.K_LEFT and chosen_patch is not None:
                    chosen_patch.rotation90(1)
                    draw_possible_patches(patch_list, chosen_patch)
                    mouse_position = pygame.mouse.get_pos()
                    draw_Field()
                    draw_patch(mouse_position, chosen_patch)
            if event.type == pygame.MOUSEMOTION and chosen_patch is not None:
                mouse_position = pygame.mouse.get_pos()
                draw_Field()
                draw_patch(mouse_position, chosen_patch)
            if event.type == pygame.MOUSEBUTTONDOWN and chosen_patch is not None:
                mouse_position = pygame.mouse.get_pos()
                is_patch_drew = draw_patch(mouse_position, chosen_patch, insert=True)
                if is_patch_drew is False:
                    if chosen_patch is patch_1x1:
                        current_player.patches_1x1_num -= 1
                    else:
                        patch_list = bg.make_possible_patches_list(chosen_patch, game_patch_list)
                    current_player.check_7x7_bonus(TimeBoard)
                    time_shift = chosen_patch.time_token
                    current_player.income += chosen_patch.income
                    current_player.buttons -= chosen_patch.price
                    TimeBoard.move_player(time_shift, gain_buttons_by_shift=False)
                    winner = TimeBoard.check_winner()
                    if winner is not None:
                        running = False
                        draw_winner(winner)
                    TimeBoard.check_turn()
                    if TimeBoard.turn:
                        current_player = TimeBoard.player1
                    else:
                        current_player = TimeBoard.player2
                    chosen_patch = None
                    draw_Field()
                    draw_possible_patches(patch_list, chosen_patch)
                    draw_players_info()
        if winner is not None:
            draw_winner(winner)
            pygame.display.update()
            pygame.time.wait(6000)
        pygame.display.update()
