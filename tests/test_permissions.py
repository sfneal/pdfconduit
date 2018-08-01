import os
from pdfwatermarker import info


def main():
    password = 'baz'
    directory = '/Users/Stephen/Desktop/pdfs'
    for i in os.listdir(directory):
        print(i)
        s = info.security_objects(os.path.join(directory, i), password)
        print(s)
        for k, v in s:
            print("{0:20} ---> {1}".format(k, v))
        print('\n')


if __name__ == '__main__':
    main()