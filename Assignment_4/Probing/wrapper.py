import random
import warnings
import numpy as np
import pandas as pd
from sklearn import svm
from HTML_Malware import HTML_Malware
from sklearn.preprocessing import normalize, scale


def create_random_instance(instance_length):
    ci = np.random.dirichlet(np.ones(instance_length), size=1)
    # for i in range(instance_length):
    #     ci.append(random.uniform(
    #         0, 1) / instance_length)

    # ci = np.array(ci)
    ci = ci.reshape(1, -1)
    normalized_ci = normalize(ci)[0]
    normalized_ci = np.ndarray.tolist(normalized_ci)
    sum = 0
    for i in range(len(normalized_ci)):
        sum += normalized_ci[i]
    column_headers = list(range(1, instance_length + 1))
    data = dict(zip(column_headers, normalized_ci))
    random_instance = pd.DataFrame(data, index=[0])
    return random_instance, sum


def probe():
    global instance_length, number_of_probes
    html_obj = HTML_Malware(base_dataset)

    # Preprocess the dataset
    html_obj.preprocess()
    svm_rbf = html_obj.svm_rbf()

    instances = []
    labels = []
    for i in range(number_of_probes):

        random_instance, sum = create_random_instance(instance_length)
        x, y = svm_rbf.predict_proba(random_instance)[0]
        final_label = -1.0 * x + 1.0 * y

        if i % 10 == 0:
            print("At Iteration: " + str(i) +
                  "\n\tsum: " + str(sum))
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

    # print(instances)
    print(labels)


base_dataset = "HTML_malware_dataset.csv"
instance_length = 95
number_of_probes = 1000

warnings.filterwarnings("ignore")
probe()
