import argparse

from pubmedake import read_pubmedake, evaluate_model
from pubmedake import exact_match, porter_match, partial_match


def get_results(gt_file, extracted_file, ext_key, metric):
    '''
    Get the performance results for an extracted file with the baseline
    '''
    # load the ground truth
    gt_map = read_pubmedake(gt_file)
    # load the extracted keywords
    ext_map = read_pubmedake(extracted_file)
    match_type = exact_match
    if metric == "stem":
        match_type = porter_match
    elif metric == "partial":
        match_type = partial_match
    return evaluate_model(ext_map, gt_map, match_type, ext_key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ground_truth', type=str,
                        help='JSON File with ground truth')
    parser.add_argument('extracted', type=str,
                        help='JSON File with ground truth')
    parser.add_argument('-extract_key', default="keywords_in", type=str)
    parser.add_argument('-metric_type', default="exact", type=str)
    args = parser.parse_args()

    # evaluate the model
    perf = get_results(args.ground_truth, args.extracted,
                       args.extract_key, args.metric_type)
    print("Precision:", perf["precision"])
    print("Recall:", perf["recall"])
    print("F1:", perf["f1"])

