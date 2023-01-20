# Brain Persistent Homology

Using persistent homology and multidimensional scaling on Wasserstein distance
matrix

## Data pre-processing

### Input matrix

- S x C x N x N, where S = #subjects, C = #cohorts, N = #ROIs
- Mat file
- Size: 316 x 3 x 114 x 114
- Three cohorts: mx645, mx1400, std2500

### Data normalization

- Removed NaN values by removing column 24 and row 24 from each 114 x 114
  matrix
- Used correlation coefficients on transposed matrix and then applied square
  root on the 1 - squared distance
- 316 x 3 files, 3 files for each subject
- Each file contains 113 x 113 matrix
- Example: `subject_1_mx645.txt`,
  `subject_1_mx1400.txt`,
  `subject_1_std2500.txt`

## Pipeline 1: Comparison across cohorts

### Persistent homology

- Computed 0-dimensional persistent homology (PH) for all three cohorts of each
  subjects
- Generated 0-dimensional barcodes from calculated PH values with maximum value
  of 1
- To use persistent homology features from Gudhi library set 
  `manual=False` in 
  `get_barcodes_single_subject` method in [distance_calculation.py](distance_calculation.py). Otherwise, set 
  `manual=True` for raw calculation of persistent homology and 
  0-dimensional barcodes.

### Distance calculation

- Computed 1-Wasserstein Distance (WD) between cohorts for each
  subjects from the 0-dimensional barcodes
- For each subject, computed WD on the 0-dimensional barcodes:
    - WD(mx645 - mx1400)
    - WD(mx1400 - std2500)
    - WD(std2500 - mx645)
- Generated 1 JSON file with 316 arrays, each array contains 3 values
- Generated
  file: [distances_between_cohorts_ws.json](output/distances_between_cohorts_ws.json)

## Pipeline 2: Comparison within a cohort

### Persistent homology

- Computed 0-dimensional persistent homology (PH) for all three cohorts of each
  subjects
- Generated 0-dimensional barcodes from calculated PH values with maximum value
  of 1
- To use persistent homology features from Gudhi library set 
  `manual=False` in 
  `get_barcodes_single_subject` method in [distance_calculation.py](distance_calculation.py). Otherwise, set 
  `manual=True` for raw calculation of persistent homology and 
  0-dimensional barcodes.
### Distance matrix (Wasserstein distance)

- Computed 1-Wasserstein Distance (WD) matrix within a cohort separately
- For each cohort, computed WD distance matrix on the 0-dimensional barcodes:
    - WD_matrix(mx645): 316 x 316
    - WD_matrix(mx1400): 316 x 316
    - WD_matrix(std2500): 316 x 316
- Generated 3 JSON files each with 316 x 316 matrix
- Generated files:
    - [distance_matrix_mx645_ws.json](output/distance_matrix_mx645_ws.json)
    - [distance_matrix_mx1400_ws.json](output/distance_matrix_mx1400_ws.json)
    - [distance_matrix_std2500_ws.json](output/distance_matrix_std2500_ws.json)

### Multidimensional scaling (Wasserstein distance)

- Applied classical metric Multidimensional scaling (MDS) with precomputed
  distance (1-Wasserstein)
- Calculated MDS of 2 components for each 1-Wasserstein distance matrix
- Generated 3 JSON files each with 316 x 2 matrix
- Generated files:
    - [mds_mx645_ws.json](output/mds_mx645_ws.json)
    - [mds_mx1400_ws.json](output/mds_mx1400_ws.json)
    - [mds_std2500_ws.json](output/mds_std2500_ws.json)
- Applied Kmeans++ clustering by selecting the number of clusters `n` using
  Silhouette Coefficient.
    - [clustering_ws.json](output/clusters_ws.json)

## Statistical analysis

- Calculate `p-value` using ANOVA test on the [316 x 3] size Wasserstein
  distances between the cohorts
- ANOVA test p-value: 0.133
- Wasserstein distance for the following three pairs: (1) TR=645ms and 
  TR=1400ms, (2) TR=1400ms and TR=2500ms and, (1) TR=2500ms and TR=645ms 
  plotted using box plots: [boxplots](screenshots/distribution_boxplot.png)
