import subprocess
from datetime import datetime
from pathlib import Path

import numpy.random

from task_runner_cli import TaskRunnerCli


def get_date_string(date_format: str = "%Y_%b_%d_%H%M"):
    return datetime.now().strftime(date_format)


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
    # Shuffle
    run_order = list(range(1, 7))
    numpy.random.default_rng().shuffle(run_order)

    cli = TaskRunnerCli()

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
        # In-scanner session: write out planned order and run the tasks.
        output_path = Path.cwd() / f'{cli.get_participant_id()}_{get_date_string()}_session_{cli.get_session()}_task_run_order.txt'
        with open(output_path, mode='w') as f:
            s = f'# Planned order for subject {cli.get_participant_id()} during session {cli.get_session()}:\n'
            f.write(s)
            print(s, end='')
            for run in run_order:
                s = f'Run {run}, '
                f.write(s)
                print(s, end='')
                for task_name in block_list[run]:
                    s = f'{task_name}, '
                    f.write(s)
                    print(s, end='')
                f.write('\n')
                print()

        # Run the tasks.
        runs_per_task = {'construal level': 0,
                         'ROC': 0,
                         'values affirmation': 0}
        for run in run_order:
            # Run the first task
            task_name = block_list[run][0]
            runs_per_task[task_name] += 1
            p = subprocess.run(['python3', str(tasks[task_name]),
                                '--id', cli.get_participant_id(),
                                '--session', str(cli.get_session()),
                                '--run', str(runs_per_task[task_name]),
                                '--is_first', str(True)],
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
                                '--run', str(runs_per_task[task_name]),
                                '--is_first', str(False)],
                               capture_output=True,
                               text=True)
            print(f'Output: {p.stdout}')
            print(f'Error : {p.stderr}')
