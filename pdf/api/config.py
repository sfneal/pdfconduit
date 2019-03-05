import os


APP_NAME = 'pdfconduit'
VERSION = 1.0

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

# 16mb max file size
MAX_CONTENT_LENGTH = 16 * (1024 * 1024)

