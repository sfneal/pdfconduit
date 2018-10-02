import os
import PySimpleGUI as gui
import json
from pdf.conduit._version import __version__


def _read_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
    with open(config_path, 'r') as cp:
        config = json.load(cp)
    return config


HEADER = _read_config()["global_header"]


def get_directory():
    with gui.FlexForm('Source Directory') as form:
        form_rows = [
            [gui.Text('Enter the Source folders')],
            [gui.Text('Destination Folder', size=(15, 1), justification='right'), gui.InputText('Dest'), gui.FolderBrowse()],
            [gui.Submit(), gui.Cancel()]]

        button, (source) = form.LayoutAndRead(form_rows)
        return source[0]


def get_file():
    with gui.FlexForm('Source File') as form:
        form_rows = [
            [gui.Text('Select a source file')],
            [gui.Text('Source File', size=(15, 1), justification='right'), gui.InputText(),
             gui.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
            [gui.Submit(), gui.Cancel()]]

        button, (source) = form.LayoutAndRead(form_rows)
        return source[0]


def _line(char='_', width=105, size=(75, 1)):
    return gui.Text(char * width, size=size)


def header(title, global_head=HEADER):
    head = [[gui.Text(title, size=(30, 1), font=("Helvetica", 25), text_color='blue')],
            [gui.Text('version: ' + __version__, size=(30, 1), font=("Helvetica", 16), text_color='blue')],
            [_line()]]
    if global_head:
        head.insert(0, [gui.Text(global_head, size=(30, 1), font=("Helvetica", 25), text_color='blue')])
    return head


class GUI:
    @staticmethod
    def watermark():
        """Wrapper method for WatermarkGUI"""
        from pdf.gui.forms.watermark import WatermarkGUI
        WatermarkGUI()

    @staticmethod
    def merge():
        """Wrapper method for MergeGUI"""
        from pdf.gui.forms.merge import MergeGUI
        MergeGUI()

    @staticmethod
    def flatten():
        """Wrapper method for FlattenGUI"""
        from pdf.gui.forms.flatten import FlattenGUI
        FlattenGUI()

    @staticmethod
    def encrypt():
        from pdfconduit import Encrypt

        title = 'PDF Encryptor'
        label_w = 20

        def header():
            return [[gui.Text('HPA Design', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('PDF Encryption utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('version: ' + __version__, size=(30, 1), font=("Helvetica", 16), text_color='blue')],
                    [_line()]]

        def footer(message='Click Submit to encrypt PDF'):
            return [[gui.Text(message)], [gui.Submit(), gui.Cancel()]]

        def folder(params):
            with gui.FlexForm(title, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source folder', size=(label_w, 1)),
                     gui.InputText(params['pdf'], size=(30, 1)),
                     gui.FolderBrowse(button_text='Folder')],

                    [_line()],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndRead(layout)

            params['pdf'] = values[0]
            return params

        def settings(p):
            with gui.FlexForm(title, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source PDF file', size=(label_w, 1)), gui.InputText(p['pdf']),
                     gui.FileBrowse(button_text='File', file_types=(("PDF Files", "*.pdf"),)),
                     gui.SimpleButton('Folder')],

                    [_line()],

                    # Encryption
                    [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
                    [gui.Text('User Password', size=(label_w, 1)), gui.InputText()],
                    [gui.Text('Owner Password', size=(label_w, 1)), gui.InputText()],
                    [gui.Checkbox('128 bit encryption', default=True)],
                    [gui.Checkbox('Allow Printing', default=True), gui.Checkbox('Allow Commenting', default=False)],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndRead(layout)

            user_pw = values[1] if len(values[1]) > 0 else ''
            owner_pw = values[2] if len(values[2]) > 0 else ''
            params = {
                'pdf': values[0],
                'user_pw': user_pw,
                'owner_pw': owner_pw,
                '128bit': values[3],
                'allow_printing': values[4],
                'allow_commenting': values[5],
            }
            if button == 'Folder':
                params = folder(params)
                params = settings(params)
            return params

        p = {
            'pdf': '',
            'user_pw': '',
            'owner_pw': '',
            '128bit': True,
            'allow_printing': True,
            'allow_commenting': False,
        }

        p = settings(p)

        if os.path.isfile(p['pdf']):
            p['pdf'] = [p['pdf']]
        elif os.path.isdir(p['pdf']):
            src_dir = p['pdf']
            p['pdf'] = [os.path.join(src_dir, pdf) for pdf in os.listdir(src_dir) if pdf.endswith('.pdf')]

        for pdf in p['pdf']:
            e = Encrypt(pdf, p['user_pw'], p['owner_pw'], bit128=p['128bit'], allow_printing=p['allow_printing'],
                        allow_commenting=p['allow_commenting'])
        return str(e)
