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
--session [number]
```
The session number, should be 1 or 2. You can use `--session 0` to run a practice
session that will run all three tasks with a couple of trials in each task.

```
--id [participant identifier]
```
Participant identifier, for logging the task run order. Must be in `ASH` followed
by 3 digits. Example: `--id ASH999`.

#### Prerequisites
Install psychopy as a Python module, by running `pip3 install psychopy`.