- Plot WD distances between:
    - WD for all 316 subjects for mx645 and
      mx1400: [WD_mx645_mx1400](screenshots/WD_mx645_mx1400.png)
    - WD for all 316 subjects for mx1400 and
      std2500: [WD_mx1400_std2500](screenshots/WD_mx1400_std2500.png)
    - WD for all 316 subjects for std2500 and
      mx645: [WD_std2500_mx645](screenshots/WD_std2500_mx645.png)
- Plot MDS value for all three
  cohorts: [mds graph](screenshots/mds_graph_color.png)
- Clustering on the MDS results
    - Wasserstein distance: 
      - Single figure: [clustering_ws](screenshots/clusters_ws.png)
      - mx1400: [clusters_mx1400_ws](screenshots/clusters_mx1400_ws.png)
      - mx645: [clusters_mx645_ws](screenshots/clusters_mx645_ws.png)
      - std2500: [clusters_std2500_ws](screenshots/clusters_std2500_ws.png)

## Local Setup

### Requirements

- Python 3

### Install dependencies

- Clone the repository.
- Open a terminal / powershell in the cloned repository.
- Create a virtual environment and activate it. If you are using Linux / Mac:

```commandline
python3 -m venv venv
source venv/bin/activate
```

Create and activate `venv` in Windows (Tested in Windows 10):

```commandline
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

After activating `venv`, the terminal / powershell will have `(venv)` added to
the prompt.

- Check `pip` version:

```commandline
pip --version
```

It should point to the `pip` in the activated `venv`.

- Install required packages:

```commandline
pip install -r requirements.txt
```

### Run the project:

- Calculate distance between cohorts:

```commandline
python distance_calculation.py --method ws --start 1 --end 316 --distance y --mds n
```

- Calculate MDS within a cohort using WD:

```commandline
python distance_calculation.py --method ws --start 1 --end 316 --distance n --mds y
```

- Calculate both above:

```commandline
python distance_calculation.py --method ws --start 1 --end 316 --distance y --mds y
```

- Draw plots and ANOVA test:

```commandline
python statistical_calculation.py
```

- Generate clusters on the MDS data:

```commandline
python cluster_calculation.py
```

### Results

- Calculating distances between cohorts and MDS within each cohorts:

```
python distance_calculation.py --method ws --start 1 --end 316 --distance y --m
ds y

Calculating barcodes for Subject 1
...
Calculating barcodes for Subject 316
Calculating distances between cohorts for Subject 1
...
Calculating distances between cohorts for Subject 316
Done generating the ws JSON file between cohorts: output/distances_between_cohorts_ws.json
Method compute_distances_between_cohorts executed in 1.3996 seconds

Calculating ws distance matrix of 316 subjects for cohort mx645
Calculating MDS of 316 subjects for cohort mx645
Done generating output/distance_matrix_mx645_ws.json
Done generating output/mds_mx645_ws.json
Method compute_mds_within_a_cohort executed in 72.3580 seconds

Calculating ws distance matrix of 316 subjects for cohort mx1400
Calculating MDS of 316 subjects for cohort mx1400
Done generating output/distance_matrix_mx1400_ws.json
Done generating output/mds_mx1400_ws.json
Method compute_mds_within_a_cohort executed in 68.6565 seconds

Calculating ws distance matrix of 316 subjects for cohort std2500
Calculating MDS of 316 subjects for cohort std2500
Done generating output/distance_matrix_std2500_ws.json
Done generating output/mds_std2500_ws.json
Method compute_mds_within_a_cohort executed in 68.2057 seconds

Method compute_mds_of_all_cohorts executed in 209.2202 seconds

Method main executed in 223.9559 seconds

