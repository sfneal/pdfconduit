import os
import datetime
from databasetools import CSV
from synfo import Synfo


directory = os.path.join(os.path.dirname(__file__), 'data')
# file_name = 'plan_l.pdf'
# file_name = 'plan_p.pdf'
# file_name = 'article.pdf'
# file_name = 'document.pdf'
file_name = 'con docs2.pdf'
# file_name = 'con docs2_sliced.pdf'
pdf = os.path.join(directory, file_name)


info = Synfo()


def write_log(file_path, log):
    if os.path.isfile(file_path):
        CSV(file_path).append(log)
    else:
        CSV(file_path).write(log)


def dump_log(test_case=None, time=None, result=None):
    now = datetime.datetime.now()
    date_time = str(now).split('.', 1)[0]
    fname = test_case[0] + '.csv'
    file_path = os.path.join(os.path.dirname(__file__), 'log', fname)

    rows = [date_time, test_case[-2], test_case[-1], file_name, result, str(round(time, 2)), info.python.version,
            info.system.os, info.hardware.processor.cores, info.hardware.memory]
    return rows, file_path


__all__ = ['pdf', 'directory', 'dump_log', 'write_log']
