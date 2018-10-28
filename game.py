"""Wikipedia Bingo code."""

import sys
from collections import Counter

import numpy as np
import pandas as pd

import pygame
import pygame.locals as loc

from pygame_textinput import TextInput

from validate_numbers import Validation

from word_generation import TargetWord, get_word_list


# Create the constants (go ahead and experiment with different values)
BOARDSIZE = 5
TILESIZE = 80
TILE_WIDTH = 200
TILE_HEIGHT = 80
WINDOWWIDTH = 1920
WINDOWHEIGHT = 800
FPS = 30
BLANK = None

# Colours (R, G, B)
BLACK = (78, 0, 105)
WHITE = (255, 255, 255)
LIGHTBLUE = (207, 228, 255)
GREEN = (117, 213, 148)

BGCOLOR = LIGHTBLUE
TILECOLOR = GREEN
TEXTCOLOR = BLACK
BORDERCOLOR = BLACK
BUTTONCOLOR = BLACK
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = BLACK

BASICFONTSIZE = 20
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

ALL_WORDS = get_word_list('no_stop_g2.txt')


def make_text(text, color, bgcolor, top, left):
    """Create the Surface and Rect objects for some text."""
    surface = BASICFONT.render(text, True, color, bgcolor)
    rect = surface.get_rect()
    rect.topleft = (top, left)
    return (surface, rect)


class Button(object):
    """A button object."""

    def __init__(self, text, text_color, back_color, x, y):
        self.surface, self.rect = make_text(text, text_color, back_color, x, y)


