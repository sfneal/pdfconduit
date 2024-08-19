class OutputException(Exception):
    message = "Unable to determine PDF output path.  Make a call to `set_output()` prior to `write() when reading from streams and writing to files"
