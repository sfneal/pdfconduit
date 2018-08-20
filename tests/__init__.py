import os


directory = os.path.join(os.path.dirname(__file__), 'data')
# file_name = 'plan_l.pdf'
# file_name = 'plan_p.pdf'
file_name = 'article.pdf'
pdf = os.path.join(directory, file_name)


__all__ = [pdf, directory]
