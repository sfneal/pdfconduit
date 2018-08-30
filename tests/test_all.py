import os


def main():
    print(__file__)
    directory = os.path.dirname(__file__)
    test_scripts = [os.path.join(directory, i) for i in os.listdir(directory)
                    if not i.startswith('.') and os.path.isfile(i) and i != 'test_all.py' and i != '__init__.py']

    for i in test_scripts:
        print(i)
        m = str('tests.' + os.path.basename(i).strip('.py'))
        command = 'python -m unittest ' + m
        os.system(command)


if __name__ == '__main__':
    main()
