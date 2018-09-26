import os
import shutil
from time import sleep

USERNAME = 'stephenneal'
PASSWORD = 'pythonstealth19'

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pdf', 'convert'))
DST_PATH = os.path.join(os.path.dirname(__file__), 'pdf', 'convert')


def sync_folder(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main():
    print('Creating ~~convert~~ source distribution')
    sync_folder(SRC_PATH, DST_PATH)
    os.chdir(os.path.dirname(__file__))
    os.system('python setup.py sdist')
    sleep(1)
    os.system(str('twine upload -u ' + USERNAME + ' -p ' + PASSWORD + ' dist/*'))


if __name__ == '__main__':
    main()
