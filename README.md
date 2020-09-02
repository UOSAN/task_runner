# task runner
Task runner runs the complete set of
[partial permutations](https://en.wikipedia.org/wiki/Permutation#k-permutations_of_n)
of a given set of tasks. The set is run in a random order.

## How to use
```
python3 task_runner.py --task-path /Users/user/task1.py /Users/user/task2.py /Users/user/task3.py --num 2
```

### Arguments
```
--task-path [task1] [task2] ...
```
A space separated list of paths to the tasks. Tasks are assumed to be
implemented using PsychoPy, and have been compiled to Python script form.

```
--num [number]
```
How many tasks to run per block. Blocks are created from the partial
permutations of the task list. For example, with 3 tasks `A`, `B`, and `C` and `--num 2`,
6 blocks will be created and executed in a random order. A possible task
execution order is:
```
AB
CB
BC
CA
AC
BA
```
