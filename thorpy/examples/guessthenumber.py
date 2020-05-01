#ThorPy minigame tutorial. Guess the number : start menu
import thorpy
import _mygame as mygame

def launch_game(): #launch the game using parameters from varset
    global varset, e_background
    game = mygame.MyGame(player_name=varset.get_value("player name"),
                         min_val=varset.get_value("minval"),
                         max_val=varset.get_value("maxval"),
                         trials=varset.get_value("trials"))
    game.launch_game()
    game.e_background.unblit() #unblit the game when finished
    game.e_background.update()
    e_background.unblit_and_reblit() #reblit the start menu


application = thorpy.Application(size=(600, 400), caption="Guess the number")

thorpy.set_theme("human")

e_title = thorpy.make_text("My Minigame", font_size=20, font_color=(0,0,150))
e_title.center() #center the title on the screen
e_title.set_topleft((None, 10)) #set the y-coord at 10

e_play = thorpy.make_button("Play!", func=launch_game) #launch the game

varset = thorpy.VarSet() #here we will declare options that user can set
varset.add("trials", value=5, text="Trials:", limits=(1, 20))
varset.add("minval", value=0, text="Min value:", limits=(0, 100))
varset.add("maxval", value=100, text="Max value:", limits=(0, 100))
varset.add("player name", value="Jack", text="Player name:")
e_options = thorpy.ParamSetterLauncher.make([varset], "Options", "Options")

e_quit = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)

e_background = thorpy.Background(color=(200, 200, 255),
                                 elements=[e_title, e_play, e_options, e_quit])
thorpy.store(e_background, [e_play, e_options, e_quit])

menu = thorpy.Menu(e_background)
menu.play()

application.quit()