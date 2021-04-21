# task runner
Task runner runs the complete set of
[partial permutations](https://en.wikipedia.org/wiki/Permutation#k-permutations_of_n)
for the 3 tasks in the smoking study. The task paths are hard-coded, and have
to be in `Desktop/ASH/high_level_construal`, `Desktop/ASH/regulation_of_craving`, and
`Desktop/ASH/value_affirmation`. It will print out and log to a file the planned order
the tasks will run in.

## How to use
```
python3 task_runner.py --id ASH999 --session 2
```

### Arguments
```
--session [session number]
```
The session number, should be 1 or 2. Required. You can use `--session 0` to run a practice
session that will run all three tasks with a couple of trials in each task.

```
--id [participant identifier]
```
Participant identifier, for logging the task run order. Required. Must be `ASH` followed
by 3 digits. Example: `--id ASH999`.

```
--run [run number]
```
Run number to start. Optional. Should only be used to restart an interrupted scan session.
Each run corresponds to a predefined pair of tasks that the participant will perform.
Example: `--run 3`.

### Output
The run order is pre-generated for each participant and is in a CSV file named `[participant identifier]_session_[session number]_task_run_order.csv`,
e.g. `ASH999_session_2_task_run_order.csv`. After starting task_runner, it will immediately start running tasks.
If you want to restart from run 2 (because you were forced to end in the middle of
that run), then add a `--run [run number]` argument to the command line, e.g.
```
python3 task_runner.py --id ASH999 --session 2 --run 2
```
It will read the planned run order from the CSV file, then will execute
starting from run 2. For example, if the run order is 6, 4, 2, 3, 1, 5,
then runs 2, 3, 1, 5 will be run.

#### Prerequisites
Install psychopy as a Python module, by running `pip3 install psychopy`.

To install psychopy as a Python module on a new computer, you will need
to install some prerequisites. To do this, on macOS, I had to do the following:
1. Install brew (https://brew.sh/)
2. Use brew to install some dependencies: `brew install hdf5 c-blosc git`
3. Install Python3
4. Install PsychoPy as a Python module: `pip3 install psychopy`
5. Remove a troublesome and optional dependency: `pip3 uninstall psychtoolbox`
6. Complete!