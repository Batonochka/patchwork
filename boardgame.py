import numpy as np
import random as rd
import pygame_constants as const

FIELD_HEIGHT, FIELD_WIDTH = const.FIELD_HEIGHT, const.FIELD_HEIGHT
POSSIBLE_PATCHES = const.POSSIBLE_PATCH_LIST_LEN


class Patch:
    """
    class Patch
    object of this class are copies of tiles from Patchwork
    """
    def __init__(self, price: int, time_token: int, income: int, configuration):
        self.price = price
        self.income = income
        self.time_token = time_token
        self.configuration = configuration

    def get_all_configurations(self):
        all_configuration = [
            np.rot90(self.configuration, 1),
            np.rot90(self.configuration, 1),
            np.rot90(self.configuration, 1),
            np.rot90(self.configuration, 1),
            np.flip(np.rot90(self.configuration, 1), axis=1),
            np.flip(np.rot90(self.configuration, 1), axis=1),
            np.flip(np.rot90(self.configuration, 1), axis=1),
            np.flip(np.rot90(self.configuration, 1), axis=1)
        ]
        return all_configuration

    @property
    def height(self):
        return len(self.configuration)

    @property
    def width(self):
        if self.height == 0:
            return 0
        return len(self.configuration[0])

    def rotation90(self, rotation_number):
        self.configuration = np.rot90(self.configuration, rotation_number)  # rotation 90 on clockwise

    def mirror(self):
        self.configuration = np.flip(self.configuration, axis=1)


class QuiltField:
    """
    make a field for each player, let players put tiles
    """

    def __init__(self):
        self.board = np.zeros((FIELD_HEIGHT, FIELD_WIDTH), dtype=bool)

    # def can_insert_patch(self, x_cor, y_cor, patch):
    #     if (x_cor + patch.width <= 9) and (y_cor + patch.height <= 9):
    #         copy = QuiltField()
    #         copy.board[y_cor: y_cor + patch.height, x_cor: x_cor + patch.width] = patch.configuration
    #         return (np.all(np.invert(copy.board & self.board)), copy.board)

    def insert_tile(self, x_cor, y_cor, patch):
        if (x_cor + patch.width <= FIELD_WIDTH) and (y_cor + patch.height <= FIELD_HEIGHT):
            copy = QuiltField()
            copy.board[y_cor: y_cor + patch.height, x_cor: x_cor + patch.width] = patch.configuration
            if np.all(np.invert(copy.board & self.board)):
                self.board = copy.board + self.board

    def try_insert_patch(self, x_cor, y_cor, patch):
        if (x_cor + patch.width <= FIELD_WIDTH) and (y_cor + patch.height <= FIELD_HEIGHT):
            copy = QuiltField()
            copy.board[y_cor: y_cor + patch.height, x_cor: x_cor + patch.width] = patch.configuration
            if np.all(np.invert(copy.board & self.board)):
                return self.board, copy.board



class Person:
    """
    Player class, contains information about income, bonus,
    time_token position, current buttons
    """
    def __init__(self, first_name, last_name):
        # self.time_token = 0
        self.field = QuiltField()
        self.first_name = first_name
        self.last_name = last_name
        self.have_7x7_bonus = False
        self.income = 0
        self.patches_1x1_num = 0
        self.buttons = 5

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def check_7x7_bonus(self, TimeBoard):
        if TimeBoard._7x7_bonus_gained is False:
            _7x7patch = np.ones((7, 7), dtype=bool)
            for y_cor in range(FIELD_HEIGHT - 7):
                for x_cor in range(FIELD_WIDTH - 7):
                    copy_board = np.zeros((FIELD_WIDTH, FIELD_HEIGHT), dtype=bool)
                    copy_board[y_cor: y_cor + 7, x_cor: x_cor + 7] = _7x7patch
                    if np.array_equal(copy_board, np.logical_and(copy_board, self.field.board)):
                        self.have_7x7_bonus = True
                        TimeBoard._7x7_bonus_gained = True