```

- Running statistical analysis on the generated file:

```commandline
python statistical_calculation.py
ANOVA test p-value: 0.133
T-values:
[0.099, 0.024, 0.451]
P-values:
[0.137, 0.061, 0.561]
Mean WD_MX645_MX1400: 5.494
Mean WD_MX1400_STD2500: 5.11
Mean WD_STD2500_MX645: 5.664
WD_MX645_MX1400: Distance:   2, number of subjects:  28, percentage: 8.86%
WD_MX645_MX1400: Distance:   5, number of subjects: 171, percentage: 54.11%
WD_MX645_MX1400: Distance:  10, number of subjects:  30, percentage: 9.49%
```
- T-values and p-values obtained by pairwise t-tests
comparing the WDs between data cohorts. Since all p-values
are greater than 0.05, the means of WD distributions for each
cohort comparison are statistically similar.

|            |            | t-value | p-value |
|------------|------------|---------|---------|
| WD(P1, P2) | WD(P2, P3) | 0.099   | 0.137   |
| WD(P2, P3) | WD(P3, P1) | 0.024   | 0.061   |
| WD(P3, P1) | WD(P1, P2) | 0.451   | 0.561   |


- Wasserstein distance for the following three pairs: (1) TR=645ms and 
  TR=1400ms, (2) TR=1400ms and TR=2500ms and, (1) TR=2500ms and TR=645ms 
  plotted using box plots:
  ![alt boxplots](screenshots/distribution_boxplot.png)
- WD for all 316 subjects for mx645 and mx1400:
  ![alt WD_mx645_mx1400](screenshots/WD_mx645_mx1400.png)
- WD for all 316 subjects for mx1400 and std2500:
  ![alt WD_mx1400_std2500](screenshots/WD_mx1400_std2500.png)
- WD for all 316 subjects for std2500 and mx645:
  ![alt WD_std2500_mx645](screenshots/WD_std2500_mx645.png)
- MDS graph for all three cohorts using Wasserstein distance:
  ![alt mds](screenshots/mds_graph_color.png)
- Clustering result for all three cohorts using Wasserstein distance:
  ![alt clustering ws](screenshots/clusters_ws.png)
  - mx1400: ![alt clusters_mx1400_ws](screenshots/clusters_mx1400_ws.png)
  - mx645: ![alt clusters_mx645_ws](screenshots/clusters_mx645_ws.png)
  - std2500: ![alt clusters_std2500_ws](screenshots/clusters_std2500_ws.png)

### Generated files:

- [distances_between_cohorts_ws.json](output/distances_between_cohorts_ws.json)
- [distance_matrix_mx645_ws.json](output/distance_matrix_mx645_ws.json)
- [distance_matrix_mx1400_ws.json](output/distance_matrix_mx1400_ws.json)
- [distance_matrix_std2500_ws.json](output/distance_matrix_std2500_ws.json)
- [mds_mx645_ws.json](output/mds_mx645_ws.json)
- [mds_mx1400_ws.json](output/mds_mx1400_ws.json)
- [mds_std2500_ws.json](output/mds_std2500_ws.json)
- [clustering_ws.json](output/clusters_ws.json)

### Clustering results (review update)
- Similarity between clusters:
```commandline
Cluster group: 000: #match: 26
Cluster group: 001: #match: 60
Cluster group: 010: #match: 22
Cluster group: 011: #match: 3
Cluster group: 100: #match: 40
Cluster group: 101: #match: 25
Cluster group: 110: #match: 134
Cluster group: 111: #match: 6

Max + rev = 134 + 60 = 194

