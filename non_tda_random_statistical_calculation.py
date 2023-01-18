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
    return [round(i, 6) for i in t_values]


def get_p_values(wd_645_1400, wd_1400_2500, wd_2500_645):
    p_values = []
    p_values.append(f_oneway(wd_645_1400, wd_1400_2500)[1])
    p_values.append(f_oneway(wd_1400_2500, wd_2500_645)[1])
    p_values.append(f_oneway(wd_2500_645, wd_645_1400)[1])
    return [round(i, 6) for i in p_values]


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


def draw_boxplots(labels, data, colors, x_axis_label=None, y_axis_label=None):
    plt.figure(figsize=(6, 3.5))
    bp = plt.boxplot(data, notch=True, vert=True,
                     patch_artist=True,
                     labels=labels,
                     medianprops={"color": "black"})
    if x_axis_label:
        plt.xlabel(x_axis_label)
    if y_axis_label:
        plt.ylabel(y_axis_label)

    for box, color in zip(bp['boxes'], colors):
        box.set_facecolor(color)
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
    distances_between_cohorts_data_file = "output_non_tda_random/distances_between_cohorts_ed.json"
    mds_mx645_data_file = "output_non_tda_random/mds_mx645_ed.json"
    mds_mx1400_data_file = "output_non_tda_random/mds_mx1400_ed.json"
    mds_std2500_data_file = "output_non_tda_random/mds_std2500_ed.json"
    with open(distances_between_cohorts_data_file) as fp:
        distance_between_cohorts = json.load(fp)
        wd_645_1400 = [distance[0] for distance in distance_between_cohorts]
        wd_1400_2500 = [distance[1] for distance in distance_between_cohorts]
        wd_2500_645 = [distance[2] for distance in distance_between_cohorts]

    t_values = get_t_values(wd_645_1400, wd_1400_2500, wd_2500_645)
    print("T-values:")
    for value in t_values:
        print(f"{value:.6f}", end=" ")
    print("")
    p_values = get_p_values(wd_645_1400, wd_1400_2500, wd_2500_645)
    print("P-values:")
    for value in p_values:
        print(f"{value:.6f}", end=" ")
    print("")
    p_value = get_anova_p_value(wd_645_1400, wd_1400_2500, wd_2500_645)
    p_value = round(p_value, 6)
    print(f"ANOVA test p-value: {p_value:.6f}")
    #
    # mean_wd_645_1400 = round(mean(wd_645_1400), 3)
    # print(f"Mean WD_MX645_MX1400: {mean_wd_645_1400}")
    # mean_wd_1400_2500 = round(mean(wd_1400_2500), 3)
    # print(f"Mean WD_MX1400_STD2500: {mean_wd_1400_2500}")
    # mean_wd_2500_645 = round(mean(wd_2500_645), 3)
    # print(f"Mean WD_STD2500_MX645: {mean_wd_2500_645}")
    # distance_2 = get_distribution_distance(wd_645_1400, 2, 316)
    # distance_5 = get_distribution_distance(wd_645_1400, 5, 316)
    # distance_10 = get_distribution_distance(wd_645_1400, 10, 316, True)
    # print(f"WD_MX645_MX1400: {distance_2}")
    # print(f"WD_MX645_MX1400: {distance_5}")
    # print(f"WD_MX645_MX1400: {distance_10}")
    #
    # subject_numbers = [i for i in range(1, 317)]
    # # WD_mx645_mx1400
    # draw_line_chart(subject_numbers, wd_645_1400, 0, 60, 0, 320,
    #                 "Subject ID", "Distance", "WD(mx645 - mx1400)")
    # boxplot_data = [wd_645_1400, wd_1400_2500, wd_2500_645]
    # boxplot_labels = ["WD(645ms-1400ms)", "WD(1400ms-2500ms)",
    #                   "WD(2500ms-645ms)"]
    # boxplot_colors = ['orangered', 'lightblue', 'lightgreen']
    # draw_boxplots(boxplot_labels, boxplot_data, boxplot_colors,
    #               "Distributions",
    #               "Distance")
    # # WD_mx1400_std2500
    # draw_line_chart(subject_numbers, wd_1400_2500, 0, 60, 0, 320,
    #                 "Subject ID", "Distance", "WD(mx1400 - std2500)")
    # # WD_std2500_mx645
    # draw_line_chart(subject_numbers, wd_2500_645, 0, 60, 0, 320,
    #                 "Subject ID", "Distance", "WD(mx1400 - std2500)")
    #
    # with open(mds_mx645_data_file) as fp:
    #     mds_mx645 = np.array(json.load(fp))
    # with open(mds_mx1400_data_file) as fp:
    #     mds_mx1400 = np.array(json.load(fp))
    # with open(mds_std2500_data_file) as fp:
    #     mds_std2500 = np.array(json.load(fp))
    #
    # title = f'mx645'
    # plot_mds(mds_mx645, title, "red", 1)
    # title = f'mx1400'
    # plot_mds(mds_mx1400, title, "green", 2)
    # title = f'std2500'
    # plot_mds(mds_std2500, title, "purple", 3)
    # plt.tight_layout()
    # plt.show()