class TimeBoard:
    """
    The simulation of timeline in the game. Passing tiles players gain buttons.
    Also it   the turn
    """
    def __init__(self, player1, player2):
        self._7x7_bonus_gained = False
        self.turn = True
        self.player1 = player1
        self.player2 = player2
        self.players_position = [0, 0]
        self.button_positions = [4, 10, 16, 22, 28, 34, 40, 46]
        self.patch_1x1_positions = [19, 25, 31, 43, 49, 52]
        self.len = 53

    def check_marked_spaces(self, old_position, new_position, gain_buttons_by_shift=False):
        """
        :param old_position: old position of current player
        :param new_position: new position of current player
        :return: None, just change som player parametres (buttons, 1x1 tiles, give income)
        """
        button_space_num = 0
        _1x1patch_space_num = 0
        if self.turn is True:
            another_player_position = self.players_position[1]
            player = self.player1
        else:
            another_player_position = self.players_position[0]
            player = self.player2
        if new_position > self.len:
            new_position = self.len
        for time_space in range(old_position+1, new_position+1):
            if time_space in self.button_positions:
                button_space_num += 1
        for time_space in range(another_player_position+1, new_position+1):
            if time_space in self.patch_1x1_positions:
                self.patch_1x1_positions.remove(time_space)
                _1x1patch_space_num += 1
        player.patches_1x1_num += _1x1patch_space_num
        player.buttons += player.income * button_space_num
        if gain_buttons_by_shift is True:
            player.buttons += new_position-old_position

    def move_player(self, time_shift, gain_buttons_by_shift):
        """
        :param time_shift: exchange between old and new position
        :return: None, change player's position on the timeboard
        """
        if self.turn is True:
            old_position = self.players_position[0]
            new_position = old_position + time_shift
            if self.len <= new_position:
                self.players_position[0] = self.len
            else:
                self.players_position[0] = new_position
        else:
            old_position = self.players_position[1]
            new_position = old_position + time_shift
            if self.len <= new_position:
                self.players_position[1] = self.len
            else:
                self.players_position[1] = new_position
        self.check_marked_spaces(old_position, new_position, gain_buttons_by_shift)

    def pass_turn(self):
        time_shift = max(self.players_position) - min(self.players_position) + 1
        self.move_player(time_shift, gain_buttons_by_shift=True)
        if self.turn is True:
            self.turn = False
        else:
            self.turn = True

    def check_turn(self):
        '''
        :return:
        '''
        player_1_pos = self.players_position[0]
        player_2_pos = self.players_position[1]
        if player_1_pos < player_2_pos:
            self.turn = True
        elif player_1_pos > player_2_pos:
            self.turn = False
        else:
            if self.turn == True:
                self.turn = True
            else:
                self.turn = False

    def check_winner(self):
        if self.players_position[0] == self.len\
                and self.players_position[1] == self.len:
            missed_tiles = 0
            for line in self.player1.field.board:
                for block in line:
                    if block is False:
                        missed_tiles += 1
            player1_buttons = self.player1.buttons - missed_tiles
            missed_tiles = 0
            for line in self.player2.field.board:
                for block in line:
                    if block is False:
                        missed_tiles += 1
            player2_buttons = self.player2.buttons - missed_tiles
            if player1_buttons == player2_buttons:
                if self.turn is True:
                    winner = self.player1.full_name
                else:
                    winner = self.player2.full_name
            else:
                if player1_buttons > player2_buttons:
                    winner = self.player1.full_name
                else:
                    winner = self.player2.full_name
            return winner
        return None


def make_game_patch_list(PATCHES_without_last, LAST_TILE):
    '''
    список всех игровых тайлов
    :return: list
    return list of patches for the game
    '''
    patch_list = sorted(PATCHES_without_last, key=lambda i: rd.random())
    patch_list.append(LAST_TILE)
    return patch_list


def make_possible_patches_list(choosen_patch, PATCHES):
    """
    список из 3х тайлов, которые доступны игрокам
    :param choosen_patch:
    :return:
    """
    cur_index = PATCHES.index(choosen_patch)
    if POSSIBLE_PATCHES > len(PATCHES):
        return PATCHES
    if cur_index + POSSIBLE_PATCHES < len(PATCHES):
        patch_list = PATCHES[cur_index+1:cur_index+POSSIBLE_PATCHES+1]
        # 4 = POSSIBLE_PATCHES + 1 (1 from the shift of patches)
        return patch_list
    else:
        patch_list = PATCHES[cur_index:len(PATCHES)]
        for index in range(len(PATCHES) - cur_index):
            patch_list.append(PATCHES[index])
    PATCHES.remove(choosen_patch)
    return patch_list


