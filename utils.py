import random
import csv
import numpy as np
from time import time


def get_adjacency_for_triangle(triangular_matrix, lower=True):
    matrix = []
    data = get_dataset(triangular_matrix)
    if lower:
        data = data[::-1]
    size = len(data) + 1
    for i in range(len(data)):
        row = data[i]
        temp = []
        for j in range(size - len(row) - 1):
            temp.append(matrix[j][i])
        temp.append(0)
        for value in row:
            temp.append(value)
        matrix.append(temp)
    i = size - 1
    temp = []
    for j in range(size - 1):
        temp.append(matrix[j][i])
    temp.append(0)
    matrix.append(temp)
    with open("mod.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(matrix)
    return matrix


def get_simplices(matrix):
    simplices = []
    for i in range(len(matrix)):
        simplices.append(([i], 0))
        for j in range(i + 1, len(matrix[0])):
            simplices.append(([i, j], matrix[i][j]))
    return simplices


def get_dataset(filename='dataset_4_4.csv', v=100, generate=False, fmri=False):
    if generate:
        return generate_large_dataset(v=v, filename=filename)
    data = []
    if fmri:
        with open(filename) as fmri_file:
            fmri_reader = csv.reader(fmri_file, delimiter='\t')
            for line in fmri_reader:
                values = []
                for c in line:
                    if c.strip() != "":
                        val = float(c.strip())
                        if np.isnan(val):
                            val = 0
                        values.append(val)
                data.append(values)
        return data
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            values = [float(c.strip()) for c in line if c.strip() != ""]
            data.append(values)
    return data


def generate_large_dataset(v=100, filename='large_dataset.csv'):
    ar = []
    for i in range(v):
        temp = []
        for j in range(v):
            if i == j:
                temp.append(0)
            elif j < i:
                temp.append(ar[j][i])
            else:
                temp.append(round(random.random(), 2))
        ar.append(temp)
    with open(filename, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(ar)
    return ar


def timer(func):
    def inner(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        total_time = end_time - start_time
        print(f"Method {func.__name__} executed in {total_time:.4f} seconds\n")
        return result

    return inner


@timer
def sample_method(x, y, add=None):
    for i in range(10 ** 6):
        if add == True:
            x += y
        else:
            x -= y
    return x


if __name__ == "__main__":
    z = sample_method(50, 6)
    print(z)

    z = sample_method(5, 6, add=True)
    print(z)
