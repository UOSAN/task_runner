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
Example: `--run 3`.

### Output
The application will write out to the terminal window the planned task run order. For example:
```
# Planned order for subject ASH999 during session 2:
Run 6, values affirmation, ROC
Run 4, values affirmation, construal level
Run 2, construal level, values affirmation
Run 3, ROC, values affirmation
Run 1, construal level, ROC
Run 5, ROC, construal level
```
It will also write this information to a CSV file named `[participant identifier]_session_[session number]_task_run_order.csv`,
e.g. `ASH999_session_2_task_run_order.csv`.  Then it will start running tasks.
If you want to restart from run 2 (because you were forced to end in the middle of
that run), then add a `--run [run number]` argument to the command line, e.g.
```
python3 task_runner.py --id ASH999 --session 2 --run 2
```
It will read the planned run order from the CSV file written initially, then will execute
starting from run 2. In our example, runs 2, 3, 1, 5 will be run.

#### Prerequisites
Install psychopy as a Python module, by running `pip3 install psychopy`.