from sklearn import svm
from HTML_Malware import HTML_Malware
import warnings

SVM_RBF = "svm_rbf"
SVM_LINEAR = "svm_linear"
KNN = "knn"
MLP = "mlp"


def get_confusion_matrix(classifier):

    if (classifier == KNN):
        tn, fp, fn, tp, actual, prediction = html_obj.knn()
    elif (classifier == SVM_RBF):
        tn, fp, fn, tp, actual, prediction = html_obj.svm_rbf()
    elif (classifier == SVM_LINEAR):
        tn, fp, fn, tp, actual, prediction = html_obj.svm_linear()
    else:
        tn, fp, fn, tp, actual, prediction = html_obj.mlp()

    false_positives, false_negatives = get_false_results(actual, prediction)
    # print(f"{len(false_positives)} false positives: {false_positives}")
    # print(f"{len(false_negatives)} false negatives: {false_negatives}")
    return tn, fp, fn, tp, false_positives, false_negatives


def get_false_results(actual, prediction):
    actual_values, actual_indices = actual
    false_positives = []
    false_negatives = []
    for i in range(len(actual_values)):
        if prediction[i] != actual_values[i]:
            if prediction[i] == 1:
                false_positives.append(actual_indices[i])
            else:
                false_negatives.append(actual_indices[i])
    return false_positives, false_negatives


def run(classifier):
    total_runs = 10
    avg_tn = 0
    avg_fp = 0
    avg_fn = 0
    avg_tp = 0
    total_false_positives = []
    total_false_negatives = []

    print(f"=-=-=-=-=- {classifier} -=-=-=-=-=")
    for i in range(total_runs):
        print(f"--- Run #{i+1} ---")
        tn, fp, fn, tp, false_positives, false_negatives = get_confusion_matrix(
            classifier)
        avg_tn += tn
        avg_fp += fp
        avg_fn += fn
        avg_tp += tp
        total_false_positives.append(false_positives)
        total_false_negatives.append(false_negatives)

    avg_tn /= total_runs
    avg_fp /= total_runs
    avg_fn /= total_runs
    avg_tp /= total_runs

    total_false_positives = list(
        set.intersection(*map(set, total_false_positives)))
    total_false_negatives = list(
        set.intersection(*map(set, total_false_negatives)))

    total_false_positives.sort()
    total_false_negatives.sort()

    return avg_tn, avg_fp, avg_fn, avg_tp, total_false_positives, total_false_negatives


# -- main -- #

warnings.filterwarnings("ignore")
html_obj = HTML_Malware('HTML_malware_dataset.csv')

# # Inspect the dataset
# html_obj.inspect_dataset()

# # Preprocess the dataset
html_obj.preprocess()

knn_confusion_matrix = run(KNN)
knn_type1_errors = knn_confusion_matrix[4]
knn_type2_errors = knn_confusion_matrix[5]

svm_rbf_confusion_matrix = run(SVM_RBF)
svm_rbf_type1_errors = svm_rbf_confusion_matrix[4]
svm_rbf_type2_errors = svm_rbf_confusion_matrix[5]

svm_linear_confusion_matrix = run(SVM_LINEAR)
svm_linear_type1_errors = svm_linear_confusion_matrix[4]
svm_linear_type2_errors = svm_linear_confusion_matrix[5]

mlp_confusion_matrix = run(MLP)
mlp_type1_errors = mlp_confusion_matrix[4]
mlp_type2_errors = mlp_confusion_matrix[5]

print(f"\n\n=-=-=-=-=- {KNN} -=-=-=-=-=")
print(f"Average knn Confusion Matrix: {knn_confusion_matrix[:4]}")
print(f"{len(knn_type1_errors)} Type I Errors: {knn_type1_errors}")
print(f"{len(knn_type2_errors)} Type II Errors: {knn_type2_errors}\n\n")

print(f"=-=-=-=-=- {SVM_RBF} -=-=-=-=-=")
print(f"Average svm_rbf Confusion Matrix: {svm_rbf_confusion_matrix[:4]}")
print(f"{len(svm_rbf_type1_errors)} Type I Errors: {svm_rbf_type1_errors}")
print(f"{len(svm_rbf_type2_errors)} Type II Errors: {svm_rbf_type2_errors}\n\n")

print(f"=-=-=-=-=- {SVM_LINEAR} -=-=-=-=-=")
print(
    f"Average svm_linear Confusion Matrix: {svm_linear_confusion_matrix[:4]}")
print(f"{len(svm_linear_type1_errors)} Type I Errors: {svm_linear_type1_errors}")
print(f"{len(svm_linear_type2_errors)} Type II Errors: {svm_linear_type2_errors}\n\n")

print(f"=-=-=-=-=- {MLP} -=-=-=-=-=")
print(f"Average mlp Confusion Matrix: {mlp_confusion_matrix[:4]}")
print(f"{len(mlp_type1_errors)} Type I Errors: {mlp_type1_errors}")
print(f"{len(mlp_type2_errors)} Type II Errors: {mlp_type2_errors}")
