"""
gde 4.2.2018
Adapted from Project Mesa Schelling Model example:
https://github.com/projectmesa/mesa-schelling-example/blob/master/analysis.ipynb
but changed to run stand-alone.
"""

import matplotlib.pyplot as plt
import itertools
import random
import copy


class SchellingAgent:
    """
    Schelling segregation agent
    """

    def __init__(self, grid, no_of_empty_houses, races):
        """
         Create a new Schelling agent.

         Args:
            pos: (x, y) Agent initial location.
            grid: a grid of the city, where 0=empty, 1=minority, 2=majority
            agent_type: Indicator for the agent's type (minority=1, majority=2)
        """
        # self.all_houses = grid
        # self.empty_ratio = no_of_empty_houses
        # self.races = races
        # self.agents = {}
        #
        # random.shuffle(self.all_houses)
        #
        # self.n_empty = int(self.empty_ratio * len(self.all_houses))
        # self.empty_houses = self.all_houses[:self.n_empty]
        #
        # self.remaining_houses = self.all_houses[self.n_empty:]
        # houses_by_race = [self.remaining_houses[i::self.races] for i in range(self.races)]
        # for i in range(self.races):
        #     # create agent for each race
        #     self.agents = dict(
        #         list(self.agents.items()) +
        #         list(dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items())
        #     )

    def calculate_similarity(self):
        """
        Calculates the similarity ratio for the agent.  Defined as:
            similarity = neighbors of same type / total (non-empty) neighbors
        """
        print('Implement calculate_similarity()')

    def is_happy(self):
        """
        The agent is happy if at least 30% of its neighbors are of the same type.
        """
        print('Implement is_happy()')

    def move(self):
        """
        Moves the agent to a randomly selected empty square.
        """
        print('Implement move')


class SchellingModel:
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height, width, density, minority_pc, races=2):
        """
        Create a new SchellingModel.
        height - rows in the city
        width - columns in the city
        density - share of cells that are occupied housing units
        minority_pc - share of agents that are of the minority type
        """

        self.height = height
        self.width = width
        self.races = races
        self.density = density
        self.empty_ratio = self.density
        self.minority_pc = minority_pc
        self.similarity_threshold = self.minority_pc
        self.n_iterations = 5
        self.empty_houses = []
        self.agents = {}

        # Set up agents
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        # self.agents = SchellingAgent(self.all_houses, self.empty_ratio, self.races)
        random.shuffle(self.all_houses)

        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_houses = self.all_houses[:self.n_empty]

        self.remaining_houses = self.all_houses[self.n_empty:]
        houses_by_race = [self.remaining_houses[i::self.races] for i in range(self.races)]
        for i in range(self.races):
            # create agent for each race
            self.agents = dict(
                list(self.agents.items()) +
                list(dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items())
            )

    def print_status(self):
        """
        Print relevant information about the current state of affairs.
        """
        # return ('Implement print_status()')
        no_happy_agents = 0
        no_unhappy_agents = 0
        # for index, values in enumerate(self.agents):
        #     if values == 1:
        #         no_happy_agents += 1
        #     if values == 2:
        #         no_unhappy_agents += 1

        for agent in self.agents:
            if self.agents[agent] == 1:
                no_happy_agents += 1
            if self.agents[agent] == 2:
                no_unhappy_agents += 1

        print("Number of happy agents = {}, Number of unhappy agents = {}".format(no_happy_agents, no_unhappy_agents))

    def step(self, x, y):
        """
        Run one step of the model.  Let unhappy agents move to an empty square.
        """
        # print('Implement step')
        race = self.agents[(x, y)]
        count_similar = 0
        count_difference = 0
        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
            if self.agents[(x - 1, y - 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if y > 0 and (x, y - 1) not in self.empty_houses:
            if self.agents[(x, y - 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
            if self.agents[(x + 1, y - 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x > 0 and (x - 1, y) not in self.empty_houses:
            if self.agents[(x - 1, y)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
            if self.agents[(x + 1, y)] == race:
                count_similar += 1
            else:
                count_difference += 1

        # now with self.height
        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
            if self.agents[(x, y + 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
            if self.agents[(x + 1, y + 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if (count_similar + count_difference) == 0:
            return False
        else:
            return float(count_similar / (count_similar + count_difference)) < self.similarity_threshold

    def run(self, max_iter=30):
        """
        Runs all iterations of the model.
        max_iters - the maximum number of iterations to run.
        If All agents are happy, halt the model.
        """
        # print('Implement run')
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_change = 0
            for agent in self.old_agents:
                if self.is_unsatisfied(agent[0], agent[1]):
                    agent_race = self.agents[agent]
                    empty_house = random.choice(self.empty_houses)
                    self.agents[empty_house] = agent_race
                    del self.agents[agent]
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)
                    n_change += 1
            print(n_change)
            if n_change == 0:
                break
        print("Process Completed")

    def move_to_empty(self, x, y):
        race = self.agents[(x, y)]
        empty_house = randome.choice(self.empty_houses)
        self.updated_agents[empty_house] = race
        del self.updated_agents[(x, y)]
        self.empty_houses.remove(empty_house)
        self.empty_houses.append((x, y))

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        # If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1: 'b', 2: 'r', 3: 'g', 4: 'c', 5: 'm', 6: 'y', 7: 'k'}
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

    def is_unsatisfied(self, x, y):
        race = self.agents[(x, y)]
        count_similar = 0
        count_difference = 0
        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
            if self.agents[(x - 1, y - 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if y > 0 and (x, y - 1) not in self.empty_houses:
            if self.agents[(x, y - 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
            if self.agents[(x + 1, y - 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x > 0 and (x - 1, y) not in self.empty_houses:
            if self.agents[(x - 1, y)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
            if self.agents[(x + 1, y)] == race:
                count_similar += 1
            else:
                count_difference += 1

        # now with self.height
        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
            if self.agents[(x, y + 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
            if self.agents[(x + 1, y + 1)] == race:
                count_similar += 1
            else:
                count_difference += 1

        if (count_similar + count_difference) == 0:
            return False
        else:
            return float(count_similar / (count_similar + count_difference)) < self.similarity_threshold


model_1 = SchellingModel(10, 10, 0.3, 0.3)
model_1.print_status()
model_1.run()
model_1.plot('Schelling Model with 2 colors: Final State with Similarity Threshold 30%', 'schelling_2_30_final.png')