class Game(object):
    """The game instance."""

    def __init__(self):
        # Create the clock
        self.clock = pygame.time.Clock()

        # Create the game window
        self.window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Wikipedia Bingo')

        # Default game options (changed on start screen)
        self.limit = 5
        self.board_size = 5

    def run(self):
        """Run the game until it quits."""
        self.running = True
        while self.running:
            # Display the start screen
            self.start_screen()
            # Start screen quit

            # Display the main screen
            self.main_screen()
            # Main screen quit

        # Exit
        self.terminate()

    def start_screen(self):
        """Create the start screen."""
        self.loop_stage = True

        # Define buttons
        self.buttons = {}
        # Options
        self.buttons['start'] = Button('START',
                                       TEXTCOLOR, TILECOLOR,
                                       WINDOWWIDTH / 2 - 100, WINDOWHEIGHT - 100)
        self.buttons['start'].action = self.next_stage

        self.buttons['quit'] = Button('QUIT',
                                      TEXTCOLOR, TILECOLOR,
                                      WINDOWWIDTH / 2 + 50, WINDOWHEIGHT - 100)
        self.buttons['quit'].action = self.terminate

        # Difficulty
        self.buttons['limit3'] = Button('Hard',
                                        TEXTCOLOR, TILECOLOR,
                                        WINDOWWIDTH / 2 + 150, WINDOWHEIGHT - 300)
        self.buttons['limit3'].action = self.set_limit_to_3
        self.buttons['limit3_sel'] = Button('Hard',
                                            TEXTCOLOR, WHITE,
                                            WINDOWWIDTH / 2 + 150, WINDOWHEIGHT - 300)
        self.buttons['limit3_sel'].action = self.set_limit_to_3

        self.buttons['limit5'] = Button('Medium',
                                        TEXTCOLOR, TILECOLOR,
                                        WINDOWWIDTH / 2, WINDOWHEIGHT - 300)
        self.buttons['limit5'].action = self.set_limit_to_5
        self.buttons['limit5_sel'] = Button('Medium',
                                            TEXTCOLOR, WHITE,
                                            WINDOWWIDTH / 2, WINDOWHEIGHT - 300)
        self.buttons['limit5_sel'].action = self.set_limit_to_5

        self.buttons['limit7'] = Button('Easy',
                                        TEXTCOLOR, TILECOLOR,
                                        WINDOWWIDTH / 2 - 150, WINDOWHEIGHT - 300)
        self.buttons['limit7'].action = self.set_limit_to_7
        self.buttons['limit7_sel'] = Button('Easy',
                                            TEXTCOLOR, WHITE,
                                            WINDOWWIDTH / 2 - 150, WINDOWHEIGHT - 300)
        self.buttons['limit7_sel'].action = self.set_limit_to_7

        # Board size
        self.buttons['3x3'] = Button('3x3',
                                     TEXTCOLOR, TILECOLOR,
                                     WINDOWWIDTH / 2 - 150, WINDOWHEIGHT - 200)
        self.buttons['3x3'].action = self.set_board_size_to_3x3
        self.buttons['3x3_sel'] = Button('3x3',
                                         TEXTCOLOR, WHITE,
                                         WINDOWWIDTH / 2 - 150, WINDOWHEIGHT - 200)
        self.buttons['3x3_sel'].action = self.set_board_size_to_3x3

        self.buttons['5x5'] = Button('5x5',
                                     TEXTCOLOR, TILECOLOR,
                                     WINDOWWIDTH / 2, WINDOWHEIGHT - 200)
        self.buttons['5x5'].action = self.set_board_size_to_5x5
        self.buttons['5x5_sel'] = Button('5x5',
                                         TEXTCOLOR, WHITE,
                                         WINDOWWIDTH / 2, WINDOWHEIGHT - 200)
        self.buttons['5x5_sel'].action = self.set_board_size_to_5x5

        self.buttons['7x7'] = Button('7x7',
                                     TEXTCOLOR, TILECOLOR,
                                     WINDOWWIDTH / 2 + 150, WINDOWHEIGHT - 200)
        self.buttons['7x7'].action = self.set_board_size_to_7x7
        self.buttons['7x7_sel'] = Button('7x7',
                                         TEXTCOLOR, WHITE,
                                         WINDOWWIDTH / 2 + 150, WINDOWHEIGHT - 200)
        self.buttons['7x7_sel'].action = self.set_board_size_to_7x7

        while self.loop_stage:
            # Get events
            events = pygame.event.get()

            # Check clicks
            for event in events:
                if event.type == loc.MOUSEBUTTONUP:
                    # check if the user clicked on an option button
                    for button_name in self.buttons:
                        button = self.buttons[button_name]
                        if button.rect.collidepoint(event.pos):
                            button.action()

            # Check for exit
            self.check_for_quit(events)

            # Draw the board
            self.draw_start_screen()

            # Tick the FPS clock
            self.clock.tick(FPS)

    def draw_start_screen(self):
        """Draw the start screen."""
        self.window.fill(BGCOLOR)
        # Draw the name
        txt = 'Wikipedia Bingo!'
        surf, rect = make_text(txt, MESSAGECOLOR, BGCOLOR, 500, 60)
        self.window.blit(surf, rect)

        # Draw the button text
        txt = 'Chose board size:'
        surf, rect = make_text(txt, MESSAGECOLOR, BGCOLOR, 870, WINDOWHEIGHT - 240)
        self.window.blit(surf, rect)
        txt = 'Chose difficulty:'
        surf, rect = make_text(txt, MESSAGECOLOR, BGCOLOR, 870, WINDOWHEIGHT - 340)
        self.window.blit(surf, rect)

        # Draw the buttons
        for button_name in self.buttons:
            button = self.buttons[button_name]
            # Size pressed
            if self.board_size == 3 and button_name in ['3x3', '5x5_sel', '7x7_sel']:
                continue
            elif self.board_size == 5 and button_name in ['3x3_sel', '5x5', '7x7_sel']:
                continue
            elif self.board_size == 7 and button_name in ['3x3_sel', '5x5_sel', '7x7']:
                continue
            # Limit button pressed
            elif self.limit == 3 and button_name in ['limit3', 'limit5_sel', 'limit7_sel']:
                continue
            elif self.limit == 5 and button_name in ['limit3_sel', 'limit5', 'limit7_sel']:
                continue
            elif self.limit == 7 and button_name in ['limit3_sel', 'limit5_sel', 'limit7']:
                continue
            else:
                self.window.blit(button.surface, button.rect)

        # Update the dipslay
        pygame.display.update()

    def main_screen(self):
        """Create the main screen."""
        self.loop_stage = True

        # Default user name
        self.name = None

        # Generate a new puzzle
        self.get_starting_board()

        # Create list of red tiles
        self.board_counts = np.zeros((self.board_size, self.board_size))

        # Quit button
        self.buttons = {}
        self.buttons['restart'] = Button('RESTART', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 150, 30)
        self.buttons['restart'].action = self.next_stage
        self.buttons['quit'] = Button('QUIT', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 150, 60)
        self.buttons['quit'].action = self.terminate

        # Create TextInput-object
        self.textinput = TextInput(text_color=TEXTCOLOR, cursor_color=TEXTCOLOR)

        # Create the message array (starts blank)
        self.message_array = None

        # Initial score.
        self.score = 0

        # Draw the initial board
        self.draw_main_screen()

        while self.loop_stage:
            # Get events
            events = pygame.event.get()

            # Check clicks
            for event in events:
                if event.type == loc.MOUSEBUTTONUP:
                    # check if the user clicked on an option button
                    for button_name in self.buttons:
                        button = self.buttons[button_name]
                        if button.rect.collidepoint(event.pos):
                            button.action()

            # Send events to the text reader
            if self.textinput.update(events):
                # Pressed enter
                user_input = self.textinput.get_text()
                self.textinput.clear_text()

                # Extra commands
                if user_input and user_input[0] == "\ "[0]:
                    command = user_input[1:].lower()
                    if command in ['q', 'quit']:
                        self.terminate()
                    if command == 'add':
                        self.board_counts += 1
                else:
                    # DEBUG
                    print(self.board_words)

                    # Put the title in the top left
                    self.message_array = [user_input + ':']

                    if not self.game_won():
                        # Get the wikipedia article
                        validation = Validation(user_input)
                        try:
                            validation.scrape_wiki()
                            validation.process_wiki()
                            words = validation.token
                            self.score += 1
                            print(self.score)
                        except Exception:
                            self.message_array.append('Article not found')
                            words = []
                            self.score += 1
                            print(self.score)

                        # Remove any words not on the board
                        words = [word.lower()
                                for word in words
                                if word.lower() in self.board_words.flatten()]

                        # Count the frequencies
                        counter = Counter(words)

                        # Create the message for the top left
                        if len(words) == 0:
                            self.message_array.append('No valid words')

                        for word in sorted(counter, key=lambda x: counter[x], reverse=True):
                            x, y = tuple(np.argwhere(self.board_words == word.lower())[0])
                            current_count = self.board_counts[x][y]
                            limit = self.board_limits[x][y]
                            new_count = current_count + counter[word]

                            # Create the message array for the left hand courner
                            message = '{} ({:.0f})+{:.0f} = {:.0f}/{:.0f}'.format(word,
                                                                                current_count,
                                                                                counter[word],
                                                                                new_count,
                                                                                limit)
                            self.message_array.append(message)

                            # Check if the counter has overflowed
                            new_word = None
                            new_range = None
                            if new_count >= limit:
                                new_count = 0
                                new_word, new_range = self.get_new_word()
                                self.message_array.append('  OVERFLOW > {}'.format(new_word))

                            # Save the new count, new word (if needed) and message
                            self.board_counts[x][y] = new_count
                            if new_word:
                                print(new_word)
                                self.board_words[x][y] = new_word
                                self.board_limits[x][y] = new_range
                    else:
                        # You win!
                        if not self.name and len(user_input) > 0:
                            self.name = user_input
                            print(self.name)

                            # Update the leaderboard.
                            new_win = pd.DataFrame(columns=['score', 'name'])
                            new_win.loc[0] = [self.score, self.name]
                            leaderboard = pd.read_csv('leaderboard.csv')
                            new_leaderboard = pd.concat([leaderboard, new_win])
                            new_leaderboard = new_leaderboard.sort_values('score')
                            new_leaderboard.to_csv('leaderboard.csv', index=False)

                            return

            # Check for exit
            self.check_for_quit(events)

            # Draw the board
            self.draw_main_screen()

            # Tick the FPS clock
            self.clock.tick(FPS)

    def draw_main_screen(self):
        """Draw the main screen."""
        self.window.fill(BGCOLOR)
        # Draw the board
        for tilex in range(len(self.board_words)):
            for tiley in range(len(self.board_words[0])):
                word = self.board_words[tilex][tiley]
                count = self.board_counts[tilex][tiley]
                limit = self.board_limits[tilex][tiley]
                if 0 < count < limit:
                    colour = (255, 255 - count * 255 / limit, 255 - count * 255 / limit)
                else:
                    colour = GREEN
                self.draw_tile(tilex, tiley, word, count, limit, colour)

        left, top = self.get_tile_courner(0, 0)
        width = self.board_size * TILE_WIDTH
        height = self.board_size * TILE_HEIGHT
        pygame.draw.rect(self.window, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

        # Draw the score
        msg = 'SCORE: {:.0f}'.format(self.score)
        surf, rect = make_text(msg, MESSAGECOLOR, BGCOLOR, 5, 5)
        self.window.blit(surf, rect)

        # Draw the message
        if self.message_array:
            for i, msg in enumerate(self.message_array):
                textSurf, textRect = make_text(msg, MESSAGECOLOR, BGCOLOR, 5, 35 + 20 * i)
                self.window.blit(textSurf, textRect)

        # Draw the winning message if you've won
        if self.game_won():
            # Display winning message
            textSurf, textRect = make_text('!! WINNER !!',
                                           MESSAGECOLOR, BGCOLOR,
                                           WINDOWWIDTH / 2 - 75, 5)
            self.window.blit(textSurf, textRect)

        # Draw the instructions
        if not self.game_won():
            instruct = 'Enter the name of a Wikipedia article:'
            color = MESSAGECOLOR
            bgcolor = BGCOLOR
        else:
            instruct = 'Enter your name to add to the leaderboard:'
            color = WHITE
            bgcolor = (255, 0, 0)
        instructSurf, instructRect = make_text(instruct,
                                               color, bgcolor,
                                               5, WINDOWHEIGHT - 60)
        self.window.blit(instructSurf, instructRect)

        # Draw the text box
        self.window.blit(self.textinput.get_surface(), (5, WINDOWHEIGHT - 30))

        # Draw the buttons
        for button_name in self.buttons:
            button = self.buttons[button_name]
            self.window.blit(button.surface, button.rect)

        # Update the dipslay
        pygame.display.update()

    # # # # #  BUTTON FUNCTIONS
    def next_stage(self):
        """Go to the next stage."""
        self.loop_stage = False

    def terminate(self):
        """Quit the game."""
        pygame.quit()
        sys.exit()

    def set_board_size_to_3x3(self):
        """Set the board size."""
        self.board_size = 3

    def set_board_size_to_5x5(self):
        """Set the board size."""
        self.board_size = 5

    def set_board_size_to_7x7(self):
        """Set the board size."""
        self.board_size = 7

    def set_limit_to_3(self):
        """Set the tile limits."""
        self.limit = 3

    def set_limit_to_5(self):
        """Set the tile limits."""
        self.limit = 5

    def set_limit_to_7(self):
        """Set the tile limits."""
        self.limit = 7

    def check_for_quit(self, events):
        """Check for quit events."""
        for event in events:
            if event.type == loc.QUIT:
                # terminate if any QUIT events are present
                self.terminate()
            if event.type == loc.KEYUP and event.key == loc.K_ESCAPE:
                # terminate if the KEYUP event was for the Esc key
                self.terminate()

    def get_starting_board(self):
        """Return a board data structure with tiles in the solved state."""
        words = []
        ranges = []
        for _ in range(self.board_size * self.board_size):
            word, limit = self.get_new_word()
            words.append(word)
            ranges.append(limit)
        self.board_words = np.array(words, dtype=object).reshape((self.board_size, self.board_size))
        self.board_limits = np.array(ranges).reshape((self.board_size, self.board_size))

    def get_new_word(self):
        """Get an unused word from the list of all words."""
        while True:
            target = TargetWord(ALL_WORDS)
            target.word_gen()
            word = target.word.lower()
            target.range_gen()
            limit = self.limit

            try:
                if word not in self.board_words.flatten():
                    break
            except Exception:
                break

        return word, limit

    def get_tile_courner(self, tilex, tiley):
        """Get the coordinates of the top left courner of a tile."""
        xmargin = int((WINDOWWIDTH - (TILE_WIDTH * self.board_size + (self.board_size - 1))) / 2)
        ymargin = int((WINDOWHEIGHT - (TILE_HEIGHT * self.board_size + (self.board_size - 1))) / 2)
        left = xmargin + (tilex * TILE_WIDTH) + (tilex - 1)
        top = ymargin + (tiley * TILE_HEIGHT) + (tiley - 1)
        return (left, top)

    def draw_tile(self, tilex, tiley, word, count, limit, colour=TILECOLOR):
        """Draw a tile at board coordinates tilex and tiley."""
        left, top = self.get_tile_courner(tilex, tiley)
        pygame.draw.rect(self.window, colour, (left, top, TILE_WIDTH, TILE_HEIGHT))

        text_surf = BASICFONT.render(str(word), True, TEXTCOLOR)
        text_rect = text_surf.get_rect()
        text_rect.center = (left + int(TILE_WIDTH / 2), top + int(TILE_HEIGHT / 2))
        self.window.blit(text_surf, text_rect)

        count_surf = BASICFONT.render('{:.0f}/{:.0f}'.format(count, limit), True, TEXTCOLOR)
        count_rect = count_surf.get_rect()
        count_rect.center = (left + int(TILE_WIDTH / 2) + 75, top + int(TILE_HEIGHT / 2) + 20)
        self.window.blit(count_surf, count_rect)

    def game_won(self):
        """Determine if anyone has won the game."""
        won = False

        # check for winning rows
        for row in self.board_counts:
            if all(row > 0):
                won = True

        # check for winning columns
        for col in self.board_counts.T:
            if all(col > 0):
                won = True

        return won


def main():
    """Run the main process."""
    # Initilise PyGame
    pygame.init()

    # Create a game instance
    game = Game()

    # Run the game
    game.run()


if __name__ == '__main__':
    main()
