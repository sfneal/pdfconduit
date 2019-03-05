import os
from pdf.api._version import __version__


APP_NAME = 'pdfconduit'
VERSION = __version__

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

# 16mb max file size
MAX_CONTENT_LENGTH = 16 * (1024 * 1024)

