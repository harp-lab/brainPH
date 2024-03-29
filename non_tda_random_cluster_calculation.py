import json
import math
import os

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from utils import timer
from distance_calculation import get_mds


def get_dataset(datafile):
    with open(datafile, "r") as json_file:
        return np.array(json.load(json_file))


def get_labels_highest_score(dataset):
    max_score = -math.inf
    labels = None
    number_of_clusters = 9
    for i in range(2, 16):
        cluster = KMeans(n_clusters=i, random_state=10)
        cluster_labels = cluster.fit_predict(dataset)
        score = silhouette_score(dataset, cluster_labels)
        if score > max_score:
            number_of_clusters = i
            max_score = score
            labels = cluster_labels
    return number_of_clusters, labels


def plot_subplot(labels, unique_labels, dataset, title, index):
    ax = plt.subplot(1, 3, index)
    for i in unique_labels:
        x = dataset[labels == i, 0]
        y = dataset[labels == i, 1]
        label = f"cluster {i + 1}"
        if i == -1:
            label = "noise"
        ax.scatter(x, y, label=label)
        ax.legend()
    ax.set_title(title)
    plt.tight_layout()


def plot_independent_figure(labels, unique_labels, dataset, title, image_name):
    ax = plt.subplot(1, 1, 1)
    for i in unique_labels:
        x = dataset[labels == i, 0]
        y = dataset[labels == i, 1]
        label = f"cluster {i + 1}"
        if i == -1:
            label = "noise"
        ax.scatter(x, y, label=label, s=4)
        ax.legend()
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(image_name, dpi=120)
    plt.close()


def generate_kmeans_clusters(mx_645_mds_path,
                             mx_1400_mds_path,
                             std_2500_mds_path,
                             output_directory, distance="ed",
                             single_figure=False):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    dataset_mx_645 = get_dataset(mx_645_mds_path)
    dataset_mx_1400 = get_dataset(mx_1400_mds_path)
    dataset_std_2500 = get_dataset(std_2500_mds_path)
    n_clusters_645, labels_645 = get_labels_highest_score(dataset_mx_645)
    unique_labels_645 = np.unique(labels_645)
    n_clusters_1400, labels_1400 = get_labels_highest_score(dataset_mx_1400)
    unique_labels_1400 = np.unique(labels_1400)
    n_clusters_2500, labels_2500 = get_labels_highest_score(dataset_std_2500)
    unique_labels_2500 = np.unique(labels_2500)

    cluster_info = [
        n_clusters_645, n_clusters_1400, n_clusters_2500
    ]
    cluster_file = f"{output_directory}/clusters_{distance}.json"
    title = f'mx645: {n_clusters_645} clusters'
    image_name = f"{output_directory}/clusters_mx645_{distance}.png"
    if single_figure:
        plot_subplot(labels_645, unique_labels_645, dataset_mx_645, title, 1)
    else:
        plot_independent_figure(labels_645, unique_labels_645, dataset_mx_645,
                                title, image_name)
        print(f"Generated {image_name}")
    title = f'mx1400: {n_clusters_1400} clusters'
    image_name = f"{output_directory}/clusters_mx1400_{distance}.png"
    if single_figure:
        plot_subplot(labels_1400, unique_labels_1400, dataset_mx_1400,
                     title, 2)
    else:
        plot_independent_figure(labels_1400, unique_labels_1400,
                                dataset_mx_1400, title, image_name)
        print(f"Generated {image_name}")
    title = f'std2500: {n_clusters_2500} clusters'
    image_name = f"{output_directory}/clusters_std2500_{distance}.png"
    if single_figure:
        image_name = f"{output_directory}/clusters_{distance}.png"
        plot_subplot(labels_2500, unique_labels_2500, dataset_std_2500,
                     title, 3)
        plt.suptitle(f"Clustering result with {distance}")
        plt.tight_layout()
        plt.savefig(image_name, dpi=200)
        plt.close()
    else:
        plot_independent_figure(labels_2500, unique_labels_2500,
                                dataset_std_2500, title, image_name)
    print(f"Generated {image_name}")

    with open(cluster_file, "w") as json_file:
        json.dump(cluster_info, json_file)
    print(f"Generated {cluster_file}")

    return cluster_info


