from pdfconduit.api.config import ALLOWED_EXTENSIONS, APP_NAME, VERSION


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def base_url(app=APP_NAME, version=VERSION):
    """Create a base URL using application name and version."""
    return "/{0}/api/v{1}".format(app, version)


def construct_url(url):
    """Create an API endpoint by concatenating the base url with specified url."""
    return "{0}/{1}".format(base_url(), url)
