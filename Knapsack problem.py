import random
import numpy as np
import operator


""" 
class Population(object):
    def __init__(self, max_capacity=250, number_of_items = 100):
        self.all_items = np.zeros(number_of_items)

    def generate_population(self):
        for i in self.all_items:
            self.all_items[i] = 1
"""
class Individual (object):
    def __init__(self, gen, cost):
        """ self.weight = weight
        self.value = value  """
        self.gen = gen
        self.cost = cost
    
    def get_value(self, start_population):
        sum = 0
        for i in self.gen:
            if i:
                sum+=start_population[1][i]
        return sum

    def get_weight(self, start_population):
        sum = 0
        for i in self.gen:
            if i:
                sum+=start_population[0][i]
        return sum

    def cross_person(self, parent, start_population):
        new_genome = self.gen[: int(len(self.gen)/4)] + parent[int(len(parent)/4) : int(len(parent)/2)] + self.gen[int(len(self.gen)/2) : int(3*len(self.gen)/4)] + parent[-int(len(parent)/4):]

        if random.randint(1, 100)%20==0:
            select_gen = random.randint(0, len(new_genome)-1)
            new_genome[select_gen] = 1 if new_genome[select_gen]==0 else 0

        weight = 0
        value = 0
        for i in new_genome:
            if i:
                weight+=start_population[0][i]
                value+=start_population[1][i]

        new_person = Individual(new_genome, value/weight)

        return new_person

       
def find_parents(arr, start_population):
    result = sorted(arr, key=operator.attrgetter('cost'))
    
    while len(result)>1:
        result = sorted(result, key=operator.attrgetter('cost'))

        element_1 = result[0]
        result.pop(0)

        index_2 = random.randint(0, len(result)-1)
        element_2 = result[index_2]

        new_person = element_1.cross_person(element_2.gen, start_population)
        if new_person.get_weight(start_population) > 250:
            index_2 = 0
            new_person = element_1.cross_person(result[index_2].gen, start_population)

        result.pop(index_2)
        result.append(new_person)

    return (result)

def generate_population(number_of_items = 100):
    weight = np.zeros(number_of_items, dtype=int)
    value = np.zeros(number_of_items, dtype=int)

    population = []

    for i in range(0 , number_of_items):
        weight[i] = random.randint(1, 25)
        value[i] = random.randint(2, 30)

        genome = [0 for j in range(0, i)] + [1] + [0 for j in range(i+1, number_of_items)]
        ind = Individual(genome, value[i]/weight[i])
        population.append(ind)
        
    return (np.append([weight],[value], axis=0)), population 

if __name__ == "__main__":
    properties, start_population = generate_population()
    find_parents(start_population[:25], properties)