Cluster group: 000: #match: {264, 140, 13, 268, 159, 289, 295, 168, 170, 298, 174, 49, 54, 182, 57, 314, 69, 74, 78, 92, 105, 110, 113, 242, 120, 125}
Cluster group: 001: #match: {128, 130, 3, 132, 5, 134, 7, 12, 14, 16, 145, 147, 275, 21, 280, 154, 285, 158, 35, 165, 38, 39, 40, 173, 302, 47, 303, 304, 179, 52, 53, 308, 309, 311, 185, 186, 312, 316, 191, 194, 197, 199, 73, 204, 206, 207, 84, 212, 86, 213, 216, 94, 95, 223, 228, 101, 230, 248, 253, 127}
Cluster group: 010: #match: {256, 9, 10, 266, 273, 18, 274, 277, 23, 163, 292, 37, 45, 301, 307, 181, 315, 60, 80, 208, 82, 87}
Cluster group: 011: #match: {225, 29, 151}
Cluster group: 100: #match: {257, 133, 269, 144, 17, 146, 276, 149, 30, 288, 34, 164, 41, 169, 44, 48, 306, 180, 188, 63, 203, 210, 83, 211, 222, 98, 226, 100, 122, 231, 104, 107, 236, 237, 239, 112, 246, 250, 124, 254}
Cluster group: 101: #match: {6, 263, 270, 20, 150, 152, 282, 162, 291, 171, 176, 178, 51, 58, 66, 67, 77, 90, 220, 93, 232, 111, 118, 249, 252}
Cluster group: 110: #match: {1, 2, 4, 8, 11, 15, 19, 22, 24, 26, 27, 28, 31, 32, 33, 36, 42, 43, 46, 55, 56, 59, 61, 64, 65, 68, 70, 71, 72, 75, 76, 79, 85, 88, 89, 91, 96, 97, 99, 102, 103, 106, 108, 109, 114, 115, 116, 117, 119, 121, 123, 126, 129, 131, 135, 136, 137, 138, 139, 141, 142, 143, 148, 153, 155, 156, 157, 160, 161, 166, 167, 172, 175, 177, 183, 187, 189, 190, 192, 193, 195, 196, 198, 200, 201, 202, 205, 209, 214, 215, 217, 218, 219, 221, 224, 227, 229, 233, 234, 235, 238, 240, 241, 243, 244, 245, 247, 251, 258, 259, 260, 261, 262, 265, 267, 271, 272, 278, 279, 281, 283, 284, 286, 287, 290, 293, 294, 296, 297, 299, 300, 305, 310, 313}
Cluster group: 111: #match: {81, 50, 184, 25, 62, 255}
```
- Adjacency matrix between cluster:
```commandline
# columns: cluster_645[0], cluster_645[1], cluster_1400[0], cluster_1400[1], cluster_2500[0], cluster_2500[1]

111 0 86 25 48 63 
0 205 65 140 174 31 
86 65 151 0 66 85 
25 140 0 165 156 9 
48 174 66 156 222 0 
63 31 85 9 0 94 
```
- Adjacency matrix between cluster (random):
```commandline
# columns: cluster_645[0], cluster_645[1], cluster_1400[0], cluster_1400[1], cluster_2500[0], cluster_2500[1]

150 0 73 77 69 81 
0 166 68 98 78 88 
73 68 141 0 71 70 
77 98 0 175 76 99 
69 78 71 76 147 0 
81 88 70 99 0 169 
```
- Similarity between clusters (random):
```commandline

Cluster group: 000: match: {3, 6, 266, 269, 144, 147, 23, 279, 287, 36, 292, 48, 305, 179, 309, 182, 56, 58, 198, 75, 78, 206, 80, 207, 119, 89, 219, 92, 221, 99, 233, 238, 115, 247, 254}
Cluster group: 001: match: {257, 261, 8, 264, 10, 270, 273, 19, 148, 275, 276, 277, 281, 156, 285, 157, 160, 169, 174, 176, 306, 52, 181, 184, 313, 61, 191, 200, 81, 211, 214, 93, 101, 103, 107, 243, 246, 253}
Cluster group: 010: match: {131, 132, 11, 17, 145, 24, 153, 26, 155, 30, 163, 164, 39, 168, 42, 170, 44, 175, 51, 180, 307, 187, 60, 66, 77, 208, 85, 87, 217, 97, 231, 104, 106, 250}
Cluster group: 011: match: {256, 130, 5, 13, 142, 16, 278, 154, 282, 29, 31, 32, 288, 37, 294, 295, 40, 301, 46, 310, 312, 314, 189, 190, 192, 194, 69, 72, 202, 203, 79, 209, 84, 220, 228, 235, 237, 111, 239, 114, 242, 121, 252}
Cluster group: 100: match: {263, 138, 274, 18, 21, 150, 25, 284, 286, 159, 158, 291, 296, 41, 297, 299, 303, 49, 177, 62, 205, 212, 88, 224, 98, 226, 100, 227, 230, 234, 236, 118, 123, 127, 126, 255}
Cluster group: 101: match: {128, 1, 2, 259, 260, 262, 9, 139, 268, 143, 272, 298, 47, 178, 54, 185, 315, 64, 65, 195, 197, 73, 74, 76, 82, 218, 91, 95, 105, 110, 116, 245}
Cluster group: 110: match: {258, 4, 133, 7, 136, 267, 280, 27, 28, 289, 162, 290, 167, 43, 171, 45, 300, 302, 304, 50, 53, 55, 186, 63, 68, 196, 70, 204, 210, 213, 86, 216, 90, 223, 248, 108, 109, 241, 120, 249, 124, 125}
Cluster group: 111: match: {129, 134, 135, 137, 265, 12, 140, 14, 15, 141, 271, 146, 20, 149, 22, 151, 152, 283, 33, 34, 35, 161, 165, 38, 166, 293, 172, 173, 308, 183, 311, 57, 59, 188, 316, 193, 67, 71, 199, 201, 83, 215, 94, 222, 96, 225, 229, 102, 232, 112, 113, 240, 244, 117, 122, 251}