def show_clustering_table(labels_645, labels_1400, labels_2500):
    print(f"Clustering result (645ms, 1400ms, 2500ms):")
    for i in range(len(labels_645)):
        print(f"{i + 1} & {labels_645[i]} & "
              f"{labels_1400[i]} & {labels_2500[i]} \\\\ \\hline")
    print("")


def get_cluster_subject_group(labels):
    cluster = []
    max_label = max([int(label) for label in labels]) + 1
    for i in range(max_label):
        cluster.append([])

    for i, label in enumerate(labels):
        cluster[label].append(i + 1)
    return cluster


def show_matching_between_clusters(output_dir, cluster_645, cluster_1400,
                                   cluster_2500):
    cluster_group = {}
    for i in range(len(cluster_645)):
        for j in range(len(cluster_1400)):
            for k in range(len(cluster_2500)):
                x = set(cluster_645[i]).intersection(set(cluster_1400[j]))
                total_matches = x.intersection(set(cluster_2500[k]))
                group_id = f"{i}{j}{k}"
                cluster_group[group_id] = total_matches
    # for i in cluster_group:
    #     print(f"Cluster group: {i}: match: {cluster_group[i]}")
    # print("")
    triplet = {}
    print(f"{output_dir}:")
    for i in cluster_group:
        print(f"Cluster group: {i}: #match: {len(cluster_group[i])}")
        triplet[i] = len(cluster_group[i])

    triplet_file = f"{output_dir}/clusters_triplet.json"
    with open(triplet_file, "w") as json_file:
        json.dump(triplet, json_file, indent=4)
    print(f"Generated {triplet_file}")


def get_subjects_cluster_id(output_dir, mx_645_mds_path,
                            mx_1400_mds_path,
                            std_2500_mds_path):
    dataset_mx_645 = get_dataset(mx_645_mds_path)
    dataset_mx_1400 = get_dataset(mx_1400_mds_path)
    dataset_std_645 = get_dataset(std_2500_mds_path)
    n_clusters_645, labels_645 = get_labels_highest_score(dataset_mx_645)
    n_clusters_1400, labels_1400 = get_labels_highest_score(dataset_mx_1400)
    n_clusters_2500, labels_2500 = get_labels_highest_score(dataset_std_645)
    cluster_645 = get_cluster_subject_group(labels_645)
    cluster_1400 = get_cluster_subject_group(labels_1400)
    cluster_2500 = get_cluster_subject_group(labels_2500)
    show_matching_between_clusters(output_dir, cluster_645, cluster_1400,
                                   cluster_2500)

    print("\nAdjacency matrix:")
    ar = []
    for temp in cluster_645:
        ar.append(temp)
    for temp in cluster_1400:
        ar.append(temp)
    for temp in cluster_2500:
        ar.append(temp)
    matrix = [[0 for j in range(len(ar))] for i in range(len(ar))]

    for i in range(len(ar)):
        for j in range(len(ar)):
            matrix[i][j] = len(set(ar[i]).intersection(set(ar[j])))
    print(f"{output_dir}:")
    print(f"Rows X Columns: [645 clusters, 1400 clusters, 2500 clusters]")
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(matrix[i][j], end=" ")
        print("")
    print("")
    adj_matrix_file = f"{output_dir}/clusters_adjancency.json"
    with open(adj_matrix_file, "w") as json_file:
        json.dump(matrix, json_file)
    print(f"Generated {adj_matrix_file}\n")


@timer
def main():
    mx_645_mds_ws = "output_non_tda_random/mds_mx645_ed.json"
    mx_1400_mds_ws = "output_non_tda_random/mds_mx1400_ed.json"
    std_2500_mds_ws = "output_non_tda_random/mds_std2500_ed.json"
    output_dir = "output_non_tda_random"

    cluster_summary = generate_kmeans_clusters(mx_645_mds_ws,
                                               mx_1400_mds_ws,
                                               std_2500_mds_ws,
                                               output_dir, distance="ed",
                                               single_figure=False)
    print(f"Number of clusters in 3 cohorts: {cluster_summary}")

    get_subjects_cluster_id(output_dir, mx_645_mds_ws,
                            mx_1400_mds_ws, std_2500_mds_ws)


if __name__ == "__main__":
    main()

# python non_tda_random_cluster_calculation.py