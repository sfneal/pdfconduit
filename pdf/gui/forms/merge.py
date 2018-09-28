import os
import PySimpleGUI as sg
from pdfconduit import Merge
from pdf.gui.gui import _line
from pdf.utils import open_window


class MergeGUI:
    def __init__(self, directory=None):
        self.directory = directory
        self.run()

    def run(self):
        # Select directory if not already set
        if not self.directory or not os.path.isdir(self.directory):
            self.directory = sg.PopupGetFolder('Select a folder with PDF files')

        # Create list of full file paths in directory
        file_paths = [os.path.join(self.directory, fname) for fname in os.listdir(self.directory)
                      if os.path.isfile(os.path.join(self.directory, fname))
                      and not fname.startswith('.')
                      and fname.endswith('.pdf')]

        # Raise error if no PDF file are found
        if not len(file_paths) > 0:
            sg.PopupError('Unable to find PDF files to merge')

        # Set listbox height (limit in case of large number of files in folder)
        listbox_h = len(file_paths) if len(file_paths) < 15 else 15

        # Display form
        window = sg.Window('PDF Merger', default_element_size=(80, 1), grab_anywhere=False)
        layout = [
            [sg.Text('PDF File Merger', size=(20, 1), font=("Helvetica", 25))],

            # Multi-selectable file list box
            [sg.Text('Select the PDF files you would like to merge', size=(40, 1), font=("Helvetica", 16))],
            [sg.Listbox(values=file_paths, size=(80, listbox_h), key='pdf_files', select_mode='multiple')],
            [_line()],

            # Destination folder
            [sg.Text('Choose a destination folder', size=(40, 1), font=("Helvetica", 16))],
            [sg.Text('Folder', size=(10, 1), auto_size_text=False, justification='left'),
             sg.InputText(os.path.dirname(file_paths[0]), key='folder', do_not_clear=True, size=(60, 1)),
             sg.FolderBrowse()],
            [_line()],

            # Destination filename
            [sg.Text('Choose a merged pdf filename', size=(40, 1), font=("Helvetica", 16))],
            [sg.Text('File', size=(10, 1), auto_size_text=False, justification='left'),
             sg.InputText('merged', key='file', do_not_clear=True, size=(65, 1))],
            [_line()],

            [sg.Submit('Merge'), sg.Cancel()]
        ]

        button, values = window.LayoutAndRead(layout)
        m = Merge(values['pdf_files'], output_name=values['file'], output_dir=values['folder'])
        open_window(m.file)


def main():
    MergeGUI().run()


if __name__ == '__main__':
    main()
