import os
from time import sleep

USERNAME = 'stephenneal'
PASSWORD = 'pythonstealth19'


def main():
    os.chdir(os.path.dirname(__file__))
    os.system('python setup.py sdist')
    sleep(1)
    os.system(str('twine upload -u ' + USERNAME + ' -p ' + PASSWORD + ' dist/*'))


if __name__ == '__main__':
    main()
