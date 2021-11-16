# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 19:31:41 2019

@author: Gerry Dozier
"""

from os.path import exists
from os import remove
import csv
import random
import sys
import math
from helper import write_feature_mask_dataset
from HTML_Malware import HTML_Malware

#
#  A Simple Steady-State, Real-Coded Genetic Algorithm
#


def get_fitness(chromosome):

    html_obj = HTML_Malware("feature_mask_dataset.csv")
    # Inspect the dataset
    # html_obj.inspect_dataset()

    # Preprocess the dataset
    html_obj.preprocess()

    # chrom_fitness = html_obj.knn()
    # chrom_fitness = html_obj.svm_linear()
    # chrom_fitness = html_obj.svm_rbf()
    chrom_fitness = html_obj.mlp()

    x, y = html_obj.svm_rbf(chromosome)

    # return accuracy as the chromosome fitness
    return chrom_fitness


class anIndividual:
    def __init__(self, specified_chromosome_length):
        self.chromosome = []
        self.fitness = 0
        self.chromosome_length = specified_chromosome_length

    def randomly_generate(self):
        for i in range(self.chromosome_length):
            self.chromosome.append(random.uniform(0, 1))
        self.fitness = 0

    # TODO: Get better fitness function
    # fitness will be the final_label (-1.0x + 1.0y)?
    def calculate_fitness(self):
        self.fitness = get_fitness(self.chromosome)

    def print_individual(self, i):
        # print("Chromosome " +str(i) + " - Fitness: " + str(self.fitness))
        print("Chromosome "+str(i) + ": " + str(self.chromosome) +
              " Fitness: " + str(self.fitness))

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
    def __init__(self, population_size, chromosome_length, mutation_rate, svm_rbf):
        if (population_size < 2):
            print("Error: Population Size must be greater than 2")
            sys.exit()
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_amt = mutation_rate
        self.population = []
        self.svm_rbf = svm_rbf

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

    def get_best_fitness(self):
        best_fitness = -99999999999.0
        best_individual = -1
        for i in range(self.population_size):
            if self.population[i].fitness > best_fitness:
                best_fitness = self.population[i].fitness
                best_individual = i
        return best_fitness

    def evolutionary_cycle(self, num_parents):
        # Sort population by ascending fitness so worst fit individuals are in the front
        self.population.sort()

        # Binary Tournament Selection
        parents = []
        for i in range(num_parents):
            # Grab two random individuals from the population
            indiviual_A, indiviual_B = random.sample(
                range(0, self.population_size), 2)
            # Use the best one of the two as a parent
            A_fitness = self.population[indiviual_A].fitness
            B_fitness = self.population[indiviual_B].fitness
            parent = indiviual_A if A_fitness >= B_fitness else indiviual_B
            parents.append(parent)

        for kid in range(num_parents):
            for chrom in range(self.chromosome_length):
                self.population[kid].chromosome[chrom] = random.uniform(
                    parents[0].chromosome[chrom], self.population[1].chromosome[chrom])
                self.population[kid].chromosome[chrom] += self.mutation_amt * \
                    random.gauss(0, 1.0)
                if self.population[kid].chromosome[chrom] > self.ub:
                    self.population[kid].chromosome[chrom] = self.ub
                if self.population[kid].chromosome[chrom] < self.lb:
                    self.population[kid].chromosome[chrom] = self.lb
        self.population[kid].calculate_fitness()

    def print_population(self):
        for i in range(self.population_size):
            self.population[i].print_individual(i)

    def get_best_max_fitness(self):
        best_fitness = -999999999.0  # For Maximization
        best_individual = -1
        for i in range(self.population_size):
            if self.population[i].fitness > best_fitness:
                best_fitness = self.population[i].fitness
                best_individual = i
        return best_fitness, best_individual

    def print_best_max_fitness(self):
        best_fitness, best_individual = self.get_best_max_fitness(self)
        print("Best Indvidual: ", str(best_individual), " ",
              self.population[best_individual].chromosome, " Fitness: ", str(best_fitness))
