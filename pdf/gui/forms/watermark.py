import os
import PySimpleGUI as gui
from platform import system
from pdfconduit import Watermark, Flatten
from pdf.conduit.lib import available_images
from pdf.utils import Receipt
from pdf.conduit._version import __version__
from pdf.gui.gui import HEADER, _line


LABEL_W = 20
TITLE = 'PDF Watermarker'


def header(global_head=HEADER):
    head = [[gui.Text('Watermark utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
            [gui.Text('version: ' + __version__, size=(30, 1), font=("Helvetica", 16), text_color='blue')],
            [_line()]]
    if global_head:
        head.insert(0, [gui.Text(global_head, size=(30, 1), font=("Helvetica", 25), text_color='blue')])
    return head


def footer(message='Click Submit to watermark PDF'):
    return [[gui.Text(message)], [gui.Submit(), gui.Cancel()]]


def folder(params):
    with gui.FlexForm(TITLE, default_element_size=(40, 1)) as form:
        inputs = [
            # Source
            [gui.Text('Source', font=('Helvetica', 15), justification='left')],
            [gui.Text('Source folder', size=(LABEL_W, 1)),
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


def input_source():
    return [
        # Source
        [gui.Text('Source', font=('Helvetica', 15), justification='left')],
        [gui.Text('Source file or folder', size=(LABEL_W, 1)),
         gui.InputText(params['pdf'], size=(30, 1), key='pdf'),
         gui.FileBrowse(button_text='File', file_types=(("PDF Files", "*.pdf"),)),
         gui.SimpleButton('Folder')],
        [_line()],
    ]


def input_text():
    return [
        # Watermark Text
        [gui.Text('Project address', font=('Helvetica', 15), justification='left')],
        [gui.Text('Address', size=(LABEL_W, 1)), gui.InputText(params['address'], key='address')],
        [gui.Text('Town', size=(LABEL_W, 1)), gui.InputText(params['town'], key='town')],
        [gui.Text('State', size=(LABEL_W, 1)), gui.InputText(params['state'], key='state')],

        [_line()],
    ]


def input_watermark_settings():
    return [
        # Watermark Settings
        [gui.Text('Watermark Settings', font=('Helvetica', 15), justification='left')],
        [gui.Text('Logo Image', size=(LABEL_W, 1)),
         gui.InputCombo(values=(available_images()), size=(20, 4), key='image'),
         gui.SimpleButton('Add'), gui.SimpleButton('View')],

        [gui.Text('File Compression', size=(LABEL_W, 1)),
         gui.Radio('Uncompressed', "RADIO1", default=params['compression']['uncompressed'], key='uncompressed'),
         gui.Radio('Compressed', "RADIO1", default=params['compression']['compressed'], key='compressed')],

        [gui.Text('Watermark Flattening', size=(LABEL_W, 1)),
         gui.Radio('Flattened', "RADIO3", default=params['flattening']['flattened'], key='flattened'),
         gui.Radio('Layered', "RADIO3", default=params['flattening']['layered'], key='layered')],
        [gui.Text('Watermark Placement', size=(LABEL_W, 1)),
         gui.Radio('Overlay', "RADIO2", default=params['placement']['overlay'], key='overlay'),
         gui.Radio('Underneath', "RADIO2", default=params['placement']['underneath'], key='underneath')],

        [gui.Text('Opacity', size=(LABEL_W, 1)),
         gui.Slider(range=(1, 20), orientation='h', size=(34, 30), default_value=params['opacity'], key='opacity')],

        [_line()],
    ]


def input_encryption():
    return [
        # Encryption
        [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
        [gui.Checkbox('Encrypt', default=params['encrypt'], key='encrypt'),
         gui.Checkbox('Allow Printing', default=params['allow_printing'], key='allow_printing'),
         gui.Checkbox('Allow Commenting', default=params['allow_commenting'], key='allow_commenting')],
        [gui.Text('User Password', size=(LABEL_W, 1)),
         gui.InputText(params['user_pw'], key='user_pw')],
        [gui.Text('Owner Password', size=(LABEL_W, 1)),
         gui.InputText(params['owner_pw'], key='owner_pw')],

        [_line()],
        [gui.Checkbox('Flatten PDF pages', default=params['flat'], key='flat')],
    ]


def window():
    """GUI window for inputing Watermark parameters"""
    platform = system()
    # Tabbed layout for Windows
    if platform is 'Windows':
        with gui.FlexForm(TITLE, default_element_size=(40, 1)) as form:
            with gui.FlexForm(TITLE) as form2:
                layout_tab_1 = []
                layout_tab_1.extend(header())
                layout_tab_1.extend(input_source())
                layout_tab_1.extend(input_text())
                layout_tab_1.extend(input_encryption())
                layout_tab_1.extend(footer())

                layout_tab_2 = []
                layout_tab_2.extend(input_watermark_settings())

                r = gui.ShowTabbedForm(TITLE, (form, layout_tab_1, 'Document Settings'),
                                       (form2, layout_tab_2, 'Watermark Settings'))
                values = []
                button = None
                for but, result in r:
                    if but is not None:
                        button = but
                    values.extend(result)
                return button, values, platform
    # Standard layout for macOS
    else:
        with gui.FlexForm(TITLE, default_element_size=(40, 1)) as form:
            layout = []
            layout.extend(header())
            layout.extend(input_source())
            layout.extend(input_text())
            layout.extend(input_watermark_settings())
            layout.extend(input_encryption())
            layout.extend(footer())
            button, values = form.LayoutAndRead(layout)
            return button, values, platform


def add_image(params):
    from pdf.gui.config.images import add
    with gui.FlexForm(TITLE, default_element_size=(40, 1)) as form:
        inputs = [
            # Source
            [gui.Text('Select an image to add to your PDF Conduit image library', font=('Helvetica', 15),
                      justification='left')],
            [gui.Text('Source image', size=(LABEL_W, 1)),
             gui.InputText(params['pdf'], size=(30, 1)),
             gui.FileBrowse(button_text='File', file_types=(("PNG Files", "*.png"),))],
            [gui.Text('Image name', size=(LABEL_W, 1)), gui.InputText(size=(30, 1))],

            [_line()],
        ]
        layout = []
        layout.extend(header())
        layout.extend(inputs)
        layout.extend(footer('Click submit to add your watermark image'))

        (button, (values)) = form.LayoutAndRead(layout)
    name = values[1] if len(values[1]) > 0 else None
    add(values[0], name)
    return params


def view_images(params):
    from pdf.gui.config.images import view
    view()
    return params


def settings(params):
    # Fix opacity if it is adjusted$
    if params['opacity'] < 1:
        params['opacity'] = int(params['opacity'] * 100)

    button, values, platform = window()

    params['pdf'] = values['pdf'] if platform == 'Darwin' else values[0]
    params['address'] = values['address'] if platform == 'Darwin' else values[1]
    params['town'] = values['town'] if platform == 'Darwin' else values[2]
    params['state'] = values['state'] if platform == 'Darwin' else values[3]
    params['image'] = values['image'] if platform == 'Darwin' else values[10]
    params['compression']['uncompressed'] = values['uncompressed'] if platform == 'Darwin' else values[11]
    params['compression']['compressed'] = values['compressed'] if platform == 'Darwin' else values[12]
    params['flattening']['flattened'] = values['flattened'] if platform == 'Darwin' else values[13]
    params['flattening']['layered'] = values['layered'] if platform == 'Darwin' else values[14]
    params['placement']['overlay'] = values['overlay'] if platform == 'Darwin' else values[15]
    params['placement']['underneath'] = values['underneath'] if platform == 'Darwin' else values[16]
    params['opacity'] = float(values['opacity'] * .01) if platform == 'Darwin' else float(values[17] * .01)

    params['encrypt'] = values['encrypt'] if platform == 'Darwin' else values[4]
    params['allow_printing'] = values['allow_printing'] if platform == 'Darwin' else values[5]
    params['allow_commenting'] = values['allow_commenting'] if platform == 'Darwin' else values[6]
    params['user_pw'] = values['user_pw'] if platform == 'Darwin' else values[7]
    if not len(params['user_pw']) > 0:
        params['user_pw'] = ''
    params['owner_pw'] = values['owner_pw'] if platform == 'Darwin' else values[8]
    if not len(params['owner_pw']) > 0:
        params['owner_pw'] = ''
    params['flat'] = values['flat'] if platform == 'Darwin' else values[9]
    if button == 'Folder':
        params = folder(params)
        params = settings(params)
    elif button == 'Add':
        params = add_image(params)
        params = settings(params)
    elif button == 'View':
        params = view_images(params)
        params = settings(params)

    return params


def watermark():
    if system() is not 'Windows':
        gui.SetOptions(background_color='white')

    params = {
        'pdf': '',
        'address': '',
        'town': '',
        'state': '',
        'image': None,
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
        'flat': False,
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
        doc = wm.add(underneath=params['placement']['underneath'], method='pdfrw')
        if params['flat']:
            doc = Flatten(doc, 2.0, progress_bar='gui', tempdir=wm.tempdir).save()
        if params['encrypt']:
            doc = wm.encrypt(params['user_pw'], params['owner_pw'], document=doc)

    wm.cleanup()

    print('\nSuccess!')


def main():
    watermark()


if __name__ == '__main__':
    main()
