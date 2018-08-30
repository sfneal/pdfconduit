import os
import shutil
from time import sleep

USERNAME = 'stephenneal'
PASSWORD = 'pythonstealth19'

SRC_PATH1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pdf', 'conduit'))
DST_PATH1 = os.path.join(os.path.dirname(__file__), 'pdf', 'conduit')

SRC_PATH2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pdfconduit'))
DST_PATH2 = os.path.join(os.path.dirname(__file__), 'pdfconduit')

SRC_PATH3 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pdf', 'utils'))
DST_PATH3 = os.path.join(os.path.dirname(__file__), 'pdf', 'utils')


def sync_folder(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main():
    print('Creating ~~conduit~~ source distribution')
    sync_folder(SRC_PATH1, DST_PATH1)
    sync_folder(SRC_PATH2, DST_PATH2)
    sync_folder(SRC_PATH3, DST_PATH3)
    os.chdir(os.path.dirname(__file__))
    os.system('python setup.py sdist')
    sleep(1)
    os.system(str('twine upload -u ' + USERNAME + ' -p ' + PASSWORD + ' dist/*'))


if __name__ == '__main__':
    main()
