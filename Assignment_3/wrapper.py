import csv
from os import write, makedirs
from os.path import exists
from simpleSteadyStateGA import aSimpleSteadyStateGA

# Params: algorithm object, algorithm type
# Returns: feature mask, best fitness


def run_algorithm(ssga, algorithm_type):
    if algorithm_type == "SSGA":
        num_parents = 2
    elif algorithm_type == "SEDA":
        num_parents = (int)(PopSize / 2)
    else:
        print("Invalid algorithm type...")
        return

    ssga.generate_initial_population()
    for i in range(MaxEvaluations-PopSize+1):
        ssga.evolutionary_cycle(num_parents)
        print("At Iteration: " + str(i))
        # ssga.print_population()

        # Found optimized feature mask.
        # TODO: Replace 0.99754 with value signifying optimized feature mask has been found
        if (ssga.get_best_fitness() >= 0.99754):
            break
    best_fitness, best_individual = ssga.get_best_max_fitness()
    feature_mask = ssga.population[best_individual].chromosome
    return feature_mask, best_fitness

# Params: a row to insert into the csv file


def write_to_csv(file_name, row):
    try:
        if exists(file_name):
            file = open(file_name, 'a', newline='')
        else:
            file = open(file_name, 'x', newline='')

        csv_writer = csv.writer(file)
        csv_writer.writerow(row)
        file.close()
    except Exception as err:
        print(f"Error: {err}")


# ----- Wrapper Config ----- #
ssga_directory = "ssga/"
seda_directory = "seda/"
feature_mask_filename = "feature_mask.csv"
algorithm_runs = 30

# ----- Algorithm Config ----- #
ChromLength = 95
MaxEvaluations = 15000
PopSize = 44
mu_amt = 0.01

ssga_feature_mask_filename = ssga_directory + feature_mask_filename

for i in range(algorithm_runs):
    print(f"----- SSGA Run #{i+1} -----")
    ssga = aSimpleSteadyStateGA(PopSize, ChromLength, mu_amt)
    ssga_feature_mask, ssga_best_fitness = run_algorithm(ssga, "SSGA")

    # TODO: Create file and write ssga_feature_mask as a new row
    if i == 0:
        try:
            # Create directory for ssga csv file if it doesn't already exist
            if not exists(ssga_directory):
                makedirs(ssga_directory)
        except OSError:
            print('Error: Creating directory. ' + ssga_directory)
        except Exception as err:
            print(f"Error: {err}")

        # column_headers = list(range(ChromLength))
        column_headers = ["Run #"]
        # column_headers.insert(0, "Run #")
        for j in range(95):
            column_headers.append(j)

        write_to_csv(ssga_feature_mask_filename, column_headers)
    row = [i]
    row.extend(ssga_feature_mask)
    write_to_csv(ssga_feature_mask_filename, row)


# seda = aSimpleSteadyStateGA(PopSize,ChromLength,mu_amt)
# seda_feature_mask, seda_best_fitness = run_algorithm(seda, "SEDA")
# print(seda_feature_mask)
# print(seda_best_fitness)
