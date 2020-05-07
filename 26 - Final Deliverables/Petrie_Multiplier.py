import random
from random import choice


class PetrieAgent:
    """
    Creates agent for the petrie model simulation
    Each agent holds four parameters:
    count - Agent's ID
    sex - Gender of the Agent - 'Male' or 'Female'
    sexist - whether the agent is sexist comment tendency or not. 0 for not being sexist, 1 being sexist
    sexist_remarks_received - whether it received any sexist comments from other opposite gender (default=0)
    """

    def __init__(self, count, sex, sexist, sexist_remarks_received):
        self.count = count
        self.sex = sex
        self.sexist = sexist
        self.sexist_remarks_received = sexist_remarks_received
        self.agent = [self.count, self.sex, self.sexist, self.sexist_remarks_received]


class PetrieModel:
    """
    The is Petrie Model.
    By default it takes three parameters:
    number of people, the ratio of female to male and the ratio of number of female and male being sexist
    It also has three implementable methods:
    step()
    run_model()
    print_summary()
    """

    def __init__(self, no_of_people, female_to_male_ratio, sexist_ratio):
        self.no_of_people = no_of_people
        self.female_to_male_ratio = female_to_male_ratio
        self.number_of_male = 0
        self.number_of_female = 0
        self.sexist_male = 0
        self.sexist_female = 0
        self.sexist = 0
        self.sexist_remarks_received = 0
        self.count = 0
        self.population = []
        self.female_population = []
        self.male_population = []
        self.index = 0
        self.sex = ""
        self.sexist_ratio = sexist_ratio

        while self.index < self.no_of_people:
            male_ratio = 1 - self.female_to_male_ratio
            if self.number_of_male < int(male_ratio * self.no_of_people):
                self.sex = 'Male'
                if self.sexist_male < int(self.sexist_ratio * male_ratio * self.no_of_people):
                    self.sexist = 1
                    self.sexist_male += 1
                else:
                    self.sexist = 0
                self.number_of_male += 1
            else:
                self.sex = 'Female'
                if self.sexist_female < int(self.female_to_male_ratio * self.sexist_ratio * self.no_of_people):
                    self.sexist = 1
                    self.sexist_female += 1
                else:
                    self.sexist = 0
                self.number_of_female += 1
            agent = PetrieAgent(self.count, self.sex, self.sexist, self.sexist_remarks_received)
            self.population.append(agent)
            self.count += 1
            self.index += 1
        self.mmale = 0
        self.mfemale = 0
        for i, values in enumerate(self.population):
            if values.sex == "Male":
                self.male_population.append(values)
            else:
                self.female_population.append(values)


    def step(self):
        """
        iterates the model by one step
        From the pool of persons, identifies an individual at random, checks whether if the individual is sexist
        if yes, picks a random individual from opposite sex and directs the comment to it.
        :return: null
        """
        chosen_person = random.choice(self.population)
        # print(chosen_persons)
        sexist_target = []
        if chosen_person.sex == 'Male' and chosen_person.sexist == 1:
            sexist_target = random.choice(self.female_population)
            # print("Target Female member:{}".format(sexist_target))
            self.population.remove(sexist_target)
            self.female_population.remove(sexist_target)
            sexist_target.sexist_remarks_received += 1
            self.female_population.append(sexist_target)
            self.population.append(sexist_target)
        if chosen_person.sex == 'Female' and chosen_person.sexist == 1:
            sexist_target = random.choice(self.male_population)
            # print("Target Male member:{}".format(sexist_target))
            self.population.remove(sexist_target)
            self.male_population.remove(sexist_target)
            sexist_target.sexist_remarks_received += 1
            self.male_population.append(sexist_target)
            self.population.append(sexist_target)

    def run_model(self, n_iterations=1000):
        """runs the model for user-defined iteration numbers.
        If user doesnt specify the iteration then the model run for default 1000 times. """
        male = female = 0
        for count in range(n_iterations):
            self.step()
        for index, value in enumerate(self.population):
            if value.sex == "Male" and value.sexist_remarks_received >= 1:
                male += value.sexist_remarks_received
            if value.sex == "Female" and value.sexist_remarks_received >= 1:
                female += value.sexist_remarks_received
        # print('number of male:{}'.format(number_of_male))
        # mean number of sexist remarks per male
        self.mmale = (male / self.number_of_male)
        # print('number of female:{}'.format(number_of_female))
        # mean number of sexist remarks per female
        self.mfemale = (female / self.number_of_female)

    def print_summary(self):
        """
            provides summary of the statistics related to Petrie Model
        """
        print("Mean sexist remarks received by male:{}".format(self.mmale))
        print("Mean sexist remarks received by female:{}".format(self.mfemale))
        print("Petrie Multiplier:{}".format(self.mfemale / self.mmale))


pm = PetrieModel(50, 0.20, 0.20)
pm.run_model(1000)
pm.print_summary()
