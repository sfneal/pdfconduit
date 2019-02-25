import PySimpleGUI as sg
from pdfconduit import Flatten
from pdf.gui.gui import _line, header
from pdf.utils import open_window


class FlattenGUI:
    def __init__(self):
        self.run()

    @staticmethod
    def run():
        layout = []
        layout.extend(header('PDF File Flattener'))
        form = [
            # PDF to Flatten
            [sg.Text('Choose a PDF file to flatten', size=(40, 1), font=("Helvetica", 16))],
            [sg.Text('PDF', size=(10, 1), auto_size_text=False, justification='left'),
             sg.InputText('', key='pdf', do_not_clear=True, size=(60, 1)),
             sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
            [_line()],

            [sg.Submit('Flatten'), sg.Cancel()]
        ]
        layout.extend(form)

        window = sg.Window('PDF Flattener', default_element_size=(80, 1), grab_anywhere=False)
        button, values = window.Layout(layout).Read()
        window.Close()

        f = Flatten(values['pdf'], progress_bar='gui').save()
        open_window(f)


def main():
    FlattenGUI()


if __name__ == '__main__':
    main()
