import json
import csv
import gudhi
import matplotlib.pyplot as plt


def draw_barcode_and_matrix(data, matrix, output_filename):
    plt.rcdefaults()
    fig, ax = plt.subplots(1, 2)
    max_xaxis = sorted([i[1] for i in data], reverse=True)[0]
    y_pos = [i for i in range(len(data))]
    values = [pair[1] for pair in data]
    ax[0].barh(y_pos, values, align='center', height=0.6)
    ax[0].invert_yaxis()
    ax[0].set_xlabel('Delta')
    ax[0].set_title('Persistent barcodes (0 dimensional)')
    ax[0].set_xlim([0, max_xaxis])
    ax[0].bar_label(ax[0].containers[0])
    ax[0].get_yaxis().set_visible(False)
    ax[1].set_title('Adjacency matrix')
    matrix = [["{:.2f}".format(j) for j in ar] for ar in matrix]
    t = ax[1].table(cellText=matrix,
                cellLoc='center',
                rowLoc='center',
                colLoc='center',
                loc='center')
    t.scale(1, 4)
    ax[1].axis('off')
    plt.gcf().set_size_inches(8, 2.5)
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches='tight', dpi=600)
    print(f"Chart exported to: {output_filename}")


def draw_matrix_only(matrix):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    matrix = [["{:.2f}".format(j) for j in ar] for ar in matrix]
    t = ax.table(cellText=matrix,
                cellLoc='center',
                rowLoc='center',
                colLoc='center',
                loc='center')
    t.scale(1, 3)
    ax.axis('off')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    plt.gcf().set_size_inches(6, 2)
    plt.tight_layout()
    output_filename = f'output/barcode_demo/matrix.png'
    plt.savefig(output_filename, bbox_inches='tight', dpi=600)
    print(f"Chart exported to: {output_filename}")


def draw_barcode_only(data, output_filename):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    max_xaxis = sorted([i[1] for i in data], reverse=True)[0]
    y_pos = [i for i in range(len(data))]
    values = [pair[1] for pair in data]
    ax.barh(y_pos, values, height=0.7, align='center')
    ax.invert_yaxis()
    # ax.set_xlabel('Delta')
    # ax.set_title('Persistent barcodes (0 dimensional)')
    ax.set_xlim([0, max_xaxis])
    # ax.bar_label(ax.containers[0])
    ax.get_yaxis().set_visible(False)
    plt.tight_layout()
    plt.gcf().set_size_inches(8, 4)
    plt.savefig(output_filename, bbox_inches='tight', dpi=600)
    print(f"Chart exported to: {output_filename}")


if __name__ == "__main__":
    datafile = "full_data_linear/subject_31_mx645.txt"
    output_filename = f'output_linear/barcode.png'

    with open(datafile, newline='') as f:
        reader = csv.reader(f, delimiter="\t")
        data = []
        for row in reader:
            record = []
            for val in row:
                record.append(float(val.strip()))
            data.append(record)
    max_distance = max(map(max, data))
    rips_complex = gudhi.RipsComplex(distance_matrix=data,
                                     max_edge_length=max_distance)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)
    pd = simplex_tree.persistence()[1:]
    barcodes = [pair[1] for pair in pd]
    barcodes.append([0, max_distance])
    barcodes = sorted(barcodes, key=lambda x: -x[1])
    draw_barcode_only(barcodes, output_filename)
    # draw_barcode_and_matrix(barcodes, data)
    # draw_matrix_only(data)
    # draw_barcode_only(barcodes)

    # diag = simplex_tree.persistence()
    # gudhi.plot_persistence_barcode(diag)
    # plt.show()
