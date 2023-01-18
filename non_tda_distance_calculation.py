import argparse
import json
import os
import numpy as np
from sklearn.manifold import MDS
from utils import get_dataset, timer


def get_mds(dissimilarity_matrix, is_euclidean=None, random_state=6):
    embedding = MDS(n_components=2, dissimilarity="precomputed",
                    random_state=random_state)
    return embedding.fit_transform(dissimilarity_matrix)


def get_distance(dgm_1, dgm_2, distance_method='ed'):
    return np.linalg.norm(dgm_1 - dgm_2)


def get_adj_matrices_single_subject(data_dir, subject_number):
    print(f"Calculating adjacency matrices for Subject {subject_number}")
    filepath_645 = f'{data_dir}/subject_{subject_number}_mx645.txt'
    filepath_1400 = f'{data_dir}/subject_{subject_number}_mx1400.txt'
    filepath_2500 = f'{data_dir}/subject_{subject_number}_std2500.txt'
    normalized_matrix_645 = get_dataset(filename=filepath_645, fmri=True)
    normalized_matrix_1400 = get_dataset(filename=filepath_1400, fmri=True)
    normalized_matrix_2500 = get_dataset(filename=filepath_2500, fmri=True)
    return [np.array(normalized_matrix_645),
            np.array(normalized_matrix_1400),
            np.array(normalized_matrix_2500)]


def get_adj_matrices(data_directory, total_subjects):
    adj_matrices = []
    for subject_number in range(1, total_subjects + 1):
        adj_matrices.append(get_adj_matrices_single_subject(data_directory,
                                                            subject_number))
    return adj_matrices


def get_pairwise_distances(matrices, subject_number, distance_method='ed'):
    matrix_645, matrix_1400, matrix_2500 = matrices[subject_number - 1]
    distance_645_1400 = get_distance(matrix_645,
                                     matrix_1400,
                                     distance_method=distance_method)
    distance_1400_2500 = get_distance(matrix_1400,
                                      matrix_2500,
                                      distance_method=distance_method)
    distance_645_2500 = get_distance(matrix_645,
                                     matrix_2500,
                                     distance_method=distance_method)
    return [round(distance_645_1400, 3),
            round(distance_1400_2500, 3),
            round(distance_645_2500, 3)]


@timer
def compute_distances_between_cohorts(matrices,
                                      total_subjects,
                                      start_subject=None,
                                      end_subject=None,
                                      distance_method='ed',
                                      output_directory='output_non_tda'):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if start_subject == None:
        start_subject = 1
        end_subject = total_subjects
    generated_json = f'{output_directory}/distances_between_cohorts_{distance_method}.json'
    distances = []
    for subject_number in range(start_subject, end_subject + 1):
        print(f"Calculating distances between cohorts "
              f"for Subject {subject_number}")
        distances.append(get_pairwise_distances(matrices,
                                                subject_number,
                                                distance_method))
    with open(generated_json, "w") as f:
        json.dump(distances, f)
    print(
        f"Done generating the {distance_method} JSON file between cohorts: {generated_json}")


@timer
def compute_mds_within_a_cohort(matrices, total_subjects, cohort,
                                distance_method='ed', generate_file=True,
                                output_directory='output_non_tda'):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    cohort_name = {0: "mx645", 1: "mx1400", 2: "std2500"}[cohort]
    print(f"Calculating {distance_method} distance matrix "
          f"of {total_subjects} subjects for cohort {cohort_name}")
    dissimilarity_matrix = np.array([[0.0 for j in range(total_subjects)]
                                     for i in range(total_subjects)])
    for i in range(total_subjects):
        matrix_1 = matrices[i][cohort]
        for j in range(i):
            matrix_2 = matrices[j][cohort]
            distance = get_distance(matrix_1,
                                    matrix_2,
                                    distance_method=distance_method)
            distance = round(distance, 3)
            dissimilarity_matrix[i - 1][j - 1] = distance
            dissimilarity_matrix[j - 1][i - 1] = distance
    print(f"Calculating MDS of {total_subjects} subjects "
          f"for cohort {cohort_name}")
    if distance_method == "ed":
        mds_matrix = get_mds(dissimilarity_matrix, is_euclidean=True)
    else:
        mds_matrix = get_mds(dissimilarity_matrix, is_euclidean=False,
                             random_state=258)
    if generate_file:
        generated_matrix_file = f'{output_directory}/distance_matrix_{cohort_name}_{distance_method}.json'
        with open(generated_matrix_file, "w") as f:
            json.dump(dissimilarity_matrix.tolist(), f)
            print(f"Done generating {generated_matrix_file}")
        generated_mds_file = f'{output_directory}/mds_{cohort_name}_{distance_method}.json'
        with open(generated_mds_file, "w") as f:
            json.dump(mds_matrix.tolist(), f)
            print(f"Done generating {generated_mds_file}")


@timer
def compute_mds_of_all_cohorts(matrices, total_subjects,
                               distance_method='ed'):
    compute_mds_within_a_cohort(matrices, total_subjects, 0,
                                distance_method)
    compute_mds_within_a_cohort(matrices, total_subjects, 1,
                                distance_method)
    compute_mds_within_a_cohort(matrices, total_subjects, 2,
                                distance_method)


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', '-m',
                        help='Enter the distance method (ed)')
    parser.add_argument('--start', '-s',
                        help='Enter start subject (1, 316)')
    parser.add_argument('--end', '-e',
                        help='Enter end subject (1, 316)')
    parser.add_argument('--distance', '-p',
                        help='To calculate distance matrix (y or n)')
    parser.add_argument('--mds', '-q',
                        help='To calculate MDS (y or n)')

    args = parser.parse_args()
    if args.start:
        main(args.method, start_subject=int(args.start),
             end_subject=int(args.end),
             distance_calculation=args.distance,
             mds_calculation=args.mds)
        return
    parser.print_help()


@timer
def main(method, start_subject=1, end_subject=316,
         distance_calculation='y', mds_calculation='y'):
    data_directory = "full_data"
    total_subjects = 316
    matrices = get_adj_matrices(data_directory, total_subjects)
    if distance_calculation == 'y':
        compute_distances_between_cohorts(matrices,
                                          total_subjects,
                                          start_subject,
                                          end_subject,
                                          distance_method=method)
    if mds_calculation == 'y':
        compute_mds_of_all_cohorts(matrices, total_subjects,
                                   distance_method=method)


if __name__ == "__main__":
    get_user_input()
    # python non_tda_distance_calculation.py --method ed --start 1 --end 316 --distance y --mds y
    # python non_tda_distance_calculation.py --method ed --start 1 --end 316 --distance y --mds n
    # python non_tda_distance_calculation.py --method ed --start 1 --end 316 --distance n --mds y
