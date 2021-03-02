from pathlib import Path
import argparse


class TaskRunnerCli:
    def __init__(self, path: Path):
        program_description = 'Run several tasks in a block design, assuming all tasks are Python scripts'
        parser = argparse.ArgumentParser(description=program_description,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--task-path',
                            metavar='Path to tasks',
                            required=False,
                            nargs='*',
                            help='Space separated list of the paths to each task. '
                                 'Example: --task-path /Users/user/task1 /Users/user/task2',
                            default=[str(path / 'value_affirmation' / 'value_affirmation.py'),
                                     str(path / 'down_regulation_of_craving' / 'ROC.py'),
                                     str(path / 'high_level_construal' / 'construal_level_task.py')],
                            dest='task_paths')

        parser.add_argument('--num',
                            metavar='Number of tasks per block',
                            required=False,
                            help='Number of tasks per block. '
                                 'Example: --num 2',
                            default=2,
                            type=int,
                            dest='num')

        parser.add_argument('--id',
                            metavar='Participant ID',
                            required=True,
                            help='The participant identifier. '
                                 'Example: --id RS999',
                            type=str,
                            dest='partid'
                            )

        self._args = parser.parse_args()

    def get_task_paths(self) -> list[str]:
        return self._args.task_paths

    def get_number(self) -> int:
        return self._args.num

    def get_participant_id(self) -> str:
        return self._args.partid
