import argparse
import itertools
import numpy.random
import subprocess
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
                            default=[str(path / 'value_affirmation.py'),
                                     str(path / 'ROC.py'),
                                     str(path / 'construal_level_task.py')],
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


if __name__ == '__main__':
    # Go get the tasks
    cli = TaskRunnerCli(path=Path.home())

    # Permute them
    block_list = list(itertools.permutations(cli.get_task_paths(), r=cli.get_number()))
    numpy.random.default_rng().shuffle(block_list)

    # Write out expected task run order
    output_path = Path.cwd() / f'{cli.get_participant_id()}_{int(datetime.now().timestamp())}_task_run_order.txt'
    with open(output_path, mode='w') as f:
        f.write('# Planned task run order:\n')
        for block in block_list:
            for task in block:
                f.write(Path(task).name + '\n')

    # Run the tasks.
    for block in block_list:
        # Wait between blocks?
        # Log task run order?
        for task in block:
            p = subprocess.run(['python3', task])
            print(f'Output: {p.stdout}')
            print(f'Error : {p.stderr}')
