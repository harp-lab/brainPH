import argparse
import json
import os
import csv
import gudhi
import gudhi.wasserstein
import numpy as np
from sklearn.manifold import MDS
from utils import get_dataset, timer, generate_random_initial_dataset, write_csv, generate_random_data
from barcodes_calculation import get_0_dim_barcodes


def get_mds(dissimilarity_matrix, is_euclidean=None, random_state=6):
    if is_euclidean:
        embedding = MDS(n_components=2, random_state=random_state)
    else:
        embedding = MDS(n_components=2, dissimilarity="precomputed",
                        random_state=random_state)
    return embedding.fit_transform(dissimilarity_matrix)


def get_barcodes_distance(dgm_1, dgm_2, distance_method='ws'):
    if distance_method == 'ws':
        return gudhi.wasserstein.wasserstein_distance(dgm_1, dgm_2,
                                                      order=1., internal_p=2.)
    elif distance_method == 'bn':
        return gudhi.bottleneck_distance(dgm_1, dgm_2)
    elif distance_method == 'ed':
        return np.linalg.norm(dgm_1 - dgm_2)


def get_barcodes_single_subject(data_dir, subject_number, manual=False):
    print(f"Calculating barcodes for Subject {subject_number}")
    filepath_645 = f'{data_dir}/subject_{subject_number}_mx645.txt'
    filepath_1400 = f'{data_dir}/subject_{subject_number}_mx1400.txt'
    filepath_2500 = f'{data_dir}/subject_{subject_number}_std2500.txt'
    normalized_matrix_645 = get_dataset(filename=filepath_645, fmri=True)
    normalized_matrix_1400 = get_dataset(filename=filepath_1400, fmri=True)
    normalized_matrix_2500 = get_dataset(filename=filepath_2500, fmri=True)
    if manual:
        barcodes_645 = np.array(get_0_dim_barcodes(normalized_matrix_645))
        barcodes_1400 = np.array(get_0_dim_barcodes(normalized_matrix_1400))
        barcodes_2500 = np.array(get_0_dim_barcodes(normalized_matrix_2500))
    else:
        rips_complex_645 = gudhi.RipsComplex(
            distance_matrix=normalized_matrix_645)
        rips_complex_1400 = gudhi.RipsComplex(
            distance_matrix=normalized_matrix_1400)
        rips_complex_2500 = gudhi.RipsComplex(
            distance_matrix=normalized_matrix_2500)
        pd_645 = rips_complex_645.create_simplex_tree(
            max_dimension=1).persistence()[1:]
        pd_1400 = rips_complex_1400.create_simplex_tree(
            max_dimension=1).persistence()[1:]
        pd_2500 = rips_complex_2500.create_simplex_tree(
            max_dimension=1).persistence()[1:]
        barcodes_645 = np.array([pair[1] for pair in pd_645])
        barcodes_1400 = np.array([pair[1] for pair in pd_1400])
        barcodes_2500 = np.array([pair[1] for pair in pd_2500])
    return [barcodes_645, barcodes_1400, barcodes_2500]


def get_barcodes(data_directory, total_subjects):
    barcodes = []
    for subject_number in range(1, total_subjects + 1):
        barcodes.append(get_barcodes_single_subject(data_directory,
                                                    subject_number))
    return barcodes


def get_distances(barcodes, subject_number, distance_method='ws'):
    barcodes_645, barcodes_1400, barcodes_2500 = barcodes[subject_number - 1]
    distance_645_1400 = get_barcodes_distance(barcodes_645,
                                              barcodes_1400,
                                              distance_method=distance_method)
    distance_1400_2500 = get_barcodes_distance(barcodes_1400,
                                               barcodes_2500,
                                               distance_method=distance_method)
    distance_645_2500 = get_barcodes_distance(barcodes_645,
                                              barcodes_2500,
                                              distance_method=distance_method)
    return [round(distance_645_1400, 3),
            round(distance_1400_2500, 3),
            round(distance_645_2500, 3)]


@timer
def compute_distances_between_cohorts(barcodes,
                                      total_subjects,
                                      start_subject=None,
                                      end_subject=None,
                                      distance_method='ws',
                                      output_directory='output_random'):
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
        distances.append(get_distances(barcodes,
                                       subject_number,
                                       distance_method))
    with open(generated_json, "w") as f:
        json.dump(distances, f)
    print(
        f"Done generating the {distance_method} JSON file between cohorts: {generated_json}")


@timer
def compute_mds_within_a_cohort(barcodes, total_subjects, cohort,
                                distance_method='ws', generate_file=True,
                                output_directory='output_random'):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    cohort_name = {0: "mx645", 1: "mx1400", 2: "std2500"}[cohort]
    print(f"Calculating {distance_method} distance matrix "
          f"of {total_subjects} subjects for cohort {cohort_name}")
    dissimilarity_matrix = np.array([[0.0 for j in range(total_subjects)]
                                     for i in range(total_subjects)])
    for i in range(total_subjects):
        barcodes_1 = barcodes[i][cohort]
        for j in range(i):
            barcodes_2 = barcodes[j][cohort]
            distance = get_barcodes_distance(barcodes_1,
                                             barcodes_2,
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
def compute_mds_of_all_cohorts(barcodes, total_subjects,
                               distance_method='ws'):
    compute_mds_within_a_cohort(barcodes, total_subjects, 0,
                                distance_method)
    compute_mds_within_a_cohort(barcodes, total_subjects, 1,
                                distance_method)
    compute_mds_within_a_cohort(barcodes, total_subjects, 2,
                                distance_method)


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', '-m',
                        help='Enter one of the distance method (ws, bn)')
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
    data_directory = "random_data"
    total_subjects = 316
    barcodes = get_barcodes(data_directory, (end_subject - start_subject) + 1)
    if distance_calculation == 'y':
        compute_distances_between_cohorts(barcodes,
                                          total_subjects,
                                          start_subject,
                                          end_subject,
                                          distance_method=method)
    if mds_calculation == 'y':
        compute_mds_of_all_cohorts(barcodes, total_subjects,
                                   distance_method=method)


if __name__ == "__main__":
    generate_random_data("random_data", start_subject=1, end_subject=316)
    get_user_input()
    # python distance_calculation_random.py --method ws --start 1 --end 316 --distance y --mds y
