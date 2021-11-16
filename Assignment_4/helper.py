from os.path import exists
from os import remove
import csv
import numpy as np

# Helper methods for wapper.py and simpleSteadyStateGA.py

# writes the feature masked csv file
#
# Params: feature_mask


def write_feature_mask_dataset(feature_mask):
    base_dataset = "HTML_malware_dataset.csv"
    feature_mask_dataset = "feature_mask_dataset.csv"

    feature_mask = [1, 1] + feature_mask
    feature_mask = np.array(feature_mask, dtype=bool)

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

            repl = [0]
            row_np = np.array(row, dtype=float)
            row_np[~feature_mask] = repl 

            csv_writer.writerow(row_np)

        feature_mask_file.close()
        base_dataset_file.close()
    except Exception as err:
        print(f"Error: {err}")


# Writes the given row to the specified csv file
#
# Params: filename, row


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
