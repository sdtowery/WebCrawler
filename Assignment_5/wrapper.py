from HTML_Malware import HTML_Malware
import warnings

SVM_RBF = "svm_rbf"
SVM_LINEAR = "svm_linear"
KNN = "knn"
MLP = "mlp"


def get_confusion_matrix(classifier):
    warnings.filterwarnings("ignore")
    html_obj = HTML_Malware('HTML_malware_dataset.csv')

    # # Inspect the dataset
    # html_obj.inspect_dataset()

    # # Preprocess the dataset
    html_obj.preprocess()

    if (classifier == KNN):
        tn, fp, fn, tp, actual, prediction = html_obj.knn()
    elif (classifier == SVM_RBF):
        tn, fp, fn, tp, actual, prediction = html_obj.svm_rbf()
    elif (classifier == SVM_LINEAR):
        tn, fp, fn, tp, actual, prediction = html_obj.svm_linear()
    else:
        tn, fp, fn, tp, actual, prediction = html_obj.mlp()

    false_positives, false_negatives = get_false_results(actual, prediction)
    print(f"{len(false_positives)} false positives: {false_positives}")
    print(f"{len(false_negatives)} false negatives: {false_negatives}")
    return tn, fp, fn, tp

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

    print(f"=-=-=-=-=- {classifier} -=-=-=-=-=")
    for i in range(total_runs):
        print(f"--- Run #{i+1} ---")
        tn, fp, fn, tp = get_confusion_matrix(classifier)
        avg_tn += tn
        avg_fp += fp
        avg_fn += fn
        avg_tp += tp

    avg_tn /= total_runs
    avg_fp /= total_runs
    avg_fn /= total_runs
    avg_tp /= total_runs

    return avg_tn, avg_fp, avg_fn, avg_tp


# -- main -- #
knn_confusion_matrix = run(KNN)
svm_rbf_confusion_matrix = run(SVM_RBF)
svm_linear_confusion_matrix = run(SVM_LINEAR)
mlp_confusion_matrix = run(MLP)


print(f"Average knn Confusion Matrix: {knn_confusion_matrix}")
print(f"Average svm_rbf Confusion Matrix: {svm_rbf_confusion_matrix}")
print(f"Average svm_linear Confusion Matrix: {svm_linear_confusion_matrix}")
print(f"Average mlp Confusion Matrix: {mlp_confusion_matrix}")
