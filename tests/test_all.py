import os
from databasetools import CSV


directory = os.path.dirname(__file__)


def merge_logs(directory):
    # Merge log files
    logs_dir = os.path.join(directory, 'log')
    log_files = [os.path.join(logs_dir, i) for i in os.listdir(logs_dir) if i.endswith('.csv')]

    master = []
    for i in log_files:
        data = [r for r in CSV.read(i) if all(c.strip() is not None for c in r) and len(r) > 1]
        for d in data:
            print(d)
        master.extend(data)
    master = [m for m in master if m is not None]
    print(len(master))
    w = CSV.write(master, os.path.join(directory, 'master.csv'))
    print(w)


def main():
    test_scripts = [os.path.join(directory, i) for i in os.listdir(directory)
                    if not i.startswith('.') and os.path.isfile(i) and 'all' not in i and i != '__init__.py']

    for i in test_scripts:
        print(i)
        m = str('tests.' + os.path.basename(i).strip('.py'))
        command = 'python -m unittest ' + m
        os.system(command)

    merge_logs(directory)


if __name__ == '__main__':
    merge_logs(directory)
