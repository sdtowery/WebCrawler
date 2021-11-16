import csv
from os import write, makedirs
from os.path import exists
import random
import warnings
from helper import write_to_csv
from simpleSteadyStateGA import aSimpleSteadyStateGA

# Checks if directory is created. Tf not, creates it
# and creates csv file with set column headers and file name
#
# Params: directory


def initialize_directory(directory):
    try:
        # Create directory for csv file if it doesn't already exist
        if not exists(directory):
            makedirs(directory)
    except OSError:
        print('Creating directory. ' + directory)
    except Exception as err:
        print(f"Error: {err}")

    filename = directory + feature_mask_filename
    write_to_csv(filename, column_headers)


# Runs the specified algorithm type with the set algorithm config
#
# Params: algorithm object, algorithm type
# Returns: feature mask, best fitness


def run_algorithm(algorithm_obj, algorithm_type):
    if algorithm_type == "SSGA":
        num_parents = 2
    elif algorithm_type == "SEDA":
        num_parents = (int)(PopSize / 2)
    else:
        print("Invalid algorithm type...")
        return

    algorithm_obj.generate_initial_population()
    for i in range(MaxEvaluations-PopSize+1):
        algorithm_obj.evolutionary_cycle(num_parents)
        if i % PopSize == 0:
            print("At Iteration: " + str(i))
            # algorithm_obj.print_population()
        # TODO: Replace 0.99754 with value signifying optimized feature mask has been found
        if (algorithm_obj.get_best_fitness() >= 0.99754):
            break
    best_fitness, best_individual = algorithm_obj.get_best_max_fitness()
    feature_mask = algorithm_obj.population[best_individual].chromosome
    return feature_mask, best_fitness

# Runs specified algorithm X times specified by algorithm_runs and
# saves the best fit individual of each run in a csv file
#
# Params: algorithm type


def run(algorithm_type):
    if algorithm_type == "SSGA":
        directory = ssga_directory
    elif algorithm_type == "SEDA":
        directory = seda_directory
    else:
        print("Invalid algorithm type...")
        return
    filename = directory + feature_mask_filename
    global total_best_fitness

    for i in range(algorithm_runs):
        print(f"----- {algorithm_type} Run #{i+1} -----")
        algorithm_obj = aSimpleSteadyStateGA(PopSize, ChromLength, mu_amt)
        feature_mask, best_fitness = run_algorithm(
            algorithm_obj, algorithm_type)
        if i == 0:
            initialize_directory(directory)
        row = [i]
        row.extend(feature_mask)
        write_to_csv(filename, row)
        total_best_fitness.append(best_fitness)


# ----- Algorithm Config ----- #
ChromLength = 95
MaxEvaluations = 500
PopSize = 5
mu_amt = 0.01

# ----- Wrapper Config ----- #
algorithm_runs = 30
# - Output - #
ssga_directory = "ssga/"
seda_directory = "seda/"
base_dataset = "HTML_malware_dataset.csv"
feature_mask_dataset = "feature_mask_dataset.csv"
feature_mask_filename = "feature_mask.csv"
column_headers = ["Run #"] + list(range(ChromLength))
total_best_fitness = []

warnings.filterwarnings("ignore")
run("SSGA")
# run("SEDA")


best_fitness = max(total_best_fitness)
print(f"Best fitness: {best_fitness}")
