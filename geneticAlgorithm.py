""" geneticAlgorithm.py
~~~~~~~~~~~~~~~~~~~~~~~
Contains the Population and Individual classes and applies an genetic algorithm
to them as a training mechanism to train a neural network to play tic tac toe

"""


from network import *
from game import *
from random import randint


### Individual
class Individual(object):
    """ Wrapper for a neural net to play a game and keep track of results """
    def __init__(self, generation, network):
        self.wins, self.losses, self.ties = 0, 0, 0
        self.generation = generation
        self.net = network
        self.player = NeuralnetPlayer(network, self)

    def get_game_player(self): return NeuralnetPlayer(self.network, self)

    def fitness(self): return 2 * self.wins + self.ties - 2 * self.losses


### Population
class Population(object):
    """Measure the fitness of a population of Individual neural networks and
    train them with a genetic algorithm
    """
    def __init__(self, size, carry_over_pct, show_progress=False):
        self.size = size
        self.carry_over_size = int(size * carry_over_pct)
        self.generation = 1
        self.show_progress = show_progress
        self.pool = []
        for i in range(size):
            network = Network([9, 18, 9])
            individual = Individual(self.generation, network)
            self.pool.append(individual)

    def measure_fitness(self):
        """Measure the fitness of each neural network by playing games of tic tac toe"""
        for i in self.pool:
            # play random player 10 times as player one and 10 times as player 2
            for cnt in range(10):
                Game(i.player, RandomPlayer()).play_game()
                Game(RandomPlayer(), i.player).play_game()

            # play againt every other individual
            for j in self.pool:
                if i != j:
                    Game(i.player, j.player).play_game()

        # sort the list, best at the beginning
        self.pool.sort(key=Individual.fitness, reverse=True)

    def print_current_stats(self):
        best = self.pool[0]
        total_games = best.wins + best.ties + best.losses
        worst = self.pool[self.size - 1]
        print("Gen %i | spread: %i to %i  (best possible: %i)" % (self.generation, best.fitness(), worst.fitness(), total_games * 2))

    def advance_one_generation(self):
        """create a new generation based on the fitness of the current generation.
        After measureing the fitness of each individual, cull the cream of the
        crop and breed them using crossover and mutation to (hopefully) produce
        a more fit generation
        """
        self.measure_fitness()

        if self.show_progress:
            self.print_current_stats()

        # We only want the cream of the crop so remove everything after the carry_over_size
        for index in range(self.size - 1, self.carry_over_size, -1):
            del self.pool[index]

        # clear current stats as fitness only applies to current generation
        for i in self.pool:
            i.wins, i.losses, i.ties = 0, 0, 0

        # start breeding the new generation
        self.generation += 1
        # top 2 breed for sure a few times. arranged marriage I guess
        for x in range(self.carry_over_size):
            child = crossover_breed(self.pool[0].net, self.pool[1].net)
            indivdual = Individual(self.generation, child)
            self.pool.append(indivdual)
        # then breed randomly among the cream of the crop until the list is at its full size
        while True:
            mom_net = self.pool[randint(0, self.carry_over_size)].net # randomly pick a mommy
            dad_net = self.pool[randint(0, self.carry_over_size)].net # randomly pick a daddy
            child = crossover_breed(mom_net, dad_net)
            indivdual = Individual(self.generation, child)
            self.pool.append(indivdual)
            if len(self.pool) == self.size:
                break
