import os
import PySimpleGUI as gui
from platform import system
from pdfconduit import Watermark, Flatten
from pdf.conduit.lib import available_images
from pdf.utils import Receipt
from pdf.gui.gui import _line, header


LABEL_W = 20
TITLE = 'PDF Watermarker'


DEFAULT_PARAMS = {
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


def view_images():
    from pdf.gui.config.images import view
    view()


class WatermarkGUI:
    def __init__(self):
        self.params = DEFAULT_PARAMS
        self.run()

    @staticmethod
    def footer(message='Click Submit to watermark PDF'):
        return [[gui.Text(message)], [gui.Submit(), gui.Cancel()]]

    def add_image(self):
        from pdf.gui.config.images import add
        with gui.FlexForm(TITLE, default_element_size=(40, 1)) as form:
            inputs = [
                # Source
                [gui.Text('Select an image to add to your PDF Conduit image library', font=('Helvetica', 15),
                          justification='left')],
                [gui.Text('Source image', size=(LABEL_W, 1)),
                 gui.InputText(self.params['pdf'], size=(30, 1)),
                 gui.FileBrowse(button_text='File', file_types=(("PNG Files", "*.png"),))],
                [gui.Text('Image name', size=(LABEL_W, 1)), gui.InputText(size=(30, 1))],

                [_line()],
            ]
            layout = []
            layout.extend(self.header())
            layout.extend(inputs)
            layout.extend(self.footer('Click submit to add your watermark image'))

            (button, (values)) = form.LayoutAndRead(layout)
        name = values[1] if len(values[1]) > 0 else None
        add(values[0], name)

    def input_source(self):
        return [
            # Source
            [gui.Text('Source', font=('Helvetica', 15), justification='left')],
            [gui.Text('Source file or folder', size=(LABEL_W, 1)),
             gui.InputText(self.params['pdf'], size=(30, 1), key='pdf'),
             gui.FileBrowse(button_text='File', file_types=(("PDF Files", "*.pdf"),)),
             gui.SimpleButton('Folder')],
            [_line()],
        ]

    def input_text(self):
        return [
            # Watermark Text
            [gui.Text('Project address', font=('Helvetica', 15), justification='left')],
            [gui.Text('Address', size=(LABEL_W, 1)), gui.InputText(self.params['address'], key='address')],
            [gui.Text('Town', size=(LABEL_W, 1)), gui.InputText(self.params['town'], key='town')],
            [gui.Text('State', size=(LABEL_W, 1)), gui.InputText(self.params['state'], key='state')],

            [_line()],
        ]

    def input_encryption(self):
        return [
            # Encryption
            [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
            [gui.Checkbox('Encrypt', default=self.params['encrypt'], key='encrypt'),
             gui.Checkbox('Allow Printing', default=self.params['allow_printing'], key='allow_printing'),
             gui.Checkbox('Allow Commenting', default=self.params['allow_commenting'], key='allow_commenting')],
            [gui.Text('User Password', size=(LABEL_W, 1)),
             gui.InputText(self.params['user_pw'], key='user_pw')],
            [gui.Text('Owner Password', size=(LABEL_W, 1)),
             gui.InputText(self.params['owner_pw'], key='owner_pw')],

            [_line()],
            [gui.Checkbox('Flatten PDF pages', default=self.params['flat'], key='flat')],
        ]

    def input_watermark_settings(self):
        return [
            # Watermark Settings
            [gui.Text('Watermark Settings', font=('Helvetica', 15), justification='left')],
            [gui.Text('Logo Image', size=(LABEL_W, 1)),
             gui.InputCombo(values=(available_images()), size=(20, 4), key='image'),
             gui.SimpleButton('Add'), gui.SimpleButton('View')],

            [gui.Text('File Compression', size=(LABEL_W, 1)),
             gui.Radio('Uncompressed', "RADIO1", default=self.params['compression']['uncompressed'],
                       key='uncompressed'),
             gui.Radio('Compressed', "RADIO1", default=self.params['compression']['compressed'], key='compressed')],

            [gui.Text('Watermark Flattening', size=(LABEL_W, 1)),
             gui.Radio('Flattened', "RADIO3", default=self.params['flattening']['flattened'], key='flattened'),
             gui.Radio('Layered', "RADIO3", default=self.params['flattening']['layered'], key='layered')],
            [gui.Text('Watermark Placement', size=(LABEL_W, 1)),
             gui.Radio('Overlay', "RADIO2", default=self.params['placement']['overlay'], key='overlay'),
             gui.Radio('Underneath', "RADIO2", default=self.params['placement']['underneath'], key='underneath')],

            [gui.Text('Opacity', size=(LABEL_W, 1)),
             gui.Slider(range=(1, 20), orientation='h', size=(34, 30), default_value=self.params['opacity'],
                        key='opacity')],

            [_line()],
        ]

    def window(self):
        """GUI window for inputing Watermark parameters"""
        platform = system()
        # Tabbed layout for Windows
        if platform is 'Windows':
            with gui.FlexForm(TITLE, default_element_size=(40, 1)) as form:
                with gui.FlexForm(TITLE) as form2:
                    layout_tab_1 = []
                    layout_tab_1.extend(header('PDF Watermark Utility'))
                    layout_tab_1.extend(self.input_source())
                    layout_tab_1.extend(self.input_text())
                    layout_tab_1.extend(self.input_encryption())
                    layout_tab_1.extend(self.footer())

                    layout_tab_2 = []
                    layout_tab_2.extend(self.input_watermark_settings())

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
                layout.extend(header('PDF Watermark Utility'))
                layout.extend(self.input_source())
                layout.extend(self.input_text())
                layout.extend(self.input_watermark_settings())
                layout.extend(self.input_encryption())
                layout.extend(self.footer())
                button, values = form.LayoutAndRead(layout)
                return button, values, platform

    def folder(self):
        with gui.FlexForm(TITLE, default_element_size=(40, 1)) as form:
            inputs = [
                # Source
                [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                [gui.Text('Source folder', size=(LABEL_W, 1)),
                 gui.InputText(self.params['pdf'], size=(30, 1)),
                 gui.FolderBrowse(button_text='Folder')],

                [_line()],
            ]
            layout = []
            layout.extend(header('Watermark utility'))
            layout.extend(inputs)
            layout.extend(self.footer())

            (button, (values)) = form.LayoutAndRead(layout)

        self.params['pdf'] = values[0]
        return self.params

    def settings(self):
        # Fix opacity if it is adjusted$
        if self.params['opacity'] < 1:
            self.params['opacity'] = int(self.params['opacity'] * 100)

        button, values, platform = self.window()

        self.params['pdf'] = values['pdf'] if platform == 'Darwin' else values[0]
        self.params['address'] = values['address'] if platform == 'Darwin' else values[1]
        self.params['town'] = values['town'] if platform == 'Darwin' else values[2]
        self.params['state'] = values['state'] if platform == 'Darwin' else values[3]
        self.params['image'] = values['image'] if platform == 'Darwin' else values[10]
        self.params['compression']['uncompressed'] = values['uncompressed'] if platform == 'Darwin' else values[11]
        self.params['compression']['compressed'] = values['compressed'] if platform == 'Darwin' else values[12]
        self.params['flattening']['flattened'] = values['flattened'] if platform == 'Darwin' else values[13]
        self.params['flattening']['layered'] = values['layered'] if platform == 'Darwin' else values[14]
        self.params['placement']['overlay'] = values['overlay'] if platform == 'Darwin' else values[15]
        self.params['placement']['underneath'] = values['underneath'] if platform == 'Darwin' else values[16]
        self.params['opacity'] = float(values['opacity'] * .01) if platform == 'Darwin' else float(values[17] * .01)

        self.params['encrypt'] = values['encrypt'] if platform == 'Darwin' else values[4]
        self.params['allow_printing'] = values['allow_printing'] if platform == 'Darwin' else values[5]
        self.params['allow_commenting'] = values['allow_commenting'] if platform == 'Darwin' else values[6]
        self.params['user_pw'] = values['user_pw'] if platform == 'Darwin' else values[7]
        if not len(self.params['user_pw']) > 0:
            self.params['user_pw'] = ''
        self.params['owner_pw'] = values['owner_pw'] if platform == 'Darwin' else values[8]
        if not len(self.params['owner_pw']) > 0:
            self.params['owner_pw'] = ''
        self.params['flat'] = values['flat'] if platform == 'Darwin' else values[9]
        if button == 'Folder':
            self.folder()
            self.settings()
        elif button == 'Add':
            self.add_image()
            self.settings()
        elif button == 'View':
            self.view_images()
            self.settings()

    def run(self):
        if system() is not 'Windows':
            gui.SetOptions(background_color='white')

        self.settings()

        if os.path.isfile(self.params['pdf']):
            self.params['pdf'] = [self.params['pdf']]
        elif os.path.isdir(self.params['pdf']):
            src_dir = self.params['pdf']
            self.params['pdf'] = [os.path.join(src_dir, pdf) for pdf in os.listdir(src_dir) if pdf.endswith('.pdf')]

        receipt = Receipt(gui=True)
        receipt.set_dst(self.params['pdf'][0])

        for pdf in self.params['pdf']:
            # Execute Watermark class
            wm = Watermark(pdf, receipt=receipt, progress_bar='gui', progress_bar_enabled=True)
            wm.draw(text1=self.params['address'],
                    text2=str(self.params['town'] + ', ' + self.params['state']),
                    image=self.params['image'],
                    opacity=self.params['opacity'],
                    compress=self.params['compression']['compressed'],
                    flatten=self.params['flattening']['flattened'])
            doc = wm.add(underneath=self.params['placement']['underneath'], method='pdfrw')
            if self.params['flat']:
                doc = Flatten(doc, 2.0, progress_bar='gui', tempdir=wm.tempdir).save()
            if self.params['encrypt']:
                doc = wm.encrypt(self.params['user_pw'], self.params['owner_pw'], document=doc)

        wm.cleanup()

        print('\nSuccess!')


def main():
    WatermarkGUI()


if __name__ == '__main__':
    main()
