import os


test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
# file_name = 'plan_l.pdf'
# file_name = 'plan_p.pdf'
# file_name = 'article.pdf'
# file_name = 'document.pdf'
pdf_name = 'con docs2.pdf'
# file_name = 'con docs2_sliced.pdf'
pdf_path = os.path.join(test_data_dir, pdf_name)
img_path  = os.path.join(test_data_dir, pdf_name)


__all__ = ['pdf_path', 'test_data_dir']
