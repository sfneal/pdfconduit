import os
import sys
from databasetools import CSV


directory = os.path.dirname(__file__)


def merge_logs(directory):
    # Merge log files
    logs_dir = os.path.join(directory, 'log')
    log_files = [os.path.join(logs_dir, i) for i in os.listdir(logs_dir) if i.endswith('.csv')]

    master = []
    for i in log_files:
        data = [r for r in CSV(i).read() if all(c.strip() is not None for c in r) and len(r) > 1]
        for d in data:
            print(d)
        master.extend(data)
    master = [m for m in master if m is not None]
    w = CSV(os.path.join(directory, 'master.csv')).write(master)
    print(w)


def main():
    test_scripts = [os.path.join(directory, i) for i in os.listdir(directory)
                    if not i.startswith('.')
                    and os.path.isfile(i)
                    and i.endswith('.py')
                    and 'all' not in i
                    and i != '__init__.py']

    for i in test_scripts:
        print(i)
        m = str('tests.' + os.path.basename(i).strip('.py'))
        command = sys.executable + ' -m unittest ' + m
        os.system(command)

    merge_logs(directory)


if __name__ == '__main__':
    main()
