import os
import shutil
import inspect

test_data_dir = os.path.join(os.path.dirname(__file__), "data")
# pdf_name = 'plan_l.pdf'
# pdf_name = 'plan_p.pdf'
# pdf_name = 'article.pdf'
pdf_name = "document.pdf"
# pdf_name = 'con docs2.pdf'
img_name = "floor plan.png"
pdf_path = os.path.join(test_data_dir, pdf_name)
img_path = os.path.join(test_data_dir, img_name)


def files_are_equal(file1_path, file2_path):
    """
    Compare two files to check if they are the same.

    Parameters:
    file1_path (str): The path to the first file.
    file2_path (str): The path to the second file.

    Returns:
    bool: True if the files are the same, False otherwise.
    """
    with open(file1_path, "rb") as file1, open(file2_path, "rb") as file2:
        file1_content = file1.read()
        file2_content = file2.read()

    return file1_content == file2_content


def function_name_to_file_name(extension=".pdf"):
    return inspect.stack()[1][3] + extension


def copy_pdf_to_output_directory(pdf, save_name):
    shutil.copy(pdf, get_output_filepath(save_name))


def get_output_filepath(filename):
    return os.path.join(os.path.join(os.path.dirname(__file__), "output"), filename)


def expected_equals_output(test_function, output_filepath):
    return files_are_equal(get_output_filepath(test_function), output_filepath)


# Example usage
# Save outputs to tests/output directory
# copy_pdf_to_output_directory({pdfoutput}, function_name_to_file_name())

# Compare saved outputs to generate pdfs
# expected_equals_output(function_name_to_file_name(), {pdfouput})


__all__ = [
    "pdf_path",
    "img_path",
    "test_data_dir",
    "function_name_to_file_name",
    "copy_pdf_to_output_directory",
    "expected_equals_output",
]
