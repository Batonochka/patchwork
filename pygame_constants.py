import numpy as np


FIELD_WIDTH = 9
FIELD_HEIGHT = 9
WIDTH = 1920
HEIGHT = 1080
POSSIBLE_PATCH_LIST_LEN = 3
patch_1x1 = {'price': 0, 'income': 0, 'time_token': 0, 'configuration': np.array([[ True]])}
PATCHES_without_last = [
    {'price': 5, 'income': 2, 'time_token': 4, 'configuration': np.array([[False, True, False],
                                                                       [True, True, True],
                                                                       [False, True, False]])},
    {'price': 3, 'income': 1, 'time_token': 2, 'configuration': np.array([[True, True, False],
                                                                       [False, True, True]])},
    {'price': 8, 'income': 3, 'time_token': 6, 'configuration': np.array([[False, True, True],
                                                                       [True, True, True],
                                                                       [True, False, False]])},
    {'price': 10, 'income': 3, 'time_token': 5, 'configuration': np.array([[True, True, True, True],
                                                                        [False, False, True, True]])},
    # {'price': 2, 'income': 5, 'time_token': 15, 'configuration': np.array([[True, False, True, True, True],
    #                                                                     [True, False, True, False, False],
    #                                                                     [True, True, True, True, True],
    #                                                                     [False, False, True, False, True],
    #                                                                     [True, True, True, False, True]])},
    {'price': 2, 'income': 0, 'time_token': 3, 'configuration': np.array([[True, False, True],
                                                                       [True, True, True],
                                                                       [True, False, True]])},
    {'price': 1, 'income': 1, 'time_token': 4, 'configuration': np.array([[False, False, True, False, False],
                                                                       [True, True, True, True, True],
                                                                       [False, False, True, False, False]])},
    {'price': 1, 'income': 0, 'time_token': 2, 'configuration': np.array([[True, False, False, False],
                                                                       [True, True, True, True],
                                                                       [False, False, False, True]])},
    {'price': 3, 'income': 0, 'time_token': 1, 'configuration': np.array([[True, True],
                                                                       [True, False]])},
    {'price': 7, 'income': 3, 'time_token': 6, 'configuration': np.array([[True, True, False],
                                                                       [False, True, True]])},
    {'price': 7, 'income': 1, 'time_token': 1, 'configuration': np.array([[ True,  True,  True,  True,  True]])},
    {'price': 2, 'income': 1, 'time_token': 3, 'configuration': np.array([[True, True, True, False],
                                                                       [False, False, True, True]])},
    {'price': 10, 'income': 3, 'time_token': 4, 'configuration': np.array([[False, False, True],
                                                                        [False, True, True],
                                                                        [True, True, False]])},
    {'price': 2, 'income': 0, 'time_token': 2, 'configuration': np.array([[ True,  True,  True]])},
    {'price': 3, 'income': 1, 'time_token': 3, 'configuration': np.array([[ True,  True,  True,  True]])},
    {'price': 5, 'income': 1, 'time_token': 3, 'configuration': np.array([[False, True, True, False],
                                                                       [True, True, True, True],
                                                                       [False, True, True, False]])},
    {'price': 1, 'income': 0, 'time_token': 2, 'configuration': np.array([[True, True, True],
                                                                       [True, False, True]])},
    {'price': 4, 'income': 1, 'time_token': 2, 'configuration': np.array([[False, False, True],
                                                                       [True, True, True]])},
    {'price': 4, 'income': 0, 'time_token': 2, 'configuration': np.array([[False, True, True, True],
                                                                       [True, True, True, False]])},
    {'price': 2, 'income': 0, 'time_token': 2, 'configuration': np.array([[True, True, True],
                                                                       [False, True, True]])},
    {'price': 3, 'income': 1, 'time_token': 4, 'configuration': np.array([[True, True, True, True],
                                                                       [False, False, True, False]])},

    {'price': 2, 'income': 0, 'time_token': 2, 'configuration': np.array([[True, True, True],
                                                                       [False, True, False]])},
    {'price': 3, 'income': 2, 'time_token': 6, 'configuration': np.array([[False, True, True],
                                                                       [True, True, False],
                                                                       [False, True, True]])},
    {'price': 10, 'income': 2, 'time_token': 3, 'configuration': np.array([[True, True, True, True],
                                                                        [True, False, False, False]])},
    {'price': 1, 'income': 1, 'time_token': 5, 'configuration': np.array([[True, True, True, True],
                                                                       [True, False, False, True]])},
    {'price': 7, 'income': 2, 'time_token': 4, 'configuration': np.array([[False, True, True, False],
                                                                       [True, True, True, True]])},
    {'price': 2, 'income': 0, 'time_token': 1, 'configuration': np.array([[False, False, True, False],
                                                                       [True, True, True, True],
                                                                       [False, True, False, False]])},
    {'price': 6, 'income': 2, 'time_token': 5, 'configuration': np.array([[True, True],
                                                                       [True, True]])},
    {'price': 1, 'income': 0, 'time_token': 3, 'configuration': np.array([[False, True],
                                                                       [True, True]])}
]
LAST_TILE = {'price': 2, 'income': 0, 'time_token': 1, 'configuration': np.array([[ True,  True]])}