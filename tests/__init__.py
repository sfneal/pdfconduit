import os

test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
# pdf_name = 'plan_l.pdf'
# pdf_name = 'plan_p.pdf'
# pdf_name = 'article.pdf'
pdf_name = 'document.pdf'
# pdf_name = 'con docs2.pdf'
img_name = 'floor plan.png'
pdf_path = os.path.join(test_data_dir, pdf_name)
img_path = os.path.join(test_data_dir, img_name)

__all__ = ['pdf_path', 'img_path', 'test_data_dir']
