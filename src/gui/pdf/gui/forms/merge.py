import os
import PySimpleGUI as sg
from pdfconduit import Merge
from pdf.gui.gui import _line, header
from pdf.utils import open_window


class MergeGUI:
    def __init__(self):
        self.run()

    @staticmethod
    def run():
        # Display form
        layout = []
        layout.extend(header('PDF File Merger'))
        form = [
            # Multi-selectable file list box
            [sg.Text('Select the PDF files you would like to merge', size=(40, 1), font=("Helvetica", 16))],
            [sg.Text('PDF Files', size=(10, 1), auto_size_text=False, justification='left'),
             sg.InputText('', key='folder', do_not_clear=True, size=(60, 1)),
             sg.FilesBrowse(file_types=(("PDF Files", "*.pdf"),), key='pdf_files')],
            [_line()],

            # Destination folder
            [sg.Text('Choose a destination folder', size=(40, 1), font=("Helvetica", 16))],
            [sg.Text('Folder', size=(10, 1), auto_size_text=False, justification='left'),
             sg.InputText('', key='folder', do_not_clear=True, size=(60, 1)),
             sg.FolderBrowse()],
            [_line()],

            # Destination filename
            [sg.Text('Choose a destination filename', size=(40, 1), font=("Helvetica", 16))],
            [sg.Text('File', size=(10, 1), auto_size_text=False, justification='left'),
             sg.InputText('merged', key='file', do_not_clear=True, size=(65, 1))],
            [_line()],

            [sg.Submit('Merge'), sg.Cancel()]
        ]
        layout.extend(form)

        window = sg.Window('PDF Merger', default_element_size=(80, 1), grab_anywhere=False)
        button, values = window.Layout(layout).Read()
        window.Close()

        files = values['pdf_files'].split(';')
        output = values['folder'] if os.path.isdir(values['folder']) else os.path.dirname(files[0])
        m = Merge(files, output_name=values['file'], output_dir=output)
        open_window(m.file)


def main():
    MergeGUI()


if __name__ == '__main__':
    main()
