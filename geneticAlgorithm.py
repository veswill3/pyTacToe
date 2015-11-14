""" geneticAlgorithm.py
~~~~~~~~~~~~~~~~~~~~~~~
Contains the Population and Individual classes and applies an genetic algorithm
to them as a training mechanism to train a neural network to play tic tac toe

"""


from network import *
from game import *
from random import randint
import pickle
import sys


### Individual
class Individual(object):
    """ Wrapper for a neural net to play a game and keep track of results """
    def __init__(self, generation, network):
        self.wins, self.losses, self.ties = 0, 0, 0
        self.generation = generation
        self.net = network
        self.player = NeuralnetPlayer(network, self)

    def get_game_player(self): return NeuralnetPlayer(self.network, self)

    def fitness(self):
        # Winning and tying is ok but loosing is bad
        return self.wins + self.ties - 6 * self.losses


### Population
class Population(object):

    def __init__(self, pop_size, carry_over_pct, net_sizes):
        """Teach a neural network to play tic tac toe with a genetic algorithm

        Args:
            pop_size (int): The total number of individuals in the population.
            carry_over_pct (float 0-1): percentage of individuals that survive
                or carry over from one generation to the next.
            net_sizes (List[int]): see ``sizes`` in Network for more info.
            show_progress (Optional[bool]): True to print info for each generation

        """
        self.pop_size = pop_size
        self.carry_over_size = int(pop_size * carry_over_pct)
        self.generation = 1
        self.best_individuals_history = []
        self.pool = []
        for i in range(pop_size):
            network = Network(net_sizes)
            individual = Individual(self.generation, network)
            self.pool.append(individual)

    def measure_fitness(self):
        """Measure the fitness of each neural network by playing games of tic tac toe"""

        num_games_vs_rand = 500
        total_games = float(self.pop_size * (num_games_vs_rand * 2 + self.pop_size))
        print_interval = total_games / 100.0
        games_played = 0

        def print_progress():
            if games_played % print_interval == 0:
                percent = games_played / total_games * 100
                sys.stdout.write("\rMeasuring fitness: %1.0f%% through generation" % percent)
                sys.stdout.flush()

        for i in self.pool:
            # play random player 500 times as player X and 500 times as player O (1000 games total)
            for cnt in range(num_games_vs_rand):
                Game(i.player, RandomPlayer()).play_game()
                Game(RandomPlayer(), i.player).play_game()
                games_played += 2
                print_progress()

            # play againt every other individual (including self, because why not)
            for j in self.pool:
                Game(i.player, j.player).play_game()
                games_played += 1
                print_progress()

        # clean up the print display
        print("")
        # sort the list, best at the beginning
        self.pool.sort(key=Individual.fitness, reverse=True)

    def print_current_stats(self):
        best = self.pool[0]
        self.best_individuals_history.append(best)
        print("Current gen: %i | best: %i from gen %i with %i losses" % (self.generation, best.fitness(), best.generation, best.losses))

    def advance_one_generation(self):
        """create a new generation based on the fitness of the current generation.
        After measureing the fitness of each individual, cull the cream of the
        crop and breed them using mutation to produce a more fit generation
        """
        self.measure_fitness()

        self.print_current_stats()

        new_pool = []
        # We only want the cream of the crop, dont worry about copying after the carry_over_size
        for index in range(self.carry_over_size - 1):
            i = self.pool[index]
            # clear current stats as fitness only applies to current generation
            i.wins, i.losses, i.ties = 0, 0, 0
            new_pool.append(i)

        self.generation += 1

        # breed the rest of the new generation
        while True:
            for i in new_pool:
                child = mutate_network(i.net)
                childIndividual = Individual(self.generation, child)
                new_pool.append(childIndividual)
                if len(new_pool) == self.pop_size:
                    self.pool = new_pool
                    self.save_to_file("saved_population.p")
                    return

    def save_to_file(self, filename):
        """Save the population to the file ``filename``."""
        pickle.dump(self, open(filename, "wb"))


def load_population_from_file(filename):
    """Load a population from the file ``filename``.  Returns an
    instance of Population.
    """
    return pickle.load(open(filename, "rb"))
