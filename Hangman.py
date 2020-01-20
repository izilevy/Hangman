import random
import os

# The Hangman game based on the input file of words to be used as the words to be guessed and using the
# index number the user will enter to choose the hidden word to guess in the game.

# Start / welcome screen for the game - CONSTANT
HANGMAN_ASCII_ART = """  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/

"""

# Dictionary which includes all of the hangman stages - 8 correct stages for 7 wrong guesses.
# The first stage, #0, is the initial stage and does not count as mistake.
# That's is why is have added another stage number 4 to complete the correct number of
# mistakes allowed in the HANGMAN game - CONSTANT
HANGMAN_PHOTOS = {'0': """
    x-------x
""", '1': """    x-------x
    |
    |
    |
    |
    |
""", '2': """    x-------x
    |       |
    |       0
    |
    |
    |
""", '3': """    x-------x
    |       |
    |       0
    |       |
    |
    |
""", '4': """    x-------x
    |       |
    |       0
    |      /|
    |
    |
""", '5': """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
""", '6': """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
""", '7': """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
"""}

MAX_TRIES = 7  # The number of maximum tries for the user to have in a single game - CONSTANT


# Game start
def main():
    tries = 0  # tries counter
    list_of_letters = []  # list of letters which the user has already guessed
    secret_word = welcome_screen(tries).lower()  # the secret word which the user needs to reveal

    while tries < MAX_TRIES:  # loop to get the user guesses as long as the tries are below the MAX_TRIES
        guess = str(input("Guess a letter: ")).lower()  # get the user guess letter
        clear_and_logo()  # clear the screen and show the logo
        can_be_updated = try_update_letter_guessed(guess, list_of_letters)  # gets the boolean response from the
        # function while prints to the console from the function
        win = check_win(secret_word, list_of_letters)  # checks if the user got the full word completed and won the game
        if can_be_updated & (guess in secret_word):  # checks if the guess is in secret word and if it is valid input
            print(show_hidden_word(secret_word, list_of_letters))
        elif (is_valid_input(guess) & (guess in secret_word)) | (
                (not can_be_updated) & (guess not in secret_word) & (guess in list_of_letters)):
            # checks if the guess is a valid input and part of the word OR not valid input and not part
            # in the word but is in the list of letters
            continue
        elif (can_be_updated & (guess not in secret_word) & (guess in list_of_letters)) | (is_valid_input(guess)):
            # checks if the guess is valid input and not part of the word but is part of the letters list
            # OR if it is only a valid input, in order to print out the mistakes output
            tries += 1
            print(":(")
            print_hangman(tries)
            print(show_hidden_word(secret_word, list_of_letters))
        if win:  # checks if the user got the full word and exits the loop
            print("WIN")
            break
        elif (not win) & (
                tries == MAX_TRIES):  # checks if the user got to the maximum tries allowed and did not complete the
            # secret word
            print("LOSE")
            break


def welcome_screen(tries):
    """
    Clears the screen and prints the hangman welcome screen and gets the initial input demands for the game.
    :param tries:               the number of tries
    :type tries:                int
    :return:                    the secret word for the user to guess
    :rtype:                     string
    """
    clear_and_logo()
    # The input of the user for TXT words file and word index
    file_location = input("Please enter the words file path: ")
    while not os.path.exists(file_location): # check if the file exist
        file_location = input("FILE NOT FOUND! Please enter the CORRECT words file path: ")
    word_index = int(input("Please enter the wanted word index in the file: ")) # number of the index as integer
    word = choose_word(file_location, word_index)
    print("Let's start!")
    print_hangman(tries)
    print("_ " * len(word) + '\n')
    return word


def print_hangman(num_of_tries):
    """
    Prints the hangman stage according to the wrong number of tries the user has entered
    :param num_of_tries:        the number of tries
    :type num_of_tries:         int
    :return:                    None - printing to screen only
    :rtype:                     null
    """
    print(HANGMAN_PHOTOS[str(num_of_tries)])


