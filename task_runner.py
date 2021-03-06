import random
import subprocess
import csv
from pathlib import Path

from task_runner_cli import TaskRunnerCli


FIELDNAMES = ['run', 'task_a', 'task_b']

if __name__ == '__main__':
    root_path = Path.home() / 'Desktop' / 'ASH'
    # Map task_name names to paths
    tasks = {'construal level': root_path / 'high_level_construal' / 'construal_level_task.py',
             'ROC': root_path / 'regulation_of_craving' / 'ROC.py',
             'values affirmation': root_path / 'value_affirmation' / 'value_affirmation.py'}

    # List the 6 partial permutations
    block_list = {1: ('construal level', 'ROC'),
                  2: ('construal level', 'values affirmation'),
                  3: ('ROC', 'values affirmation'),
                  4: ('values affirmation', 'construal level'),
                  5: ('ROC', 'construal level'),
                  6: ('values affirmation', 'ROC')}

    cli = TaskRunnerCli()
    task_run_order_path = Path.cwd() / 'run_order' / f'{cli.get_participant_id()}_session_{cli.get_session()}_task_run_order.csv'
    run_order = []

    # If it is a practice session, just run all three tasks.
    is_practice_session = (cli.get_session() == 0)
    if is_practice_session:
        for task_name, task_path in tasks.items():
            p = subprocess.run(['python3', str(task_path),
                                '--id', cli.get_participant_id(),
                                '--session', str(cli.get_session()),
                                '--run', str(1),
                                '--is_first', str(False)],
                               capture_output=True,
                               text=True)
            print(f'Output: {p.stdout}')
            print(f'Error : {p.stderr}')
    else:
        runs_per_task = {'construal level': 0,
                         'ROC': 0,
                         'values affirmation': 0}

        # Read the planned order
        # For example: run_order = [6, 5, 4, 1, 2, 3]
        with open(task_run_order_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                run_order.append(int(row[FIELDNAMES[0]]))

        if cli.restart():
            # Get the tasks that were already run,
            # and use that information to populate which run of each task has been completed.
            # For example: if we want to restart on run 1, then already_run becomes [6, 5, 4]
            already_run = run_order[:run_order.index(cli.get_run())]
            for r in already_run:
                t1 = block_list[r][0]
                t2 = block_list[r][1]
                runs_per_task[t1] += 1
                runs_per_task[t2] += 1

            # Then only run the remaining tasks.
            # For example, run_order is just [1, 2, 3], so we just run the unfinished tasks.
            run_order = run_order[run_order.index(cli.get_run()):]
        else:
            # Run the filler task to allow a fieldmap to be collected
            filler_task = str(root_path / 'filler' / 'filler.py')
            p = subprocess.run(['python3', filler_task],
                               capture_output=True,
                               text=True)
            print(f'Output: {p.stdout}')
            print(f'Error : {p.stderr}')

        # Run the tasks.
        for run in run_order:
            # Run the first task
            task_name = block_list[run][0]
            runs_per_task[task_name] += 1
            p = subprocess.run(['python3', str(tasks[task_name]),
                                '--id', cli.get_participant_id(),
                                '--session', str(cli.get_session()),
                                '--run', str(runs_per_task[task_name]),
                                '--is_first'],
                               capture_output=True,
                               text=True)
            print(f'Output: {p.stdout}')
            print(f'Error : {p.stderr}')

            # Run the second task
            task_name = block_list[run][1]
            runs_per_task[task_name] += 1
            p = subprocess.run(['python3', str(tasks[task_name]),
                                '--id', cli.get_participant_id(),
                                '--session', str(cli.get_session()),
                                '--run', str(runs_per_task[task_name])],
                               capture_output=True,
                               text=True)
            print(f'Output: {p.stdout}')
            print(f'Error : {p.stderr}')
