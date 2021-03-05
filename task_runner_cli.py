import argparse


class TaskRunnerCli:
    def __init__(self):
        program_description = 'Run several tasks in a block design'
        parser = argparse.ArgumentParser(description=program_description,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--id',
                            metavar='Participant ID',
                            required=True,
                            help='The participant identifier. '
                                 'Example: --id ASH999',
                            type=str,
                            dest='partid'
                            )

        parser.add_argument('--session',
                            metavar='Session number',
                            required=True,
                            help='Session number. Should be 1 or 2. Use session 0 for a practice session. '
                                 'Example: --session 2',
                            default=1,
                            type=int,
                            dest='session')

        parser.add_argument('--run',
                            metavar='Run number',
                            required=False,
                            help='Restart at run number n, from the planned run order. '
                                 'Must be 1, 2, 3, 4, 5 or 6. '
                                 'Example: --run 2',
                            default=0,
                            type=int,
                            dest='restart_run')

        self._args = parser.parse_args()

    def get_participant_id(self) -> str:
        return self._args.partid

    def get_session(self) -> int:
        return self._args.session

    def restart(self) -> bool:
        return self._args.restart_run > 0

    def get_run(self) -> int:
        return self._args.restart_run
