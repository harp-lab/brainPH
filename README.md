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

### References

- [Rips complex user manual](https://gudhi.inria.fr/python/latest/rips_complex_user.html)
- [Wasserstein distance user manual](https://gudhi.inria.fr/python/3.3.0/wasserstein_distance_user.html)
- [Bottleneck docs](https://gudhi.inria.fr/python/latest/bottleneck_distance_user.html)
- [ANOVA test using scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html)
- [T-test using scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html#scipy.stats.ttest_rel)