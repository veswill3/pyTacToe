from game import *
from network import Network
from geneticAlgorithm import Population
from geneticAlgorithm import load_population_from_file
import os.path

# Shim to make sure input works in python v 2 and 3
try:
    input = raw_input
except NameError:
    pass
# end python v 2 and 3 input shim

print("Welcome to pyTacToe. Learning Python and machine learning via TicTacToe.")
print("")

if os.path.isfile("saved_population.p"):
    # load population from file if it exists
    pop = load_population_from_file("saved_population.p")
    print("[saved population autoloaded]")
else:
    # otherwise create a new one
    pop = Population(1000, 0.1, [9, 9, 9])
    print("[new population created]")

while True:
    print("")
    print("What do you want to do?")
    print("    P: Play against the current best neural net")
    print("    #: Train X number of epochs (enter an int)")
    print("    D: Delete current population and start a new one")
    print("    Q: Quit")

    choice = input("Choice: ").lower()
    print("")

    if choice[0] == "q":
        break # quit

    elif choice[0] == "d":
        yn = input("Are you sure? (enter a full YES) ").lower()
        if yn == "yes":
            pop = Population(1000, 0.1, [9, 9, 9])
            print("[new population created]")
        else:
            print("[Aborted]")

    elif choice[0] == "p":
        # play against the current best
        best_player = pop.pool[0].player

        yn = input("Do you want to go first? ").lower()
        if yn[0] == "y":
            game = Game(HumanPlayer(), best_player)
        else:
            game = Game(best_player, HumanPlayer())

        game.play_game()

    else:
        # Train for X epochs
        try:
            for epoch in range(int(choice)):
                pop.advance_one_generation()
        except ValueError:
            print("Invalid choice, try again.")
            continue
