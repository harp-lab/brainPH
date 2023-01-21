## brainPH on Cheaha
- Open the local directory in terminal.
- Open an SSH connection to Cheaha:
```
ssh ashovon@cheaha.rc.uab.edu
```
- Change directory to the desired directory:
```
cd brainPH
```
- Create a virtual environment to one directory up. 
So, we can pull the current directory to local machine again without the venv files.
```
python3 -m venv ../venvs/brainph
```
- Activate the environment:
```
source ../venvs/brainph/bin/activate
```
- Upgrade pip:
```
pip install --upgrade pip
```
- Install the requirements:
```
pip install -r requirements_cheaha.txt
```
- Create a batch job, for example: [randomdistance.job](randomdistance.job)
- Run the Job in Cheaha:
```
sbatch randomdistance.job
sbatch randomcluster.job
```
- To kill a Slurm job
```
scancel <jobid>
```
You can find your jobid with the following command:
``` 
squeue -u $USER
```
- See the users in a partition:
```
squeue -p amd-hdr100
```
- Check details of a job, (13626634 is the job id):
```
squeue -j 13626634 -o "%all"
```
- See the running scripts for the user:
```
ps aux | grep ashovon
```
- Get a medium instance:
```
srun --ntasks=1 --cpus-per-task=6 --mem-per-cpu=8192 --time=50:00:00 --partition=medium --job-name=fmri --pty /bin/bash
srun --ntasks=4 --cpus-per-task=6 --mem-per-cpu=8192 --time=50:00:00 --partition=medium --job-name=fmri_1400 --pty /bin/bash
```
- Download all files from Cheaha directory to local:
```shell
scp -r ashovon@cheaha.rc.uab.edu:/home/ashovon/brainPH/random_data_1 .
scp -r ashovon@cheaha.rc.uab.edu:/home/ashovon/full_data_positive .
scp -r ashovon@cheaha.rc.uab.edu:/home/ashovon/full_data_negative .
scp -r ashovon@cheaha.rc.uab.edu:/home/ashovon/brainPHmatlab/full_data_linear .
scp -r ashovon@cheaha.rc.uab.edu:/home/ashovon/brainPHmatlab/full_data_positive_linear .
scp -r ashovon@cheaha.rc.uab.edu:/home/ashovon/brainPHmatlab/full_data_negative_linear .
```
- Upload a file from local directory to Cheaha
```shell
scp timeseries.Yeo2011.mm316.mat ashovon@cheaha.rc.uab.edu:/home/ashovon/brainPHmatlab/
```