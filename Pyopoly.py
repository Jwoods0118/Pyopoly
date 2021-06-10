if len(argv) >= 2:
    seed(argv[1])
import csv


def get_players(player_one, player_two):
    # Player name and symbol input
    player_one['Name'] = input('First player, what is your name? ').upper()
    player_one['Symbol'] = input('First player, what symbol do you want your character to use? ').upper()

    # Check to see if the symbol is greater than one character, if so reprompt
    if len(player_one['Symbol']) > 1:
        print('Your symbol can only be one character long! Try Again')
        get_players(player_one, player_two)
    player_two['Name'] = input('Second player, what is your name? ').upper()
    player_two['Symbol'] = input('Second player, what symbol do you want your character to use? ').upper()

    # Check to see if the symbol is greater than one character, if so reprompt
    if len(player_one['Symbol']) > 1:
        print('Your symbol can only be one character long! Try Again')
        get_players(player_one, player_two)

    print()


# This function is where the actual game will take place
def play_game(starting_money, pass_go_money, board_selection):
    # Board map
    board = load_map(board_selection)

    # Player one and two dictionaries
    player_one = {'Name': 'Player', 'Symbol': 'x', 'Money': 1500, 'Is_Rolling': True, 'Properties': [], 'Position': 0,
                  'Location': board[0]}
    player_two = {'Name': 'Player', 'Symbol': 'x', 'Money': 1500, 'Is_Rolling': False, 'Properties': [],
                  'Position': 0,
                  'Location': board[0]}

    # Players will be used to easily access the both players if needed
    players = [player_one, player_two]

    # Get player info, gathers the name and symbol of the player
    get_players(player_one, player_two)

    # While each player has enough money, the game will proceed
    # Whoever runs out of money first, loses
    while players[0]['Money'] > 0 and players[1]['Money'] > 0:
        take_turn(player_one, players, board)
        take_turn(player_two, players, board)


# buying properties, getting player info, rolling the dice, and ending turn:
def take_turn(player, players, board):
    # Determing who will be rolling
    if players[0]['Is_Rolling'] == True:

        # Rolling the dice
        die_one = randint(1, 6)
        die_two = randint(1, 6)
        roll = die_one + die_two

        # Moving the player
        if player['Position'] + roll > len(board):
            # Paying the player if the position plus the roll is greater than the board
            player['Money'] += 200
            print('You passed go, 200 ducats have been added to your balance!')
        player['Position'] += roll
        player['Position'] %= len(board)

        # Displays the players position on the board
        player['Location'] = board[player['Position']]
        players[0] = player
        format_display(players, board)

        # Formatting that makes the board nicer looking
        # Displays the players dice roll
        print('-------------------')
        print(players[0]['Name'], 'You rolled a', roll)
        print('You landed on', players[0]['Location']['Place'])
        print('-------------------')

        # End turn, change who will go next
        # Changes who will roll next time around
        players[0]['Is_Rolling'] = False
        players[1]['Is_Rolling'] = True

        # Paying Rent, buying properties, seeing player/building info, ending turn
        paying_rent(player, players, board)

        # Determing who will be rolling
    elif players[0]['Is_Rolling'] == False:

        # Rolling the dice
        die_one = randint(1, 6)
        die_two = randint(1, 6)
        roll = die_one + die_two

        # Moving the player
        if player['Position'] + roll > len(board):
            player['Money'] += 200

            # Paying the player if the position plus the roll is greater than the board
            print('You passed go, 200 ducats have been added to your balance!')
        player['Position'] += roll
        player['Position'] %= len(board)
        player['Location'] = board[player['Position']]
        players[1] = player
        format_display(players, board)
        # Formatting that makes the board nicer looking
        # Displays the players dice roll
        print('-------------------')
        print(players[1]['Name'], 'You rolled a', roll)
        print('You landed on', players[1]['Location']['Place'])
        print('-------------------')

        # End turn, change who will go next
        # Changes who will roll next time around
        players[1]['Is_Rolling'] = False
        players[0]['Is_Rolling'] = True

        # Paying Rent, buying properties, seeing player/building info, ending turn
        paying_rent(player, players, board)


def paying_rent(player, players, board):
    # Find the player who needs to pay the rent, this block of code is for player one
    # These two blocks of code take the position of the player
    # Checks if the property belongs to the opposing player
    # And subtracts/adds the rent
    if player == players[0]:
        if player['Location']['Place'] in players[1]['Properties']:
            print('You paid', players[1]['Name'], player['Location']['Rent'], 'ducats for rent')
            player['Money'] -= int(player['Location']['Rent'])
            players[1]['Money'] += int(player['Location']['Rent'])
            print()
            menu_options(player, players, board)

        else:
            # If rent is not needed to be paid, proceed to the menu
            print()
            menu_options(player, players, board)

    # Find the player who needs to pay the rent, this block of code is for player two
    if player == players[1]:
        if player['Location']['Place'] in players[0]['Properties']:
            player['Money'] -= int(player['Location']['Rent'])
            players[0]['Money'] += int(player['Location']['Rent'])
            print('You paid', players[0]['Name'], player['Location']['Rent'], 'ducats for rent')
            print()
            menu_options(player, players, board)

        else:
            print()
            menu_options(player, players, board)


def menu_options(player, players, board):
    # Take user input (number or word)
    menu = input(
        'Would you like to: \n1)Buy Property \n2)Property Info \n3)Player Info \n4)Build a Building \n5)End Turn\n')
    print()
    # Buying of the property
    if menu.lower() == 'buy property' or menu == '1':
        buy_properties(player, players, board)

    elif menu.lower() == 'property info' or menu == '2':
        property_info(player, players, board)

    elif menu.lower() == 'player info' or menu == '3':
        player_info(player, players, board)

    elif menu.lower() == 'build a building' or menu == '4':
        building_buildings(player, players, board)

    # This function is used if the player would like to buy the property they are on


