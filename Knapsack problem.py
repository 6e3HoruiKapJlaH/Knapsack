import random
import numpy as np
import operator
import copy
from matplotlib import pyplot as plt

def maximum(a, a1, b, b1):
    if a>b:
        return a,a1 
    else:
        return  b,b1

class Individual (object):
    def __init__(self, gen, cost):

        self.gen = gen
        #cost = value/weight (avg value)
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
        #generate 2 successors
        #cross genomes
        new_genome = self.gen[: int(len(self.gen)/4)] + parent[int(len(parent)/4) : int(len(parent)/2)] + self.gen[int(len(self.gen)/2) : int(3*len(self.gen)/4)] + parent[-int(len(parent)/4):]
        new_genome1 = parent[: int(len(self.gen)/4)] +  self.gen[int(len(parent)/4) : int(len(parent)/2)] + parent[int(len(self.gen)/2) : int(3*len(self.gen)/4)] +  self.gen[-int(len(parent)/4):]
       
        #generate mutation
        if random.randint(1, 100)%20==0:
            select_gen = random.randint(0, len(new_genome)-1)
            new_genome[select_gen] = 1 if new_genome[select_gen]==0 else 0
        if random.randint(1, 100)%20==0:
            select_gen = random.randint(0, len(new_genome1)-1)
            new_genome1[select_gen] = 1 if new_genome1[select_gen]==0 else 0

        #create persons
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
    #successors array
    arr1 = copy.copy(sorted(arr, key=lambda Individual: Individual.cost, reverse=True))

    #parents array
    result = copy.copy(sorted(arr, key=lambda Individual: Individual.cost))

    #max value of knapsack
    max_value=0
    max_gen=[]
    
    #array of max values (for grapht)
    n=[]
    while len(result)>=1:

        #select 1st parent
        del result[0]
        element_1 = result[0]
        arr1=[]

        #select 2nd parent
        index_2 = random.randint(0, len(result)-1)
        element_2 = result[index_2]

        #get 2 successors
        new_person, new_person1 = element_1.cross_person(element_2.gen, start_population)

        #no del no sucsessors
        if new_person.get_weight(start_population) > 250 and new_person1.get_weight(start_population) > 250:
            pass

        #2nd successor`s weight >250     
        elif new_person.get_weight(start_population) <= 250 and new_person1.get_weight(start_population) > 250:
            del result[index_2]
            if new_person.get_value(start_population)>max_value:
                max_value = new_person.get_value(start_population)
                max_gen = new_person.gen
            arr1.append(new_person)  


        #1st successor`s weight >250
        elif new_person.get_weight(start_population) > 250 and new_person1.get_weight(start_population) <= 250:
            del result[index_2] 
            if new_person1.get_value(start_population)>max_value:
                max_value = new_person1.get_value(start_population)
                max_gen = new_person1.gen
            arr1.append(new_person1)    

        #common situation
        else:
            del result[index_2]
            
            #upadate max value
            if new_person1.get_weight(start_population) <= 250:
        
                if new_person1.get_value(start_population)>max_value:
                    max_value = new_person1.get_value(start_population)
                    max_gen = new_person1.gen
                arr1.append(new_person1)  

            arr1.append(new_person)  

            if new_person.get_value(start_population)>max_value:
                max_value = new_person.get_value(start_population)
                max_gen = new_person.gen
                

        
        if len(result)==1:
            arr1.append(result[0]) 

            #array of max
            n.append(max_value)

            #go to 
            result = copy.copy(sorted(arr1, key=lambda Individual: Individual.cost))

    plt.plot([i for i in range(0, len(n))], n)
    return max_value, max_gen

def generate_population(number_of_items = 100):
    weight = np.zeros(number_of_items, dtype=int)
    value = np.zeros(number_of_items, dtype=int)

    population = []

    for i in range(0 , number_of_items):
        #generate value and weight
        weight[i] = random.randint(1, 25)
        value[i] = random.randint(2, 30)
        
        #generate genme as [1, 0, 0,..], [0, 1, 0,..], ets
        genome = [0 for j in range(0, i)] + [1] + [0 for j in range(i+1, number_of_items)]
        ind = Individual(genome, value[i]/weight[i])

        #add person
        population.append(ind)

    return (np.append([weight],[value], axis=0)), population 

if __name__ == "__main__":
    #set properties, start_population
    properties, start_population = generate_population()

    #trash
    value, gen = find_parents(start_population[:25], properties)
    value1, gen1 = find_parents(start_population[25:50], properties)
    max_value, max_gen = maximum(value, gen, value1, gen1)
    value, gen = find_parents(start_population[50:75], properties)
    value1, gen1 = find_parents(start_population[75:100], properties)
    max1, gen1 = maximum(value, gen, value1, gen1)
    max_value, max_gen = maximum(max_value, max_gen, max1, gen1)

    #final output
    print(max_value, max_gen)
    plt.grid()
    plt.show()