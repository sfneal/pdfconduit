import PySimpleGUI as sg
from pdfconduit import Flatten
from pdf.gui.gui import _line
from pdf.utils import open_window


class FlattenGUI:
    def __init__(self):
        self.run()

    def run(self):
        # Display form
        window = sg.Window('PDF Flattener', default_element_size=(80, 1), grab_anywhere=False)
        layout = [
            [sg.Text('PDF File Flattener', size=(20, 1), font=("Helvetica", 25))],

            # PDF to Flatten
            [sg.Text('Choose a PDF file to flatten', size=(40, 1), font=("Helvetica", 16))],
            [sg.Text('PDF', size=(10, 1), auto_size_text=False, justification='left'),
             sg.InputText('', key='pdf', do_not_clear=True, size=(60, 1)),
             sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
            [_line()],

            [sg.Submit('Flatten'), sg.Cancel()]
        ]

        button, values = window.LayoutAndRead(layout)
        f = Flatten(values['pdf'], progress_bar='gui').save()
        open_window(f)


def main():
    FlattenGUI()


if __name__ == '__main__':
    main()