def buy_properties(player, players, board):
    # An if statement that checks if the property is buyable
    if player['Location'] in players[0]['Properties'] or player['Location'] in players[1]['Properties'] or \
            player['Location']['Price'] == '-1' or player['Location']['Price'] == '0':
        print('This property is not buyable!')
        print()
        menu_options(player, players, board)
    # If buyable, the else statement prompts the user for validation
    else:
        print('You are buying', player['Location']['Place'], 'for', player['Location']['Price'])
        validate = input('Enter yes to continue, or cancel to cancel transaction: ')
        print()
        if validate.lower() == 'yes':
            # Check to see if the player has enough money for the property
            if player['Money'] >= int(board[player['Position']]['Price']):
                # Charge the player the according price of the property
                player['Money'] -= int(board[player['Position']]['Price'])
                # Add the property to the players dictionary at ['Properties']
                player['Properties'].append(player['Location']['Place'])
                print('Purchase was successful!')
                print()
                board[player['Position']]['Price'] = '-1'
                menu_options(player, players, board)
            else:
                # If player does not have enough money, prompt an error buying message
                print('You do not have enough money')
                menu_options(player, players, board)
            # Allow the user to cancel the transaction if desired
        elif validate.lower() == 'cancel':
            menu_options(player, players, board)
            # Else statement used for non-related user input
        else:
            print('Invalid Response, Please enter again!')
            menu_options(player, players, board)

    # This function is used for when the player would like to
    # access the information about the location they are on


def property_info(player, players, board):
    # Getting info for the properties
    for info in player['Location']:
        print(info, ':', board[player['Position']][info])
    print()
    menu_options(player, players, board)

    # Getting player info


def player_info(player, players, board):
    print('Which player info would you like?')
    choose_player = input('1) Player One \n2) Player Two\n')

    # Info for player one
    if choose_player.lower() == 'player one' or choose_player.lower() == '1':
        for player_one_info in players[0]:
            print(player_one_info, players[0][player_one_info])
        print()
        menu_options(player, players, board)

    # Info for player two
    if choose_player.lower() == 'player two' or choose_player.lower() == '2':
        for player_one_info in players[1]:
            print(player_one_info, players[1][player_one_info])
        print()
        menu_options(player, players, board)

        # If statement for a non-related user input
    else:
        print('Invalid Response, Please enter again!')
        menu_options(player, players, board)

# Allows the player to build buildings
def building_buildings(player, players, board):
    print('Here are your properties:')

    # Display the players purchased properties
    for buildings in player['Properties']:
        print(buildings)
        print()

    # Ask the user which properties they would like to buy buildings for
    print('*Note this is case sensitive, type in the locations full name and with capital letter')
    choose_property = input('Which Property would you like to buy buildings for?: ')
    print()

    # Display the building cost
    # Validate that the user still wants to purchase
    print('This transaction will cost you,', board[player['Position']]['BuildingCost'])
    validation = input('Are you sure you want to purchase?(Yes or No)\n')

    # Subtract the cost of building the building
    if validation.lower() == 'yes' and choose_property in player['Properties']:
        player['Money'] -= int(board[player['Position']]['BuildingCost'])
        # Change the rent of the building to the new rent of the built building
        board[player['Position']]['Rent'] = board[player['Position']]['BuildingRent']
        menu_options(player, players, board)

    else:
        # reprompt if the user input is non-related
        print('That was an invalid input, try again!')
        menu_options(player, players, board)


# This is used to display the board and move the players around:
def format_display(players, board):
    location_list = []
    for i in board:
        location = i['Abbrev']
        players_at_space = ''

        # Take the players (Players[0] = player one and Players[1] = player two
        if players[0]['Location']["Abbrev"] == i["Abbrev"]:
            players_at_space += players[0]['Symbol']

        if players[1]['Location']["Abbrev"] == i["Abbrev"]:
            players_at_space += players[1]['Symbol']
        players_at_space = players_at_space.ljust(5)
        string = location + '\n' + players_at_space
        location_list.append(string)

    display_board(location_list)


# All the board variables we will need:
board = load_map("proj1_board1.csv")
board_one = 'python3 pyopoly.pyc 12345 proj1_board1.csv'
board_two = 'python3 pyopoly.pyc abcde proj1_board2.csv'

# Starting money and pass go money
starting_money = 1500
pass_go_money = 200

# Formatting to make the board look nice
# User input for choosing the board
print('*/*/*/ ~WELCOME TO PYOPOLY~ \*\*\*')
print('   Developed by Woods Ingenuity')
print()
print(
    'Objective:\n~Try and accumulate the most money and properties\n~Both players will start out with 1500 ducats\n~First player to run out of money loses!\n~Good luck!')
print()

# Allows players to choose the board they would like to play on
print('Which Board would you like to use?')
print('1) Board One')
print('Desc: Small Board (8 Spaces), good for quick play!')
print()
print('2) Board Two')
print('Desc: Large Board (40 Spaces), similar to original Monopoly!')
print()
board = ''
board_selection = input('Which Board would you like to use? (Enter a number or enter \'Board One or Board Two\')\n')

if __name__ == '__main__':
    # Choosing which board the player wants to play on
    # Takes the input and then calls the play_game function
    # This if statement loads map 1
    if board_selection.lower() == 'board one' or board_selection.lower() == '1':
        board = 'proj1_board1.csv'
        play_game(starting_money, pass_go_money, board)

    # This if statement loads map 2
    if board_selection.lower() == 'board two' or board_selection.lower() == '2':
        board = 'proj1_board2.csv'
        play_game(starting_money, pass_go_money, board)
