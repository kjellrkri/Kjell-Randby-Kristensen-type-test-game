"""
Type Test.

Author: Kjell Randby kristensen - student.nr:202894.
Last edited: 12/11/2020.
"""

import pygame
import datetime
import json
import random
import statistics
# importing Type Test modules
from assets.modules.type_test_module import get_word_list, get_pb_score, get_mean_score
# importing colors
from assets.colors.colors import BLACK, RED, WHITE, GRAY
# importing fonts
from assets.fonts.fonts import BASE_FONT, DIGITAL_CLOCK_FONT
# importing images
from assets.img.images import IMAGE_BG, ESC, F9, F12, TAB, DELETE
from assets.img.images import CTRL_BACKSPACE, NO_MOUSE_ALLOWED, INFO, F3, MUTE, UNMUTE
# import sounds
from assets.sounds.sounds import BEEP, WOOSH, COMMIT, FINISH


# This removes a faulty type warning from pycharm concerning
# (expected type int, got type float) in draw_text and display_img methods:
# noinspection PyTypeChecker


class Game:
    """Class representing typing game."""

    def __init__(self):
        # states
        self.type_test = False
        self.counting_down = False
        self.info = False
        self.menu = False
        self.results = False
        self.high_scores = False
        self.high_scores_by_user = False
        self.sound_muted = False
        # screen
        self.w = 1000
        self.h = 500
        self.screen = pygame.display.set_mode((self.w, self.h))
        # clock that can accurately measure out time
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.time_start = 0
        self.total_time = 0
        # typing test
        self.word_list = get_word_list()
        self.word = ''
        self.sentence = []
        self.word_index = 0
        self.input_text = ''
        self.misspelling = False
        # result calculation
        self.wpm = 0
        self.AVERAGE_WORD_LEN = 4.7
        # user high scores
        self.username = None
        self.user_high_score_list = []
        self.user_games_played = ''
        self.user_pb_wpm = ''
        self.user_mean_wpm = ''
        self.user_pb_time = ''
        self.user_mean_time = ''
        # high scores
        self.high_score_content = None
        self.high_score_list = None

    # initializing pygame
    pygame.init()

    # declaring title bar
    pygame.display.set_caption('Type Test')
    pygame.display.set_icon(pygame.image.load("assets\\img\\icon.png"))

    # ============= Menu methods: =================

    def display_menu(self):
        pygame.mixer.stop()  # stop all sounds
        self.play_sound(WOOSH)  # play switching page sound

        # menu loop
        self.update_state(menu_state=True)
        while self.menu:
            # display background
            self.display_img(IMAGE_BG)

            # draw header "Type Test"
            self.draw_text("Type Test", self.w / 2, 50, BLACK, None, 50, rect_alignment="center")

            # display no mouse allowed icon
            self.display_img(NO_MOUSE_ALLOWED, self.w / 2, self.h / 2, rect_alignment="center")

            # display info action and f12 image
            self.display_img(F12, self.w * 0.05, self.h * 0.05)
            self.draw_text("Info", self.w * 0.125, self.h * 0.05, GRAY, font_size=40)

            # display play action and tab image
            self.display_img(TAB, self.w * 0.05, self.h * 0.5)
            self.draw_text("play", self.w * 0.135, self.h * 0.5, GRAY, font_size=40)

            # display high score action and delete image
            self.display_img(DELETE, self.w * 0.05, self.h * 0.65)
            self.draw_text("High Scores", self.w * 0.185, self.h * 0.65, GRAY, font_size=40)

            # display high scores by username action and f9 image
            self.display_img(F9, self.w * 0.05, self.h * 0.8)
            self.draw_text("High Scores By Username", self.w * 0.125, self.h * 0.8, GRAY, font_size=40)

            # display f3 mute/unmute action
            self.display_img(F3, self.w * 0.85, self.h * 0.8)
            self.display_mute()

            # events:
            self.events()

            pygame.display.update()  # update the screen

    # ============= Info methods: =================
    def display_info(self):
        pygame.mixer.stop()  # stop all sounds
        self.play_sound(WOOSH)  # play switching page sound

        # info loop
        self.update_state(info_state=True)
        while self.info:
            # display background
            self.display_img(IMAGE_BG)

            # display menu action and esc image
            self.display_img(ESC, self.w * 0.05, self.h * 0.05)
            self.draw_text("Menu", self.w * 0.125, self.h * 0.05, GRAY, font_size=40)

            # display info about the game
            self.display_img(INFO, self.w / 2, self.h * 0.55, rect_alignment="center")

            # events:
            self.events()

            pygame.display.update()  # update the screen

    # ============= High scores methods: =================

    def display_high_scores(self):
        pygame.mixer.stop()  # stop all sounds
        self.play_sound(WOOSH)  # play switching page sound

        """Display high_scores."""
        # high scores loop
        self.update_state(high_scores_state=True)
        while self.high_scores:

            # display background
            self.display_img(IMAGE_BG)

            # display menu action and esc image
            self.display_img(ESC, self.w * 0.05, self.h * 0.05)
            self.draw_text("Menu", self.w * 0.125, self.h * 0.05, GRAY, font_size=40)

            # display mute/unmute symbol
            self.display_mute()

            try:
                # fetch data from json file
                self.high_score_list = []
                with open("assets/json\\high_scores.json", "r") as f:
                    self.high_score_content = json.load(f)

                # sort high scores from highest to lowest score
                self.high_score_content["high_scores"].sort(key=lambda score_x: score_x['wpm'], reverse=True)
                # formatting the high scores onto a list
                for item in self.high_score_content["high_scores"]:
                    self.high_score_list.append(
                        f"{item['wpm']} - {datetime.timedelta(seconds=item['time'])} - {item['username']}")

                # displaying top 10 high scores titles
                self.draw_text(
                    "WPM   TIME     USERNAME",
                    self.w / 2,
                    self.h * 0.1,
                    RED,
                    font_size=20,
                    rect_alignment="center"
                )

                # display top 10 high scores
                y = self.h * 0.08
                high_score_index = 0

                for score in self.high_score_list:
                    if high_score_index < 10:
                        y += self.h * 0.065
                        self.draw_text(score, self.w * 0.38, y, font_size=20)
                        high_score_index += 1

                # get and display mean wpm
                mean_wpm = round(self.get_mean_score_json('wpm'), 1)
                self.draw_text(f"MEAN WPM: {mean_wpm}", self.w * 0.38, self.h * 0.83, RED, font_size=20)

                # get and display mean time
                mean_time = datetime.timedelta(seconds=round(self.get_mean_score_json('time')))
                self.draw_text(f"MEAN TIME: {mean_time}", self.w * 0.38, self.h * 0.9, RED, font_size=20)
            except FileNotFoundError:
                # displaying message if no high scores are stored
                self.draw_text(
                    "There are not yet any high scores",
                    self.w / 2,
                    50,
                    RED,
                    font_size=20,
                    rect_alignment="center"
                )

            # events:
            self.events()
            pygame.display.update()  # update the screen

    def get_mean_score_json(self, keyword):
        """
        Return mean score for keyword in high_scores.json file.

        This function needs to run after a function has updated self.high_score_content

        :param keyword: keyword to the high score we want to use,
        takes a string that represents a keyword in high_scores.json
        :return: mean score
        """
        mean_score_list = []
        for score in self.high_score_content["high_scores"]:
            mean_score_list.append(score[keyword])
        mean_score = (statistics.mean(mean_score_list))
        return mean_score

    # ============= high scores by user methods: =================
    def display_high_score_user(self):
        """Display high_scores."""
        pygame.mixer.stop()  # stop all sounds
        self.play_sound(WOOSH)  # play switching page sound

        self.input_text = ''  # reset input text
        self.reset("user")  # reset user

        # fetch data from json file
        try:
            self.high_score_list = []
            with open("assets/json\\high_scores.json", "r") as f:
                self.high_score_content = json.load(f)
        # if no high scores, send user to high scores, to see message
        except FileNotFoundError:
            self.display_high_scores()

        # high scores by user loop
        self.update_state(high_scores_by_user_state=True)
        while self.high_scores_by_user:
            # display background
            self.display_img(IMAGE_BG)

            # display menu action and esc image
            self.display_img(ESC, self.w * 0.05, self.h * 0.05)
            self.draw_text("Menu", self.w * 0.125, self.h * 0.05, GRAY, font_size=40)

            # display delete word action and ctrl + backspace image
            self.display_img(CTRL_BACKSPACE, self.w * 0.05, self.h * 0.8)
            self.draw_text("Delete Word", self.w * 0.298, self.h * 0.8, GRAY, font_size=40)

            # display mute/unmute symbol
            self.display_mute()

            # displaying username input
            self.draw_text(f'Enter username: {self.input_text}', self.w * 0.39, self.h * 0.1, RED)

            # fetching high scores by username and calculating statistics -> see events: fetch user

            # displaying high scores by username
            self.draw_text(f"Games played: {self.user_games_played}", self.w * 0.39, self.h * 0.25)
            self.draw_text(f"Best WPM: {self.user_pb_wpm}", self.w * 0.39, self.h * 0.35)
            self.draw_text(f"Mean WPM: {self.user_mean_wpm}", self.w * 0.39, self.h * 0.45)
            self.draw_text(f"Best TIME: {self.user_pb_time}", self.w * 0.39, self.h * 0.55)
            self.draw_text(f"Mean TIME: {self.user_mean_time}", self.w * 0.39, self.h * 0.65)

            # events:
            self.events(
                backspace=True,
                ctrl_backspace=True,
                fetch_user=True,
                letters=True
            )

            pygame.display.update()  # update the screen

    def get_high_score_stats_user(self):
        """Get high score stats by username."""
        # resetting user
        self.reset("user")

        # get high scores relating to username and append to list
        for score in self.high_score_content["high_scores"]:
            if score["username"] == self.username:
                self.user_high_score_list.append(score)

        if self.user_high_score_list:
            # update number of games user has played
            self.user_games_played = len(self.user_high_score_list)

            # update the personal best wpm and mean wpm high scores
            self.user_pb_wpm = get_pb_score(self.user_high_score_list, "wpm")
            self.user_mean_wpm = get_mean_score(self.user_high_score_list, "wpm")

            # update the the personal best time and mean time high scores
            self.user_pb_time = datetime.timedelta(seconds=get_pb_score(self.user_high_score_list, "time", min))
            self.user_mean_time = datetime.timedelta(seconds=round(get_mean_score(self.user_high_score_list, "time")))

        else:
            # displaying message if username does not exist
            self.input_text = 'username does not exist'

    # ============= running game methods: =================
    def run_type_test(self):
        """Run the type test."""
        self.reset("game")  # resetting the game
        self.time_start = pygame.time.get_ticks()  # Start the timer

        # type test loop
        self.update_state(type_test_state=True)
        while self.type_test:

            # display background
            self.display_img(IMAGE_BG)

            # display reset action and tab image
            self.display_img(TAB, self.w * 0.05, self.h * 0.65)
            self.draw_text("Reset", self.w * 0.135, self.h * 0.65, GRAY, font_size=40)

            # display delete word action and ctrl + backspace image
            self.display_img(CTRL_BACKSPACE, self.w * 0.05, self.h * 0.8)
            self.draw_text("Delete Word", self.w * 0.298, self.h * 0.8, GRAY, font_size=40)

            # display mute/unmute symbol
            self.display_mute()

            # update the time
            self.current_time = pygame.time.get_ticks()
            self.total_time = round((self.current_time - self.time_start) / 1000)
            # draw the time
            self.draw_text(
                str(datetime.timedelta(seconds=self.total_time)),
                435,
                50,
                RED,
                None,
                50,
                DIGITAL_CLOCK_FONT
            )

            # update the word
            if self.word_index < 10:
                self.word = self.sentence[self.word_index]
            else:
                self.word = ''
            # draw word to screen
            self.draw_text(self.word, 435, 200)

            # check for misspelling
            self.check_misspelling()
            # update/draw the text of user input
            if self.misspelling:
                self.draw_text(self.input_text, 435, 250, RED)
            else:
                self.draw_text(self.input_text, 435, 250)
            pygame.display.update()  # update the screen

            # events:
            self.events(
                backspace=True,
                ctrl_backspace=True,
                commit_word=True,
                letters=True
            )

            # show results
            if self.word_index == 10:
                self.display_results()

            pygame.display.update()  # update the screen

        self.clock.tick(60)  # count the time at 60 frames per second

    def countdown(self):
        """3 second count down."""
        pygame.mixer.stop()  # stop all sounds
        self.play_sound(BEEP)  # play starting sound
        self.time_start = pygame.time.get_ticks()  # Start the timer

        # countdown loop
        self.update_state(countdown_state=True)
        while self.counting_down:
            # display background
            self.display_img(IMAGE_BG)

            # display mute/unmute symbol
            self.display_mute()

            # display "Test starts in:"
            self.draw_text(
                "GET READY",
                self.w / 2,
                self.h * 0.15,
                RED,
                None,
                100,
                rect_alignment="center"
            )

            # update the time
            self.current_time = pygame.time.get_ticks()
            # counting time in reverse from 3
            self.total_time = 3 - round((self.current_time - self.time_start) / 1000)

            # draw the time if time is less than 3 seconds, run the type test if time is greater than 3 seconds
            self.draw_text(
                str(self.total_time),
                self.w / 2,
                self.h / 2,
                RED,
                None,
                300,
                DIGITAL_CLOCK_FONT,
                rect_alignment="center"
            )

            # start test if time is <= 0
            if self.total_time < 0:
                self.run_type_test()

            # events
            self.events()

            pygame.display.update()  # update the screen
        self.clock.tick(60)  # count the time at 60 frames per second

    def get_sentence(self):
        """
        Create a random sentence formatted as a list of 10 words.

        :return: list of 10 words
        """
        random_list = []
        for _ in range(10):
            random_list.append(random.choice(self.word_list))
        return random_list

    def check_misspelling(self):
        """Check if text input is misspelled."""
        zip_input_text = ''
        zip_word = ''
        for input_letter, word_letter in zip(self.input_text, self.word):
            zip_input_text += input_letter
            zip_word += word_letter
        if zip_input_text == zip_word:
            self.misspelling = False
        elif zip_input_text != zip_word:
            self.misspelling = True
        if len(self.input_text) > len(self.word):
            self.misspelling = True

    def display_results(self):
        """Show result of typing test."""
        self.type_test = False  # stop the type test

        pygame.mixer.stop()  # stop all sounds
        self.play_sound(FINISH)  # play finish sound

        # calculate number of letters in sentence
        sentence_length = 0
        for w in self.sentence:
            sentence_length += len(w)
        # calculate wpm
        self.wpm = round(((sentence_length / self.AVERAGE_WORD_LEN) / self.total_time) * 60, 1)

        # display result loop
        self.update_state(results_state=True)
        while self.results:
            # display background
            self.display_img(IMAGE_BG)

            # display mute/unmute symbol
            self.display_mute()

            # draw header 'RESULT'
            self.draw_text(
                'RESULT',
                int(self.w / 2),
                self.h * 0.1,
                background_color=None,
                font_size=40,
                rect_alignment="center"
            )

            # draw the wpm result
            self.draw_text(f"{str(self.wpm)} WPM", self.w / 2, self.h * 0.4, rect_alignment="center")

            # draw the time
            self.draw_text(
                f"Time: {str(datetime.timedelta(seconds=self.total_time))}",
                self.w / 2,
                self.h * 0.5,
                rect_alignment="center"
            )

            # draw input username
            self.draw_text(f'Enter username: {self.input_text}', self.w * 0.39, self.h * 0.21, RED)

            # events:
            self.events(
                backspace=True,
                ctrl_backspace=True,
                commit_username=True,
                letters=True
            )

            pygame.display.update()  # update the screen

    def store_result(self):
        """Store result in a json file."""
        user_data = {
            "username": self.username,
            "time": self.total_time,
            "wpm": self.wpm
        }
        try:
            # Loading the current json file and appending user data to key "high_scores"
            with open("assets/json\\high_scores.json", "r") as f:
                high_score_content = json.load(f)
                high_score_content["high_scores"].append(user_data)
            # Updating the json file with the new data
            with open("assets/json\\high_scores.json", "w") as f:
                json.dump(high_score_content, f, indent=2, ensure_ascii=False)
        # create a new json file and store results if file not found
        except FileNotFoundError:
            data = {"high_scores": []}
            data["high_scores"].append(user_data)
            with open('assets/json\\high_scores.json', "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    # ============= General methods: =================
    def events(
            self,
            quit_game=True,
            info=True,
            menu=True,
            mute_sound=True,
            high_score=True,
            high_score_by_user=True,
            play=True,
            backspace=False,
            ctrl_backspace=False,
            commit_word=False,
            letters=False,
            commit_username=False,
            fetch_user=False,
            quick_quit_game=True
    ):
        """
        Perform actions based on user events.

        :param quit_game: enable user to quit the game, takes a bool
        :param info: enable user to go to info page, takes a bool
        :param menu: enable user to go to menu, takes a bool
        :param mute_sound: enables user to mute the game sound, takes a bool
        :param high_score: enable user to go to view high scores, takes a bool
        :param high_score_by_user: enable user to view high scores by user, takes a bool
        :param play: enable user to start/restart game, takes a bool
        :param backspace: enable user to delete a letter, takes a bool
        :param ctrl_backspace: enable user to delete entire word, takes a bool
        :param commit_word: enable user to get next word if no spelling mistakes, takes a bool
        :param commit_username: enable user to commit username, takes any bool
        :param fetch_user: enable user to fetch high scores based on username, takes any bool
        :param letters: enable user to type normal letters, takes a bool
        :param quick_quit_game: enable user to quit the game with shortcut, takes a bool
        """
        for event in pygame.event.get():
            # quit game (x)
            if event.type == pygame.QUIT:
                if quit_game:
                    self.update_state()
            elif event.type == pygame.KEYDOWN:
                # show info page (F12)
                if event.key == pygame.K_F12:
                    if info:
                        self.display_info()
                # show menu (esc)
                elif event.key == pygame.K_ESCAPE:
                    if menu:
                        self.display_menu()
                # show high_scores (delete)
                elif event.key == pygame.K_DELETE:
                    if high_score:
                        self.display_high_scores()
                # show high scores by user (F9)
                elif event.key == pygame.K_F9:
                    if high_score_by_user:
                        self.display_high_score_user()
                # Mute/unmute sound
                elif event.key == pygame.K_F3:
                    if mute_sound:
                        pygame.mixer.stop()  # stop all sounds
                        if self.sound_muted:
                            self.sound_muted = False
                        else:
                            self.sound_muted = True
                # restart type test (tab)
                elif event.key == pygame.K_TAB:
                    if play:
                        self.countdown()  # start countdown
                # erase letter (backspace)
                elif event.key == pygame.K_BACKSPACE:
                    if backspace:
                        self.input_text = self.input_text[: -1]
                # commit (space or return)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # get next word if no spelling mistakes
                    if commit_word:
                        if self.misspelling:
                            continue
                        else:
                            if self.input_text == self.word:
                                self.play_sound(COMMIT)  # play commit sound
                                self.input_text = ''
                                self.word_index += 1
                    # commit username if given, store results and display high scores
                    if commit_username:
                        if not self.input_text:
                            self.username = 'anonymous'
                        else:
                            self.username = self.input_text
                        self.store_result()
                        self.display_high_scores()
                    # fetch high scores by username
                    if fetch_user:
                        self.play_sound(COMMIT)  # play commit sound
                        # updating self.username
                        self.username = self.input_text
                        # calculate high scores by user
                        self.get_high_score_stats_user()
                # normal text (letter and number keys)
                else:
                    if letters:
                        self.input_text += event.unicode
        # multi keypress events
        keys = pygame.key.get_pressed()  # returns a list of keys which are currently down.
        # erase entire word (left-ctrl + backspace)
        if ctrl_backspace:
            if keys[pygame.K_BACKSPACE] and keys[pygame.K_LCTRL]:
                self.input_text = ''
        # quick quit game (right-ctrl + esc)
        if quick_quit_game:
            if keys[pygame.K_RSHIFT] and keys[pygame.K_F5]:
                self.update_state()

    def reset(self, reset_type):
        """
        Reset variables

        :param reset_type: denotes what we want to reset, takes either "game" or "user"
        """

        # reset the game
        if reset_type == "game":
            # get sentence
            self.sentence = self.get_sentence()

            # reset variables
            self.misspelling = False
            self.input_text = ''
            self.word_index = 0
            self.current_time = 0
            self.time_start = 0
            self.wpm = 0

        # reset user
        if reset_type == "user":
            self.user_high_score_list = []
            self.user_games_played = ''
            self.user_pb_wpm = ''
            self.user_mean_wpm = ''
            self.user_pb_time = ''
            self.user_mean_time = ''

    def update_state(
            self,
            type_test_state=False,
            countdown_state=False,
            results_state=False,
            menu_state=False,
            info_state=False,
            high_scores_state=False,
            high_scores_by_user_state=False
    ):
        """
        Update game state.

        :param type_test_state: updates the type test state, takes a bool
        :param results_state: updates the displaying results state, takes a bool
        :param menu_state: updates the menu state, takes a bool
        :param info_state: updates the info state, takes a bool
        :param high_scores_state: updates the high scores state, takes a bool
        :param high_scores_by_user_state: updates the high scores by user state, takes a bool
        :param countdown_state: updates the countdown_state, takes a bool
        """

        # update type test state
        if type_test_state:
            self.type_test = True
        else:
            self.type_test = False
        # update countdown state
        if countdown_state:
            self.counting_down = True
        else:
            self.counting_down = False
        # update results state
        if results_state:
            self.results = True
        else:
            self.results = False
        # update menu state
        if menu_state:
            self.menu = True
        else:
            self.menu = False
        # update info state
        if info_state:
            self.info = True
        else:
            self.info = False
        # update high score state
        if high_scores_state:
            self.high_scores = True
        else:
            self.high_scores = False
        # update high score by user state
        if high_scores_by_user_state:
            self.high_scores_by_user = True
        else:
            self.high_scores_by_user = False

    def draw_text(
            self,
            message='',
            x=0,
            y=0,
            text_color=BLACK,
            background_color=WHITE,
            font_size=30,
            font_style=BASE_FONT,
            rect_alignment="topleft"
    ):
        """
        Draw text to screen.

        :param message: the text we want to display, takes any string
        :param x: x-axis position, takes int or float
        :param y: y-axis position, takes int or float
        :param text_color: color of text, takes any rgb value in the form of a tuple
        :param background_color: color of rect/background, takes any rgb value in the form of a tuple
        :param font_size: font size of text, takes any number
        :param font_style: style of the font, takes a path to a .ttf file
        :param rect_alignment: denotes the alignment of rect, takes center or topleft
        """
        position = (int(x), int(y))  # making sure the position is an integer
        font = pygame.font.Font(font_style, font_size)
        text = font.render(message, True, text_color, background_color)
        text_rect = text.get_rect()
        if rect_alignment == "center":
            text_rect.center = position
        if rect_alignment == "topleft":
            text_rect.topleft = position
        self.screen.blit(text, text_rect)

    def display_img(self, file, x=0, y=0, rect_alignment='topleft'):
        """
        Blit image to screen at position.

        :param file: the file of the image, takes a filepath string to an image
        :param x: x-axis position, takes int or float
        :param y: y-axis position, takes int or float
        :param rect_alignment: denotes the alignment of rect, takes center or topleft
        """
        position = (int(x), int(y))  # making sure the position is an integer
        image = pygame.image.load(file)  # load the image
        image.convert()  # optimizes the image format and makes drawing faster
        image_rect = image.get_rect()  # get rect of image
        # set the alignment of the rect
        if rect_alignment == 'topleft':
            image_rect.topleft = position
        elif rect_alignment == 'center':
            image_rect.center = position
        self.screen.blit(image, image_rect)  # blit image to screen

    def play_sound(self, sound_file):
        """
        Play sound if self.sound_muted == False.

        :param sound_file: the sound we want to play, takes any .vaw file
        """
        sound = pygame.mixer.Sound(sound_file)
        if not self.sound_muted:
            sound.play()

    def display_mute(self):
        """display mute/unmute symbol"""
        if self.sound_muted:
            self.display_img(MUTE, self.w * 0.92, self.h * 0.825)
        else:
            self.display_img(UNMUTE, self.w * 0.92, self.h * 0.825)


g = Game()  # declaring instance of class Game
g.display_menu()  # calling method that displays game menu
