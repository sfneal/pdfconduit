__all__ = ['test_encrypt', 'test_encrypt_gui', 'test_merge', 'test_watermark', 'test_watermark_label',
           'test_watermark_encrypt', 'test_watermark_flat', 'test_watermark_gui']


import os


directory = os.path.join(os.path.dirname(__file__), 'data')
file_name = 'plan_l.pdf'
# file_name = 'plan_p.pdf'
file_name = 'document.pdf'
pdf = os.path.join(directory, file_name)


from tests import test_encrypt
from tests import test_encrypt_gui
from tests import test_merge
from tests import test_watermark
from tests import test_watermark_label
from tests import test_watermark_encrypt
from tests import test_watermark_flat
from tests import test_watermark_gui