Cluster group: 000: #match: 35
Cluster group: 001: #match: 38
Cluster group: 010: #match: 34
Cluster group: 011: #match: 43
Cluster group: 100: #match: 36
Cluster group: 101: #match: 32
Cluster group: 110: #match: 42
Cluster group: 111: #match: 56
```

## Non TDA cluster generation (Real data)
### Clustering result (within cohort):
```shell
python non_tda_cluster_calculation.py                                                      
Generated output_non_tda/clusters_mx645_ed.png
Generated output_non_tda/clusters_mx1400_ed.png
Generated output_non_tda/clusters_std2500_ed.png
Generated output_non_tda/clusters_ed.json
Number of clusters in 3 cohorts: [2, 2, 2]

output_non_tda:
Cluster group: 000: #match: 18
Cluster group: 001: #match: 51
Cluster group: 010: #match: 24
Cluster group: 011: #match: 8
Cluster group: 100: #match: 26
Cluster group: 101: #match: 24
Cluster group: 110: #match: 151
Cluster group: 111: #match: 14
Generated output_non_tda/clusters_triplet.json

Adjacency matrix:
output_non_tda:
Rows X Columns: [645 clusters, 1400 clusters, 2500 clusters]
101 0 69 32 42 59 
0 215 50 165 177 38 
69 50 119 0 44 75 
32 165 0 197 175 22 
42 177 44 175 219 0 
59 38 75 22 0 97 

Generated output_non_tda/clusters_adjancency.json
```
- Clustering result for all three cohorts using Euclidean distance (`np.linalg.norm`): 
  - mx645: ![alt clusters_mx645_non_tda](output_non_tda/clusters_mx645_ed.png)
  - mx1400: ![alt clusters_mx1400_non_tda](output_non_tda/clusters_mx1400_ed.png)
  - std2500: ![alt clusters_std2500_non_tda](output_non_tda/clusters_std2500_ed.png)
### Statistical analysis on non tda pipeline (across cohort):
```shell
python non_tda_statistical_calculation.py
T-values:
0.001731 0.000019 0.000000 
P-values:
0.040025 0.006077 0.000004 
ANOVA test p-value: 0.000012
```
- T-values and p-values obtained by pairwise t-tests
comparing the EDs between data cohorts. Since all p-values
are **less** than 0.05, the means of ED distributions for each
cohort comparison are statistically **dissimilar**.


|            |            | t-value  | p-value  |
|------------|------------|----------|----------|
| WD(P1, P2) | WD(P2, P3) | 0.001731 | 0.040025 |
| WD(P2, P3) | WD(P3, P1) | 0.000019 | 0.006077 |
| WD(P3, P1) | WD(P1, P2) | 0.000000 | 0.000004 |

## Non TDA cluster generation (Random data)
### Clustering result (within cohort) (random data):
```shell
Number of clusters in 3 cohorts: [3, 3, 3]
output_non_tda_random:
Cluster group: 000: #match: 0
Cluster group: 001: #match: 24
Cluster group: 002: #match: 11
Cluster group: 010: #match: 13
Cluster group: 011: #match: 0
Cluster group: 012: #match: 23
Cluster group: 020: #match: 24
Cluster group: 021: #match: 11
Cluster group: 022: #match: 0
Cluster group: 100: #match: 0
Cluster group: 101: #match: 19
Cluster group: 102: #match: 13
Cluster group: 110: #match: 11
Cluster group: 111: #match: 0
Cluster group: 112: #match: 29
Cluster group: 120: #match: 21
Cluster group: 121: #match: 13
Cluster group: 122: #match: 0
Cluster group: 200: #match: 0
Cluster group: 201: #match: 25
Cluster group: 202: #match: 15
Cluster group: 210: #match: 12
Cluster group: 211: #match: 0
Cluster group: 212: #match: 15
Cluster group: 220: #match: 23
Cluster group: 221: #match: 14
Cluster group: 222: #match: 0
Generated output_non_tda_random/clusters_triplet.json

