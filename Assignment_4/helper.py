from os.path import exists
from os import remove
import csv

# Helper methods for wapper.py and simpleSteadyStateGA.py

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
