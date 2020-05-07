"""
gde 4.2.2018
Adapted from Project Mesa Schelling Model example: 
https://github.com/projectmesa/mesa-schelling-example/blob/master/analysis.ipynb
but changed to run stand-alone. 
""" 

import random
from SchellingAgent import SchellingAgent
import itertools
import copy

class SchellingModel():
    '''
    Model class for the Schelling segregation model.
    '''

    def __init__(self, height, width, density, minority_pc):
        '''
        Create a new SchellingModel. 
        
        height - rows in the city
        width - columns in the city
        density - share of cells that are occupied housing units
        minority_pc - share of agents that are of the minority type
        '''

        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.n_iterations = 30
        self.race=2

        # set up an empty grid
        # 0 = empty, 1=minority agent, 2=majority agent
        self.grid = [[0] * self.height] * self.width
        
        self.empty_houses = []
        # this is the list of all agents in the model
        self.agents = []
        
        # Set up agents
        for x in range(0,self.width): 
            for y in range(0, self.height): 
                if random.random() < self.density:
                    if random.random() < self.minority_pc:
                        agent_type = 1
                    else:
                        agent_type = 2
                    # add agents to the agent list
                    a = SchellingAgent((x, y), self.grid, agent_type)
#                     print(a)
                    self.agents.append(a)

    def print_status(self):
        '''
        Print relevant information about the current state of affairs.  
        '''
        happy = 0
        not_happy=0
        for agent in self.agents:
            if agent.is_happy() ==1:
                happy+=1
            else:
                not_happy+=1                                          
        
        print("Total happy agents" , str(happy))
        print("Total unhappy agents" , str(not_happy))
            
#         print("Total number of agents: " + str(len(self.agents)))
     
                    
#         return('Implement print_status()')
        
    def step(self):
        '''
        Run one step of the model.  Let unhappy agents move to an empty square. 
        '''
        print('Implement step')
        
    def run(self, max_iter=30): 
        '''
        Runs all iterations of the model. 
        max_iters - the maximum number of iterations to run. 
        If All agents are happy, halt the model.
        '''
        print('Implement run')