Adjacency matrix:
output_non_tda_random:
Rows X Columns: [645 clusters, 1400 clusters, 2500 clusters]
106 0 0 35 36 35 37 35 34 
0 106 0 32 40 34 32 32 42 
0 0 104 40 27 37 35 39 30 
35 32 40 107 0 0 0 68 39 
36 40 27 0 103 0 36 0 67 
35 34 37 0 0 106 68 38 0 
37 32 35 0 36 68 104 0 0 
35 32 39 68 0 38 0 106 0 
34 42 30 39 67 0 0 0 106 

Generated output_non_tda_random/clusters_adjancency.json
```
- Clustering result for random data for all three cohorts using Euclidean distance (`np.linalg.norm`): 
  - mx645: ![alt clusters_mx645_non_tda_random](output_non_tda_random/clusters_mx645_ed.png)
  - mx1400: ![alt clusters_mx1400_non_tda_random](output_non_tda_random/clusters_mx1400_ed.png)
  - std2500: ![alt clusters_std2500_non_tda_random](output_non_tda_random/clusters_std2500_ed.png)
### Statistical analysis on non tda pipeline with random data (across cohort):
```shell
python non_tda_random_statistical_calculation.py
T-values:
0.028809 0.559694 0.124023 
P-values:
0.045081 0.588588 0.155242 
ANOVA test p-value: 0.122310
```
- T-values and p-values obtained by pairwise t-tests
comparing the EDs between data cohorts. Since all p-values
are **equal or larger** than 0.05, the means of ED distributions for each
cohort comparison are statistically **similar**.


|            |            | t-value  | p-value  |
|------------|------------|----------|----------|
| WD(P1, P2) | WD(P2, P3) | 0.028809 | 0.045081 |
| WD(P2, P3) | WD(P3, P1) | 0.559694 | 0.588588 |
| WD(P3, P1) | WD(P1, P2) | 0.124023 | 0.155242 |

### Mean and standard deviation of random clusters (49 out of 50)
```shell
Mean value of (Max + Reverse): 84.06122448979592
Standard deviation value of (Max + Reverse): 5.738786759358441
```

## TDA cluster generation (positive data)
### Clustering result (within cohort):
```shell
Generated output_positive/clusters_mx645_ws.png
Generated output_positive/clusters_mx1400_ws.png
Generated output_positive/clusters_std2500_ws.png
Generated output_positive/clusters_ws.json
Number of clusters in 3 cohorts: [2, 2, 2]
output_positive:
Cluster group: 000: #match: 26
Cluster group: 001: #match: 61
Cluster group: 010: #match: 22
Cluster group: 011: #match: 2
Cluster group: 100: #match: 40
Cluster group: 101: #match: 25
Cluster group: 110: #match: 134
Cluster group: 111: #match: 6
Generated output_positive/clusters_triplet.json

Max + rev = 134 + 61 = 195

Adjacency matrix:
output_positive:
Rows X Columns: [645 clusters, 1400 clusters, 2500 clusters]
111 0 87 24 48 63 
0 205 65 140 174 31 
87 65 152 0 66 86 
24 140 0 164 156 8 
48 174 66 156 222 0 
63 31 86 8 0 94 

Generated output_positive/clusters_adjancency.json

