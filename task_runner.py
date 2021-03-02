import itertools
import numpy.random
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from task_runner_cli import TaskRunnerCli


def get_date_string(date_format: str = "%Y_%b_%d_%H%M"):
    return datetime.now().strftime(date_format)


if __name__ == '__main__':
    # Go get the tasks
    default_path = Path.home() / 'Desktop'
    cli = TaskRunnerCli(path=default_path)

    # Permute them
    block_list = list(itertools.permutations(cli.get_task_paths(), r=cli.get_number()))
    numpy.random.default_rng().shuffle(block_list)

    # Write out expected task run order
    output_path = Path.cwd() / f'{cli.get_participant_id()}_{get_date_string()}_task_run_order.txt'
    with open(output_path, mode='w') as f:
        f.write('# Planned task run order:\n')
        for block in block_list:
            for task in block:
                f.write(Path(task).name + '\n')

    # Run the tasks.
    for block in block_list:
        # Wait between blocks?
        for task in block:
            p = subprocess.run(['python3', task], capture_output=True, text=True)
            if 'can\'t open file' in p.stderr:
                if Path(task).parent == default_path:
                    msg = f'    - Looked in default path: {default_path}.\n'
                else:
                    msg = f'    - Looked in task path: {Path(task).parent}.\n'
                print(f'Unable to find task: {Path(task).name}.\n'
                      f'{msg}'
                      '    - Make sure the path to the task is correct.\n'
                      '    - Make sure the task has been compiled to Python.')
                sys.exit()
            print(f'Output: {p.stdout}')
            print(f'Error : {p.stderr}')
