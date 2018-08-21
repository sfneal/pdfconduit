import os
import PySimpleGUI as gui
from pdfconduit import __version__
from pdfconduit.utils import available_images


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


class GUI:
    @staticmethod
    def encrypt():
        from pdfconduit.encrypt import Encrypt

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
            with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source folder', size=(label_w, 1), auto_size_text=False),
                     gui.InputText(params['pdf'], size=(30, 1)),
                     gui.FolderBrowse(button_text='Folder')],

                    [_line()],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndShow(layout)

            params['pdf'] = values[0]
            return params

        def settings(p):
            with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source PDF file', size=(label_w, 1), auto_size_text=False), gui.InputText(p['pdf']),
                     gui.FileBrowse(button_text='File', file_types=(("PDF Files", "*.pdf"),)),
                     gui.SimpleButton('Folder')],

                    [_line()],

                    # Encryption
                    [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
                    [gui.Text('User Password', size=(label_w, 1), auto_size_text=False), gui.InputText()],
                    [gui.Text('Owner Password', size=(label_w, 1), auto_size_text=False), gui.InputText()],
                    [gui.Checkbox('128 bit encryption', default=True)],
                    [gui.Checkbox('Allow Printing', default=True), gui.Checkbox('Allow Commenting', default=False)],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndShow(layout)

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

    @staticmethod
    def watermark():
        from pdfconduit.utils import Receipt
        from pdfconduit.watermark import Watermark

        label_w = 20
        title = 'PDF Watermarker'

        def header():
            return [[gui.Text('HPA Design', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('PDF Watermark utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('version: ' + __version__, size=(30, 1), font=("Helvetica", 16), text_color='blue')],
                    [_line()]]

        def footer(message='Click Submit to watermark PDF'):
            return [[gui.Text(message)], [gui.Submit(), gui.Cancel()]]

        def folder(params):
            with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source folder', size=(label_w, 1), auto_size_text=False),
                     gui.InputText(params['pdf'], size=(30, 1)),
                     gui.FolderBrowse(button_text='Folder')],

                    [_line()],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndShow(layout)

            params['pdf'] = values[0]
            return params

        def settings(params):
            # Fix opacity if it is adjusted$
            if params['opacity'] < 1:
                params['opacity'] = int(params['opacity'] * 100)

            """GUI window for inputing Watermark parameters"""
            with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:

                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source file or folder', size=(label_w, 1), auto_size_text=False),
                     gui.InputText(params['pdf'], size=(30, 1)),
                     gui.FileBrowse(button_text='File', file_types=(("PDF Files", "*.pdf"),)),
                     gui.SimpleButton('Folder')],

                    [_line()],

                    # Files and non-empty-folders
                    [gui.Text('Project address', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Address', size=(label_w, 1), auto_size_text=False), gui.InputText(params['address'])],
                    [gui.Text('Town', size=(label_w, 1), auto_size_text=False), gui.InputText(params['town'])],
                    [gui.Text('State', size=(label_w, 1), auto_size_text=False), gui.InputText(params['state'])],

                    [_line()],

                    [gui.Text('Watermark Settings', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Logo Image', size=(label_w, 1), auto_size_text=False),
                     gui.InputCombo(values=(params['image']), size=(30, 4))],

                    [gui.Text('File Compression', size=(label_w, 1), auto_size_text=False),
                     gui.Radio('Uncompressed', "RADIO1", default=params['compression']['uncompressed']),
                     gui.Radio('Compressed', "RADIO1", default=params['compression']['compressed'])],

                    [gui.Text('Watermark Flattening', size=(label_w, 1), auto_size_text=False),
                     gui.Radio('Flattened', "RADIO3", default=params['flattening']['flattened']),
                     gui.Radio('Layered', "RADIO3", default=params['flattening']['layered'])],
                    [gui.Text('Watermark Placement', size=(label_w, 1), auto_size_text=False),
                     gui.Radio('Overlay', "RADIO2", default=params['placement']['overlay']),
                     gui.Radio('Underneath', "RADIO2", default=params['placement']['underneath'])],

                    [gui.Text('Opacity', size=(label_w, 1), auto_size_text=False),
                     gui.Slider(range=(1, 20), orientation='h', size=(34, 30), default_value=params['opacity'])],

                    [_line()],

                    # Encryption
                    [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
                    [gui.Checkbox('Encrypt', default=params['encrypt']),
                     gui.Checkbox('Allow Printing', default=params['allow_printing']),
                     gui.Checkbox('Allow Commenting', default=params['allow_commenting'])],
                    [gui.Text('User Password', size=(label_w, 1), auto_size_text=False), gui.InputText(params['user_pw'])],
                    [gui.Text('Owner Password', size=(label_w, 1), auto_size_text=False), gui.InputText(params['owner_pw'])],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndShow(layout)

            params['pdf'] = values[0]
            params['address'] = values[1]
            params['town'] = values[2]
            params['state'] = values[3]
            params['image'] = values[4]
            params['compression']['uncompressed'] = values[5]
            params['compression']['compressed'] = values[6]
            params['flattening']['flattened'] = values[7]
            params['flattening']['layered'] = values[8]
            params['placement']['overlay'] = values[9]
            params['placement']['underneath'] = values[10]
            params['opacity'] = float(values[11] * .01)
            params['encrypt'] = values[12]
            params['allow_printing'] = values[13]
            params['allow_commenting'] = values[14]
            params['user_pw'] = values[15] if len(values[15]) > 0 else ''
            params['owner_pw'] = values[16] if len(values[16]) > 0 else ''
            if button == 'Folder':
                params = folder(params)
                params = settings(params)

            return params

        params = {
            'pdf': '',
            'address': '',
            'town': '',
            'state': '',
            'image': available_images(),
            'compression': {
                'uncompressed': True,
                'compressed': False
            },
            'flattening': {
                'flattened': True,
                'layered': False,
            },
            'placement': {
                'overlay': True,
                'underneath': False
            },
            'opacity': 8,
            'encrypt': True,
            'allow_printing': True,
            'allow_commenting': False,
            'user_pw': '',
            'owner_pw': '',
        }

        params = settings(params)

        if os.path.isfile(params['pdf']):
            params['pdf'] = [params['pdf']]
        elif os.path.isdir(params['pdf']):
            src_dir = params['pdf']
            params['pdf'] = [os.path.join(src_dir, pdf) for pdf in os.listdir(src_dir) if pdf.endswith('.pdf')]

        receipt = Receipt(gui=True)
        receipt.set_dst(params['pdf'][0])

        for pdf in params['pdf']:
            # Execute Watermark class
            wm = Watermark(pdf, receipt=receipt, progress_bar='gui', progress_bar_enabled=True)
            wm.draw(text1=params['address'],
                    text2=str(params['town'] + ', ' + params['state']),
                    image=params['image'],
                    opacity=params['opacity'],
                    compress=params['compression']['compressed'],
                    flatten=params['flattening']['flattened'])
            wm.add(underneath=params['placement']['underneath'], method='pdfrw')
            if params['encrypt']:
                wm.encrypt(params['user_pw'], params['owner_pw'])
        wm.cleanup()

        print('\nSuccess!')