def is_valid_input(letter_guessed):
    """
    Checks if the input letter is a valid letter
    :param letter_guessed:      the letter the user has entered
    :type letter_guessed:       string
    :return:                    the answer if the letter is valid or not for the game
    :rtype:                     boolean
    """
    if len(letter_guessed) > 1 and not letter_guessed.isalpha():
        return False
    elif len(letter_guessed) > 1:
        return False
    elif not letter_guessed.isalpha():
        return False
    else:
        return True


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    Checks if the input letter is a valid letter an if it's not in the old letter which were already guessed by the user
    :param letter_guessed:      the letter the user has entered
    :param old_letters_guessed: the list of letters the user has already entered
    :type letter_guessed:       string
    :type old_letters_guessed:  list
    :return:                    the answer if the letter is valid or not for the game
                                and if it was not already entered by the user
    :rtype:                     boolean
    """
    if len(letter_guessed) > 1 and not letter_guessed.isalpha():
        return False
    elif len(letter_guessed) > 1:
        return False
    elif not letter_guessed.isalpha():
        return False
    elif letter_guessed in old_letters_guessed:
        return False
    else:
        return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Updating the letter which the user has tries according to the validation of the letter to the chosen word
    :param letter_guessed:      the letter the user has entered
    :param old_letters_guessed: the list of letters the user has already entered
    :type letter_guessed:       string
    :type old_letters_guessed:  list
    :return:                    if the letter is valid > adding to the old letters guessed and return True,
                                otherwise, prints X and the letters which were already guessed and return False
    :rtype:                     boolean
    """
    sep = ' -> '
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed += letter_guessed
        return True
    else:
        print('X')
        if is_valid_input(letter_guessed):
            print(sep.join(old_letters_guessed))
        return False


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Building the hidden word format using _ and letters according to the guessed letters
    :param secret_word:         the word the user need to guess
    :param old_letters_guessed: the list of letters the user has already entered
    :type secret_word:          string
    :type old_letters_guessed:  list
    :return:                    the hidden word string built by letters guessed and _
    :rtype:                     string
    """
    word_str = ''
    for i in range(0, len(secret_word)):
        if secret_word[i] in old_letters_guessed:
            word_str += secret_word[i] + ' '
        elif secret_word[i] not in old_letters_guessed:
            word_str += '_ '
    return word_str


def check_win(secret_word, old_letters_guessed):
    """
    Checks if the word was guessed correctly and fully
    :param secret_word:         the word the user need to guess
    :param old_letters_guessed: the list of letters the user has already entered
    :type secret_word:          string
    :type old_letters_guessed:  list
    :return:                    returns True if the user has guessed the hidden word fully and successfully,
                                and False if the user did not guessed the hidden word fully
    :rtype:                     boolean
    """
    word = show_hidden_word(secret_word, old_letters_guessed)
    return word.count('_') == 0


def choose_word(file_path, index):
    """
    Choosing a word to be the hidden word out of the file the user had entered and index of the word according to the
    index the user entered
    :param file_path:           the path of the TXT file of words
    :param index:               the index of the word in the TXT file
    :type file_path:            string
    :type index:                int
    :return:                    returns the count of different words without duplicates in the file (cell index 0 in
                                tuple) and the hidden word according to the index the user entered by looping cycle of
                                indexing  (cell index 1 in tuple)
    :rtype:                     tuple
    """
    location = index - 1
    file = open(file_path, 'r')
    text = file.read()
    words = text.replace("\n", " ").replace(",", "").split(" ") # splitting the text into list of words
    count_words = []
    for item in words:
        if item not in count_words:
            count_words.append(item)
    file.close()
    return words[location % len(words)]


def clear_and_logo():
    """
    Clears the screen and print the game logo and amount of allowed tries
    :return:                    NONE
    :rtype:                     null
    """
    cls = lambda: os.system('cls')
    cls()
    print(HANGMAN_ASCII_ART, "\nAmount of allowed tries:", MAX_TRIES)


if __name__ == "__main__":
    main()
