import json
import statistics

data = []
with open("datasets/random_clusters.txt") as fp:
    lines = [line.strip() for line in fp.readlines() if line.strip() != ""]
    for i in range(0, len(lines), 8):
        ar = []
        for j in range(i, i + 8):
            ar.append(int(lines[j].split("#match: ")[1]))
        data.append(ar)

max_reverse = []
cnt = 0
for ar in data:
    max_value = max(ar)
    max_index = ar.index(max_value)
    max_bin_value = str(bin(max_index))[2:].rjust(3, "0")
    rev_bin_value = ""
    for c in max_bin_value:
        if c == "0":
            rev_bin_value += "1"
        else:
            rev_bin_value += "0"
    rev_index = int(rev_bin_value, 2)
    rev_value = ar[rev_index]
    max_reverse.append(max_value + rev_value)

mean_value = statistics.mean(max_reverse)
std_dev_value = statistics.stdev(max_reverse)
print(f"Mean value of (Max + Rev): {mean_value}")
print(f"Standard deviation value of (Max + Rev): {std_dev_value}")
