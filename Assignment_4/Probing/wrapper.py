from os import write
import random
import warnings
import csv
from os.path import exists
import numpy as np
import pandas as pd
from sklearn import svm
from HTML_Malware import HTML_Malware
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

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


def create_random_instance(instance_length):
    ci = np.random.dirichlet(np.ones(instance_length), size=1)
    # for i in range(instance_length):
    #     ci.append(random.uniform(
    #         0, 1) / instance_length)

    # ci = np.array(ci)
    ci = ci.reshape(1, -1)
    # normalized_ci = normalize(ci)[0]
    normalized_ci = np.ndarray.tolist(ci)[0]
    sum = 0
    for i in range(len(normalized_ci)):
        sum += normalized_ci[i]
    column_headers = list(range(1, instance_length + 1))
    data = dict(zip(column_headers, normalized_ci))
    random_instance = pd.DataFrame(data, index=[0])
    return random_instance, sum


def probe():
    write_to_csv(second_dataset, column_headers)
    instances = []
    labels = []
    for i in range(number_of_probes):

        random_instance, sum = create_random_instance(instance_length)
        x, y = svm_rbf.predict_proba(random_instance)[0]
        final_label = -1.0 * x + 1.0 * y

        if i % 10 == 0:
            print("At Iteration: " + str(i))
        if final_label == 0.0:
            continue
        if final_label > 0:
            final_label = 1.0
        else:
            final_label = -1.0

        if i == 999:
            print("Scrappy-doo")

        instances.append(random_instance)
        labels.append(final_label)

        csv_row = [i, final_label]
        csv_row.extend(random_instance.values.tolist()[0])
        write_to_csv(second_dataset, csv_row)

    # print(instances)


def compare_svm():
    print(f"Number of probes: {number_of_probes}")

    # Compute first svm accuracy
    pred_rbf_svc = svm_rbf.predict(html_obj.X_test)
    svm_rbf_accuracy = accuracy_score(html_obj.y_test, pred_rbf_svc)
    print(f"SVM_1 accuracy (baseline dataset): {svm_rbf_accuracy}")

    # Compute second svm accuracy
    pred_rbf_svc2 = svm_rbf2.predict(html_obj2.X_test)
    svm_rbf_accuracy2 = accuracy_score(html_obj2.y_test, pred_rbf_svc2)
    print(f"SVM_2 accuracy (second dataset): {svm_rbf_accuracy2}")

    # Compute the mean squared error
    mean_squared_error = pow(svm_rbf_accuracy - svm_rbf_accuracy2, 2)
    print(f"Mean squared error: {mean_squared_error}")


# ----- Wrapper Config ----- #
base_dataset = "HTML_malware_dataset.csv"
second_dataset = "second_dataset.csv"
instance_length = 95
number_of_probes = 595
column_headers = ["webpage_id", "label"] + list(range(1, instance_length + 1))

# ----- Run ----- #
warnings.filterwarnings("ignore")
html_obj = HTML_Malware(base_dataset)

# Preprocess the dataset
html_obj.preprocess()

svm_rbf = html_obj.svm_rbf()

# Probe machine learner
probe()

html_obj2 = HTML_Malware(second_dataset)

# Preprocess the second dataset
html_obj2.preprocess()

svm_rbf2 = html_obj2.svm_rbf()

# Compare the two svm's
compare_svm()
