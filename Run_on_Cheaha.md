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
pip install -r requirements.txt
```
- Create a batch job:
```
#!/bin/bash
#
#SBATCH --job-name=randomdistance
#SBATCH --output=randomdistance_job.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --partition=amd-hdr100
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=4069

# load your Anaconda module here and activate your virtual environment (if needed)
set -e
source /home/ashovon/venvs/brainph/bin/activate

python -u /home/ashovon/brainph/distance_calculation_random.py --method ws --start 1 --end 316 --distance y --mds y
```
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