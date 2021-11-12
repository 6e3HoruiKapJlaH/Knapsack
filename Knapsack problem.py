import random
import numpy as np
import operator
import copy

def maximum(a, a1, b, b1):
    if a>b:
        return a,a1 
    else:
        return  b,b1
    #return b,b1 if a<=b
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
        new_genome1 = parent[: int(len(self.gen)/4)] +  self.gen[int(len(parent)/4) : int(len(parent)/2)] + parent[int(len(self.gen)/2) : int(3*len(self.gen)/4)] +  self.gen[-int(len(parent)/4):]

        if random.randint(1, 100)%20==0:
            select_gen = random.randint(0, len(new_genome)-1)
            new_genome[select_gen] = 1 if new_genome[select_gen]==0 else 0
        if random.randint(1, 100)%20==0:
            select_gen = random.randint(0, len(new_genome1)-1)
            new_genome1[select_gen] = 1 if new_genome1[select_gen]==0 else 0

        weight = 0
        value = 0
        for i in new_genome:
            if i:
                weight+=start_population[0][i]
                value+=start_population[1][i]
        if weight==0:
            new_person = Individual(new_genome, 0)
        else:
            new_person = Individual(new_genome, value/weight)

        weight = 0
        value = 0
        for i in new_genome1:
            if i:
                weight+=start_population[0][i]
                value+=start_population[1][i]
        if weight==0:
            new_person1 = Individual(new_genome, 0)
        else:
            new_person1 = Individual(new_genome, value/weight)

        return new_person, new_person1

       
def find_parents(arr, start_population):
    arr1 = copy.copy(sorted(arr, key=lambda Individual: Individual.cost, reverse=True))
    result = copy.copy(sorted(arr, key=lambda Individual: Individual.cost))
    max_value=0
    max_gen=[]
    n=0
    while len(result)>=1:
        n+=1



        del result[0]
        element_1 = result[0]
        arr1=[]
        #del result[len(result)-1]

        
        index_2 = random.randint(0, len(result)-1)
        element_2 = result[index_2]

        new_person, new_person1 = element_1.cross_person(element_2.gen, start_population)
        if new_person.get_weight(start_population) > 250 :
            pass


        else:
            del result[index_2]
            if new_person1.get_weight(start_population) <= 250:
        
                if new_person1.get_value(start_population)>max_value:
                    max_value = new_person1.get_value(start_population)
                    #print(max_value)
                    max_gen = new_person1.gen
                    #print(max_gen)
                arr1.append(new_person1)  

            arr1.append(new_person)  

            if new_person.get_value(start_population)>max_value:
                max_value = new_person.get_value(start_population)
                print(max_value)
                max_gen = new_person.gen
                print(max_gen)
                        
        
        if len(result)==1:
            arr1.append(result[0]) 
            result = copy.copy(sorted(arr1, key=lambda Individual: Individual.cost))

    print(n)
    return max_value, max_gen

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
    value, gen = find_parents(start_population[:25], properties)
    value1, gen1 = find_parents(start_population[25:50], properties)
    max_value, max_gen = maximum(value, gen, value1, gen1)
    value, gen = find_parents(start_population[50:75], properties)
    value1, gen1 = find_parents(start_population[75:100], properties)
    max1, gen1 = maximum(value, gen, value1, gen1)
    max_value, max_gen = maximum(max_value, max_gen, max1, gen1)
    print(max_value, max_gen)