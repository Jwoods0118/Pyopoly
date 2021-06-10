
def load_map(map_file_name):
    import csv
    try:
        with open(map_file_name) as map_file:
            reader = csv.DictReader(map_file, delimiter='\t')
            the_map = [dict(x) for x in reader]
            return the_map
    except OSError:
        print('Unable to find or open the file.')


def draw_in_block(block_num, side_length, the_grid, contents):
    if block_num in range(0, side_length):
        # along the bottom, gotta count up from the bottom by 3 rows
        starting_row = len(the_grid) - 3
        starting_col = len(the_grid[0]) - (block_num + 1) * 6
    elif block_num in range(side_length, 2 * side_length):
        starting_col = 1
        starting_row = len(the_grid) - 3 * ((block_num + 1) - side_length)
    elif block_num in range(2 * side_length, 3 * side_length):
        starting_row = 1
        starting_col = 6 * (block_num - 2 * side_length) + 1
    else:
        starting_col = len(the_grid[0]) - 6
        starting_row = 3 * (block_num - 3 * side_length) + 1

    split_contents = contents.split('\n')
    for row in range(2):
        for col in range(5):
            if col < len(split_contents[row]):
                the_grid[starting_row + row][starting_col + col] = split_contents[row][col]


def display_board(the_board):
    side_length = len(the_board) // 4 + 1
    grid = [['*' if (not (i % 6) or not (j % 3)) and ((0 <= i <= 6 or (side_length - 1) * 6 <= i) or (0 <= j <= 3 or (side_length - 1) * 3 <= j)) else " "
             for i in range(side_length * 6 + 1)] for j in range(side_length * 3 + 1)]

    for i, place in enumerate(the_board):
        draw_in_block(i, side_length - 1, grid, place)

    display_grid = '\n'.join([''.join(grid[i]) for i in range(3 * side_length + 1)])
    print(display_grid)
