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
from HTML_Malware import HTML_Malware

#
#  A Simple Steady-State, Real-Coded Genetic Algorithm
#


# writes the feature masked csv file
#
# Params: feature_mask


def write_feature_mask_dataset(feature_mask):
    base_dataset = "HTML_malware_dataset.csv"
    feature_mask_dataset = "feature_mask_dataset.csv"

    try:
        if exists(feature_mask_dataset):
            remove(feature_mask_dataset)

        feature_mask_file = open(feature_mask_dataset, 'x', newline='')
        base_dataset_file = open(base_dataset, 'r')

        csv_reader = csv.reader(base_dataset_file)
        csv_writer = csv.writer(feature_mask_file)
        i = 0
        for row in csv_reader:
            # copy the first row of the base dataset to the new dataset
            if i == 0:
                csv_writer.writerow(row)
                i += 1
                continue

            # multiply the row by the feature mask and add it to new dataset
            row_data = []
            col_num = 0
            for j in range(len(row)):
                if j == 0 or j == 1:
                    # copy the first two elements to the new row
                    row_data.append(row[j])
                else:
                    # multiple the row element by the feature mask and add it to new row
                    feature = float(row[j])
                    feature = feature * float(feature_mask[col_num])
                    row_data.append(feature)
                    col_num += 1

            i += 1
            csv_writer.writerow(row_data)

        feature_mask_file.close()
        base_dataset_file.close()
    except Exception as err:
        print(f"Error: {err}")


def get_fitness(chromosome):
    # prepare the new dataset
    write_feature_mask_dataset(chromosome)

    html_obj = HTML_Malware("feature_mask_dataset.csv")
    # Inspect the dataset
    # html_obj.inspect_dataset()

    # Preprocess the dataset
    html_obj.preprocess()

    chrom_fitness = html_obj.knn()
    # chrom_fitness = html_obj.svm_linear()
    # chrom_fitness = html_obj.svm_rbf()
    # chrom_fitness = html_obj.mlp()

    # return accuracy as the chromosome fitness
    # chrom_fitness = ml_info[0]
    return chrom_fitness


class anIndividual:
    def __init__(self, specified_chromosome_length):
        self.chromosome = []
        self.fitness = 0
        self.chromosome_length = specified_chromosome_length

    def randomly_generate(self):
        for i in range(self.chromosome_length):
            self.chromosome.append(random.randint(0, 1))
        self.fitness = 0

    # TODO: Get better fitness function
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

        # TODO: Look into more optimized solution?
        # This section takes a lot of time to run for SEDA.
        # Not sure if it could be optimized better possibly?
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
