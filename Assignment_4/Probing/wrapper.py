import random
import pandas as pd
from HTML_Malware import HTML_Malware
from sklearn.preprocessing import normalize


def create_random_instance(instance_length):
    ci = []
    for i in range(instance_length):
        ci.append(random.uniform(
            0, 1) / instance_length)
    column_headers = list(range(1, len(ci) + 1))
    data = dict(zip(column_headers, ci))
    random_instance = pd.DataFrame(data, index=[0])
    print(random_instance)
    normalized_ci = normalize(ci, return_norm=True)
    print(normalized_ci)
    return random_instance


def probe():
    html_obj = HTML_Malware(base_dataset)

    # Preprocess the dataset
    html_obj.preprocess()
    rbf_svc = html_obj.svm_rbf()


base_dataset = "HTML_malware_dataset.csv"
instance_length = 95

create_random_instance(95)