Method main executed in 5.2614 seconds
```
- Clustering result for random data for all three cohorts using Wasserstein distance: 
  - mx645: ![alt clusters_mx645_non_tda_positive](output_positive/clusters_mx645_ws.png)
  - mx1400: ![alt clusters_mx1400_non_tda_positive](output_positive/clusters_mx1400_ws.png)
  - std2500: ![alt clusters_std2500_non_tda_positive](output_positive/clusters_std2500_ws.png)
### Statistical analysis on tda pipeline with positive data (across cohort):
```shell
T-values:
0.092487 0.023553 0.464024 
P-values:
0.129347 0.059304 0.572871 
ANOVA test p-value: 0.128747
```
- T-values and p-values obtained by pairwise t-tests
comparing the WDs between data cohorts. Since all p-values
are **equal or larger** than 0.05, the means of WD distributions for each
cohort comparison are statistically **similar**.


|            |            | t-value  | p-value  |
|------------|------------|----------|----------|
| WD(P1, P2) | WD(P2, P3) | 0.092487 | 0.129347 |
| WD(P2, P3) | WD(P3, P1) | 0.023553 | 0.059304 |
| WD(P3, P1) | WD(P1, P2) | 0.464024 | 0.572871 |

## TDA cluster generation (negative data)
### Clustering result (within cohort):
```shell
Generated output_negative/clusters_mx645_ws.png
Generated output_negative/clusters_mx1400_ws.png
Generated output_negative/clusters_std2500_ws.png
Generated output_negative/clusters_ws.json
Number of clusters in 3 cohorts: [3, 2, 2]
output_negative:
Cluster group: 000: #match: 20
Cluster group: 001: #match: 124
Cluster group: 010: #match: 12
Cluster group: 011: #match: 14
Cluster group: 100: #match: 23
Cluster group: 101: #match: 46
Cluster group: 110: #match: 24
Cluster group: 111: #match: 19
Cluster group: 200: #match: 8
Cluster group: 201: #match: 7
Cluster group: 210: #match: 16
Cluster group: 211: #match: 3
Generated output_negative/clusters_triplet.json

Adjacency matrix:
output_negative:
Rows X Columns: [645 clusters, 1400 clusters, 2500 clusters]
170 0 0 144 26 32 138 
0 112 0 69 43 47 65 
0 0 34 15 19 24 10 
144 69 15 228 0 51 177 
26 43 19 0 88 52 36 
32 47 24 51 52 103 0 
138 65 10 177 36 0 213 

Generated output_negative/clusters_adjancency.json

Method main executed in 5.7617 seconds
```
- Clustering result for random data for all three cohorts using Wasserstein distance: 
  - mx645: ![alt clusters_mx645_non_tda_negative](output_negative/clusters_mx645_ws.png)
  - mx1400: ![alt clusters_mx1400_non_tda_negative](output_negative/clusters_mx1400_ws.png)
  - std2500: ![alt clusters_std2500_non_tda_negative](output_negative/clusters_std2500_ws.png)

### Statistical analysis on tda pipeline with negative data (across cohort):
```shell
python statistical_calculation_positive_negative.py
T-values:
0.000003 0.004331 0.000000 
P-values:
0.000012 0.110220 0.000000 
ANOVA test p-value: 0.000000
```
- T-values and p-values obtained by pairwise t-tests
comparing the WDs between data cohorts. Since all p-values
are **not equal or larger** than 0.05, the means of WD distributions for each
cohort comparison are statistically **dissimilar**.


|            |            | t-value  | p-value  |
|------------|------------|----------|----------|
| WD(P1, P2) | WD(P2, P3) | 0.000003 | 0.000012 |
| WD(P2, P3) | WD(P3, P1) | 0.004331 | 0.110220 |
| WD(P3, P1) | WD(P1, P2) | 0.000000 | 0.000000 |

### Notes
- Within cohort: clustering
- Across cohorts: statistical analysis
- Original dataset: [timeseries.Yeo2011.mm316.mat](full_data/timeseries.Yeo2011.mm316.mat)

### To Do:
- [x] non-TDA experiments for within cohort and comparison across cohort
- [x] nonTDA on random for second pipeline
- [x] create two matrices one for positive values and one for negative values and apply the distance function on them. Since, this will be a lot of experiments, if we do this for everything, let us just start by doing with only pipeline 1 (box plots, p/t-value tests).  the original mat file which we normalized using matlab. 113 x 113 with all positive (padded by 0) and 113 x 113 with all negative (padded by 0).

### References

- [Rips complex user manual](https://gudhi.inria.fr/python/latest/rips_complex_user.html)
- [Wasserstein distance user manual](https://gudhi.inria.fr/python/3.3.0/wasserstein_distance_user.html)
- [Bottleneck docs](https://gudhi.inria.fr/python/latest/bottleneck_distance_user.html)
- [ANOVA test using scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html)
- [T-test using scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html#scipy.stats.ttest_rel)