"""Name: Flappy Bird Clone
   Python ver: 3.2 or 2.x
   Author: Innocent M Sakala
   Alias: Xenorm
   Start: 02/01/17 #Finish: 19/01/17
   Email: innocentmsakala@gmail.com"""

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/


from game import *

if __name__ == "__main__":

    game = Game()
    restart = game.play()
    while restart == 1:
        game = Game()
        restart = game.restart_button()
