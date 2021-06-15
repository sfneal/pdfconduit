import os
from datetime import datetime


class Receipt:
    def __init__(self, use=True, gui=False):
        self.dst = None
        self.use = use
        self.gui = gui
        self.items = []
        self._print = print

        self.add('PDF Watermarker', datetime.now().strftime("%Y-%m-%d %H:%M"))

    def set_dst(self, doc, file_name='watermark receipt.txt'):
        self.dst = os.path.join(os.path.dirname(doc), file_name)
        self.add('Directory', os.path.dirname(doc))
        self.add('PDF', os.path.basename(doc))
        return self

    def add(self, key, value):
        message = str("{0:20}--> {1}".format(key, value))
        if self.use:
            self._print(message)
        self.items.append(message)

    def dump(self):
        exists = os.path.isfile(self.dst)
        with open(self.dst, 'a') as f:
            if exists:
                f.write('*******************************************************************\n')

            for item in self.items:
                f.write(item + '\n')

        print('Success!')
