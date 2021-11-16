import csv
from os import sep, write, makedirs
from os.path import exists
import random
import warnings
from helper import write_to_csv
from simpleSteadyStateGA import aSimpleSteadyStateGA
from HTML_Malware import HTML_Malware

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


def run_algorithm(algorithm_obj):
    num_parents = 2
    algorithm_obj.generate_initial_population()
    for i in range(MaxEvaluations-PopSize+1):
        algorithm_obj.evolutionary_cycle(num_parents)
        if i % PopSize == 0:
            print("At Iteration: " + str(i))
            # algorithm_obj.print_population()
        if (algorithm_obj.get_best_fitness() == 0.0):
            break
    best_fitness, best_individual_index = algorithm_obj.get_best_fitness()
    best_individual = algorithm_obj.population[best_individual_index].chromosome
    return best_individual, best_fitness, i

# Runs specified algorithm X times specified by algorithm_runs and
# saves the best fit individual of each run in a csv file
#
# Params: algorithm type


def run():
    html_obj = HTML_Malware("HTML_malware_dataset.csv")
    # Inspect the dataset
    # html_obj.inspect_dataset()

    # Preprocess the dataset
    html_obj.preprocess()
    rbf_svc = html_obj.svm_rbf()
    function_evals_total = 0
    best_individuals = []
    best_fitnesses = []
    for i in range(algorithm_runs):
        print(f"----- SSGA Run #{i+1} -----")
        algorithm_obj = aSimpleSteadyStateGA(
            PopSize, ChromLength, mu_amt, lb, ub, rbf_svc)
        best_individual, best_fitness, function_evals = run_algorithm(
            algorithm_obj)
        function_evals_total += function_evals
        best_individuals.append(best_individual)
        best_fitnesses.append(best_fitness)
        print(f"Best individual: {best_individual}")
        print(f"Best fitness: {best_fitness}")
        print(f"Function evaluations: {function_evals}")

    function_evals_avg = function_evals_total / 10
    return best_individuals, best_fitnesses, function_evals_avg


# ----- Algorithm Config ----- #
ChromLength = 95
MaxEvaluations = 10000
PopSize = 44
mu_amt = 0.01
ub = 1.0
lb = 0.0

# ----- Wrapper Config ----- #
algorithm_runs = 10

warnings.filterwarnings("ignore")
best_individuals, best_fitnesses, function_evals_avg = run()

# print(f"10 Best Individuals: {best_individuals}")
print("10 Best Fitnesses:", "\n".join(
    [str(item) for item in best_fitnesses]), sep="\n")
print(f"Average Function Evaluations: {function_evals_avg}")
