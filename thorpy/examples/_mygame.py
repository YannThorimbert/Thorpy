#ThorPy minigame tutorial. Guess the number : first version
import thorpy, pygame, random #pygame for wait() function, random for randint()

class MyGame(object):

    def __init__(self, player_name, min_val, max_val, trials):
        #init some parameters of the game ...
        self.player_name = player_name
        self.min_val = min_val #the minimum value to guess
        self.max_val = max_val #the maximum value to guess
        self.init_trials = trials #keep the original trials amount in memory
        self.trials = trials #remaining number of trials
        #the number to guess:
        self.number = random.randint(self.min_val, self.max_val)
        self.guess = None #the current player guess
        self.e_quit = thorpy.make_button("Quit",
                                         func=thorpy.functions.quit_menu_func)
        self.e_restart = thorpy.make_button("Restart", func=self.restart)
        #a ghost for storing quit and restart:
        self.e_group_menu = thorpy.make_group([self.e_quit, self.e_restart])
        #a counter displaying the trials and some hint/infos about the game
        self.e_counter = thorpy.make_text(text=self.get_trials_text(),
                                          font_color=(0,0,255))
        #the inserter element in which player can insert his guess
        self.e_insert = thorpy.Inserter(name="Try:")
        self.e_background = thorpy.Background( color=(200, 200, 255),
                                                    elements=[self.e_counter,
                                                            self.e_insert,
                                                            self.e_group_menu])
        thorpy.store(self.e_background, gap=20)
        #reaction called each time the player has inserted something
        reaction_insert = thorpy.ConstantReaction(
                            reacts_to=thorpy.constants.THORPY_EVENT,
                            reac_func=self.reac_insert_func,
                            event_args={"id":thorpy.constants.EVENT_INSERT,
                                        "el":self.e_insert})
        self.e_background.add_reaction(reaction_insert)

    def get_trials_text(self):
        return "You have " + str(self.trials) + " more chances."

    def get_hint_text(self):
        if self.number > self.guess:
            return "The number to guess is larger..."
        else:
            return "The number to guess is smaller..."

    def reac_insert_func(self): #here is all the dynamics of the game
        value = self.e_insert.get_value() #get text inserted by player
        self.e_insert.set_value("") #wathever happens, we flush the inserter
        self.e_insert.unblit_and_reblit() #redraw inserter
        try: #try to cast the inserted value as int number
            self.guess = int(value)
        except ValueError: #occurs for example when trying int("some text")
            return
        self.e_counter.unblit()
        self.e_counter.update()
        if self.guess == self.number:
            new_text = "You won! Congratulations, " + self.player_name
        else:
            self.trials -= 1
            if self.trials <= 0:
                new_text = "You lost! The correct number was "+str(self.number)
            else:
                new_text = self.get_trials_text() + " " + self.get_hint_text()
        self.e_counter.set_text(new_text)
        self.e_counter.center(axis=(True,False)) #center on screen only x-axis
        self.e_counter.blit()
        self.e_counter.update()
        self.e_insert.enter() #inserter keeps the focus
        if self.guess == self.number or self.trials <= 0:
            pygame.time.wait(1000)
            self.restart()

    def restart(self):
        self.e_background.unblit() #first unblit the current game
        self.e_background.update()
        self.__init__(self.player_name, self.min_val, self.max_val,
                      self.init_trials) #re-init the game
        thorpy.functions.quit_menu_func() #quit the current menu
        self.launch_game() #relaunch the game

    def launch_game(self):
        self.e_insert.enter() #giv the focus to inserter
        menu = thorpy.Menu(self.e_background) #create and launch the menu
        menu.play()