def print_good_tiles(np_massive: np.array):
    for line in np_massive:
        copy_line = []
        for elem in line:
            if elem:
                copy_line.append('+')
            else:
                copy_line.append('-')
        print(f'[{" ".join(copy_line)}]')


def convert_data_to_tile(patch_info):
    price = patch_info['price']
    income = patch_info['income']
    time_token = patch_info['time_token']
    configuration = patch_info['configuration']
    patch = Patch(income=income, price=price, time_token=time_token,
                  configuration=configuration)
    return patch


PATCHES_without_last = [convert_data_to_tile(patch_info) for patch_info in const.PATCHES_without_last]
LAST_TILE = convert_data_to_tile(const.LAST_TILE)
patch_1x1 = convert_data_to_tile(const.patch_1x1)

if __name__ == '__main__':
    running = True
    Player1 = Person('player', '1')
    Player2 = Person('player', '2')
    timeboard = TimeBoard(Player1, Player2)
    PATCHES = make_game_patch_list(PATCHES_without_last, LAST_TILE)
    patch_list = PATCHES[:3]
    old_turn = True
    current_patch = None
    chose_1x1patch = False
    # whole game running in terminal
    while running:
        if timeboard.turn is True:
            player = Player1
            player_position = timeboard.players_position[0]
        else:
            player = Player2
            player_position = timeboard.players_position[1]
        # if old_turn != TimeBoard.turn:
        # вывод информации об игроке, тайлах и поле
        print(player.full_name)
        print_good_tiles(player.field.board)
        for patch in patch_list:
            print('income', patch.income, ', price', patch.price, ', time_shift', patch.time_token)
            print_good_tiles(patch.configuration)
        print('_1x1patch_positions', timeboard.patch_1x1_positions)
        print('buttons_position', timeboard.button_positions)
        print('time position', player_position, 'buttons', player.buttons)
        # анализируем действия игрока
        event = input()
        event = event.split()
        if event[0] == '1':
            if player.buttons >= patch_list[0].price:
                current_patch = patch_list[0]
            if current_patch is not None:
                print_good_tiles(current_patch.configuration)
        if event[0] == '2':
            if player.buttons >= patch_list[1].price:
                current_patch = patch_list[1]
            if current_patch is not None:
                print_good_tiles(current_patch.configuration)
        if event[0] == '3':
            if player.buttons >= patch_list[2].price:
                current_patch = patch_list[2]
            if current_patch is not None:
                print_good_tiles(current_patch.configuration)
        # меняем конфигурации тайлов
        if event[0] == 'r':
            if current_patch is not None:
                current_patch.rotation90(1)
                print_good_tiles(current_patch.configuration)
        if event[0] == 'm':
            if current_patch is not None:
                current_patch.mirror()
                print_good_tiles(current_patch.configuration)
        # пропуск хода
        if event[0] == '5':
            timeboard.pass_turn()
            winner = timeboard.check_winner()
            print('------')
            if winner is not None:
                print('winner is', winner)
                break
        if event[0] == '4':
            if player.patches_1x1_num > 0:
                current_patch = patch_1x1
                chose_1x1patch = True
        if event[0] == '6':
            if current_patch is not None:
                if timeboard.turn is True:
                    player = Player1
                else:
                    player = Player2
                tile_position = [int(event[1]), int(event[2])]
                old_board = player.field.board
                player.field.insert_tile(patch=current_patch,
                                         x_cor=tile_position[0],
                                         y_cor=tile_position[1])
                if np.array_equal(old_board, player.field.board) is False:
                    player.check_7x7_bonus(timeboard)
                    time_shift = current_patch.time_token
                    player.income += current_patch.income
                    player.buttons -= current_patch.price
                    timeboard.move_player(time_shift, gain_buttons_by_shift=False)
                    winner = timeboard.check_winner()
                    if winner is not None:
                        print('winner is', winner)
                        break
                    if chose_1x1patch is True:
                        player.patches_1x1_num -= 1
                    # old_turn = timeboard.turn
                    timeboard.check_turn()
                    if current_patch != patch_1x1:
                        patch_list = make_possible_patches_list(current_patch, PATCHES)
                    current_patch = None
                    print('--------')
