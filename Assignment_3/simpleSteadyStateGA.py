# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 19:31:41 2019

@author: Gerry Dozier
"""

import os
import random
import sys
import math

#
#  A Simple Steady-State, Real-Coded Genetic Algorithm       
#

class anIndividual:
    def __init__(self, specified_chromosome_length):
        self.chromosome = []
        self.fitness    = 0
        self.chromosome_length = specified_chromosome_length
        
    def randomly_generate(self):
        for i in range(self.chromosome_length):
            self.chromosome.append(random.randint(0, 1))
        self.fitness = 0
    
    def calculate_fitness(self):
        # x2y2 = self.chromosome[0]**2 + self.chromosome[1]**2
        x2y2 = 0
        for i in range(self.chromosome_length):
            x2y2 += self.chromosome[i]**2
        self.fitness = 0.5 + (math.sin(math.sqrt(x2y2))**2 - 0.5) / (1+0.001*x2y2)**2

    def print_individual(self, i):
        print("Chromosome "+str(i) +": " + str(self.chromosome) + " Fitness: " + str(self.fitness))

    def _is_valid_operand(self, other):
        return (hasattr(other, "fitness"))
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.fitness == other.fitness)
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.fitness < other.fitness)
      
class aSimpleSteadyStateGA:
    def __init__(self, population_size, chromosome_length, mutation_rate):
        if (population_size < 2):
            print("Error: Population Size must be greater than 2")
            sys.exit()
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_amt = mutation_rate
        self.population = []
        
    def generate_initial_population(self):
        for i in range(self.population_size):
            individual = anIndividual(self.chromosome_length)
            individual.randomly_generate()
            individual.calculate_fitness()
            self.population.append(individual)
    
    def get_worst_fit_individual(self):
        worst_fitness = 999999999.0  # For Maximization
        worst_individual = -1
        for i in range(self.population_size):
            if (self.population[i].fitness < worst_fitness): 
                worst_fitness = self.population[i].fitness
                worst_individual = i
        return worst_individual
    
    def sort_ascending_fitness(self):
        self.population.sort()

    def get_best_fitness(self):
        best_fitness = -99999999999.0
        best_individual = -1
        for i in range(self.population_size):
            if self.population[i].fitness > best_fitness:
                best_fitness = self.population[i].fitness
                best_individual = i
        return best_fitness
        
    def evolutionary_cycle(self, num_parents):
        self.sort_ascending_fitness()

        parents = []
        for i in range(num_parents):
            # Grab two random individuals from the population
            indiviual_A, indiviual_B = random.sample(range(0, self.population_size), 2)
            # Use the best one of the two as a parent
            A_fitness = self.population[indiviual_A].fitness
            B_fitness = self.population[indiviual_B].fitness
            parent = indiviual_A if A_fitness >= B_fitness else indiviual_B
            parents.append(parent)

        chromosome_probs = []
        for chrom_num in range(self.chromosome_length):
            ones_count = 0
            # Sum all of the 1s of a chromosome
            for parent in parents:
                current_chromosome = self.population[parent].chromosome[chrom_num]
                if current_chromosome == 1:
                    ones_count += 1
            # Divide total 1s by total num of parents to get the probability of passing down 1 to the kid
            chromosome_prob = ones_count / num_parents
            # print(f"Ones Count: {ones_count}  |  Number of Parents: {num_parents}  |  Chromosome Probability: {chromosome_prob}\n\n")
            chromosome_probs.append(chromosome_prob)

        for kid in range(num_parents):
            for chrom_num in range(self.chromosome_length):
                # Chromosome = 1 if a random number is less than or equal to the probability
                random_num = random.uniform(0, 1)
                self.population[kid].chromosome[chrom_num] = \
                    1 if random_num <= chromosome_probs[chrom_num] else 0
                # print(f"Probability: {chromosome_probs[chrom_num]}  |  Random Number: {random_num}  |  Chromosome Value: {self.population[kid].chromosome[chrom_num]}")
                # If random number is less than or equal to the probability then a mutation occurs
                # Mutation flips the bit, i.e., 0 -> 1 | 1 -> 0
                random_num = random.uniform(0, 1)
                if random_num <= self.mutation_amt:
                    self.population[kid].chromosome[chrom_num] = \
                        self.population[kid].chromosome[chrom_num] ^ (1 << 0)
                # print(f"Mutation Rate: {self.mutation_amt}  |  Random Number: {random_num}  |  Chromosome Value: {self.population[kid].chromosome[chrom_num]}\n\n")
            self.population[kid].calculate_fitness()

    def print_population(self):
        for i in range(self.population_size):
            self.population[i].print_individual(i)
    
    def print_best_max_fitness(self):
        best_fitness = -999999999.0  # For Maximization
        best_individual = -1
        for i in range(self.population_size):
            if self.population[i].fitness > best_fitness:
                best_fitness = self.population[i].fitness
                best_individual = i
        print("Best Indvidual: ",str(best_individual)," ", self.population[best_individual].chromosome, " Fitness: ", str(best_fitness))


ChromLength = 95
MaxEvaluations = 15000

# PopSize = int(sys.argv[1])
# mu_amt  = float(sys.argv[2])

PopSize = 44
mu_amt = 0.01
num_parents = (int) (PopSize / 2)

simple_steadystate_ga = aSimpleSteadyStateGA(PopSize,ChromLength,mu_amt)

simple_steadystate_ga.generate_initial_population()
# simple_steadystate_ga.print_population()

for i in range(MaxEvaluations-PopSize+1):
    simple_steadystate_ga.evolutionary_cycle(num_parents)
    print("At Iteration: " + str(i))
    simple_steadystate_ga.print_population()
    if (simple_steadystate_ga.get_best_fitness() >= 0.99754):
        break

print("\nFinal Population\n")
# simple_steadystate_ga.print_population()
simple_steadystate_ga.print_best_max_fitness()
# print("Function Evaluations: " + str(PopSize+i))





    