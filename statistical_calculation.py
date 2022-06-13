import json
from scipy.stats import f_oneway, ttest_rel
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean


def get_anova_p_value(wd_645_1400, wd_1400_2500, wd_2500_645):
    anova_result = f_oneway(wd_645_1400, wd_1400_2500, wd_2500_645)
    return anova_result[1]


def get_t_values(wd_645_1400, wd_1400_2500, wd_2500_645):
    t_values = []
    t_values.append(ttest_rel(wd_645_1400, wd_1400_2500)[1])
    t_values.append(ttest_rel(wd_1400_2500, wd_2500_645)[1])
    t_values.append(ttest_rel(wd_2500_645, wd_645_1400)[1])
    return [round(i, 3) for i in t_values]


def get_p_values(wd_645_1400, wd_1400_2500, wd_2500_645):
    p_values = []
    p_values.append(f_oneway(wd_645_1400, wd_1400_2500)[1])
    p_values.append(f_oneway(wd_1400_2500, wd_2500_645)[1])
    p_values.append(f_oneway(wd_2500_645, wd_645_1400)[1])
    return [round(i, 3) for i in p_values]


def draw_line_chart(x, y, y_limit_bottom=0.0, y_limit_top=60.0,
                    x_limit_left=0, x_limit_right=320,
                    x_axis_label=None,
                    y_axis_label=None, legend=None, title=None):
    plt.figure(figsize=(6, 3.5))
    if legend:
        plt.plot(x, y, label=legend)
        plt.legend()
    if x_axis_label:
        plt.xlabel(x_axis_label)
    if y_axis_label:
        plt.ylabel(y_axis_label)
    if title:
        plt.title(title)
    plt.ylim([y_limit_bottom, y_limit_top])
    plt.xlim([x_limit_left, x_limit_right])
    plt.tight_layout()
    plt.show()


def plot_mds(mds_matrix, title, color, index):
    x = mds_matrix[:, 0]
    y = mds_matrix[:, 1]
    ax = plt.subplot(1, 3, index)
    ax.scatter(x, y, label=title, c=color)
    ax.legend()
    ax.set_title(title)
    plt.tight_layout()


def get_distribution_distance(data, distance, total_subjects, reverse=False):
    if reverse:
        total_count = len(list(filter(lambda score: score >= distance, data)))
    else:
        total_count = len(list(filter(lambda score: score <= distance, data)))
    percentage = (total_count / total_subjects) * 100
    return f"Distance: {distance:3d}, number of subjects: {total_count:3d}, percentage: {percentage:.2f}%"


if __name__ == "__main__":
    distances_between_cohorts_data_file = "output/distances_between_cohorts_ws.json"
    mds_mx645_data_file = "output/mds_mx645_ws.json"
    mds_mx1400_data_file = "output/mds_mx1400_ws.json"
    mds_std2500_data_file = "output/mds_std2500_ws.json"
    with open(distances_between_cohorts_data_file) as fp:
        distance_between_cohorts = json.load(fp)
        wd_645_1400 = [distance[0] for distance in distance_between_cohorts]
        wd_1400_2500 = [distance[1] for distance in distance_between_cohorts]
        wd_2500_645 = [distance[2] for distance in distance_between_cohorts]

    t_values = get_t_values(wd_645_1400, wd_1400_2500, wd_2500_645)
    print("T-values:")
    print(t_values)
    p_values = get_p_values(wd_645_1400, wd_1400_2500, wd_2500_645)
    print("P-values:")
    print(p_values)
    p_value = get_anova_p_value(wd_645_1400, wd_1400_2500, wd_2500_645)
    p_value = round(p_value, 3)
    print(f"ANOVA test p-value: {p_value}")

    mean_wd_645_1400 = round(mean(wd_645_1400), 3)
    print(f"Mean WD_MX645_MX1400: {mean_wd_645_1400}")
    mean_wd_1400_2500 = round(mean(wd_1400_2500), 3)
    print(f"Mean WD_MX1400_STD2500: {mean_wd_1400_2500}")
    mean_wd_2500_645 = round(mean(wd_2500_645), 3)
    print(f"Mean WD_STD2500_MX645: {mean_wd_2500_645}")
    distance_2 = get_distribution_distance(wd_645_1400, 2, 316)
    distance_5 = get_distribution_distance(wd_645_1400, 5, 316)
    distance_10 = get_distribution_distance(wd_645_1400, 10, 316, True)
    print(f"WD_MX645_MX1400: {distance_2}")
    print(f"WD_MX645_MX1400: {distance_5}")
    print(f"WD_MX645_MX1400: {distance_10}")

    subject_numbers = [i for i in range(1, 317)]
    # WD_mx645_mx1400
    draw_line_chart(subject_numbers, wd_645_1400, 0, 60, 0, 320,
                    "Subject ID", "Distance", "WD(mx645 - mx1400)")  #
    # WD_mx1400_std2500
    draw_line_chart(subject_numbers, wd_1400_2500, 0, 60, 0, 320,
                    "Subject ID", "Distance", "WD(mx1400 - std2500)")
    # WD_std2500_mx645
    draw_line_chart(subject_numbers, wd_2500_645, 0, 60, 0, 320,
                    "Subject ID", "Distance", "WD(std2500 - mx645)")

    with open(mds_mx645_data_file) as fp:
        mds_mx645 = np.array(json.load(fp))
    with open(mds_mx1400_data_file) as fp:
        mds_mx1400 = np.array(json.load(fp))
    with open(mds_std2500_data_file) as fp:
        mds_std2500 = np.array(json.load(fp))

    title = f'mx645'
    plot_mds(mds_mx645, title, "red", 1)
    title = f'mx1400'
    plot_mds(mds_mx1400, title, "green", 2)
    title = f'std2500'
    plot_mds(mds_std2500, title, "purple", 3)
    plt.tight_layout()
    plt.show()