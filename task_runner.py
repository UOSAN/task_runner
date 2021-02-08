import argparse
import itertools
import numpy.random
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List


class TaskRunnerCli:
    def __init__(self, path: Path):
        program_description = 'Run several tasks in a block design, assuming all tasks are Python scripts'
        parser = argparse.ArgumentParser(description=program_description,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--task-path',
                            metavar='Path to tasks',
                            required=False,
                            nargs='*',
                            help='Space separated list of the paths to each task.'
                                 'Example: --task-path /Users/user/task1 /Users/user/task2',
                            default=[str(path / 'value_affirmation' / 'value_affirmation.py'),
                                     str(path / 'down_regulation_of_craving' / 'ROC.py'),
                                     str(path / 'high_level_construal' / 'construal_level_task.py')],
                            dest='task_paths')

        parser.add_argument('--num',
                            metavar='Number of tasks per block',
                            required=False,
                            help='Number of tasks per block'
                                 'Example: --num 2',
                            default=2,
                            type=int,
                            dest='num')

        parser.add_argument('--id',
                            metavar='Participant ID',
                            required=True,
                            help='The participant identifier.'
                                 'Example: --id RS999',
                            type=str,
                            dest='partid'
                            )

        self._args = parser.parse_args()

    def get_task_paths(self) -> List[str]:
        return self._args.task_paths

    def get_number(self) -> int:
        return self._args.num

    def get_participant_id(self) -> str:
        return self._args.partid


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
