import PySimpleGUI as gui
from pdfwatermarker import __version__
from pdfwatermarker.watermark.draw.canvas import available_images


def _line(char='_', width=105, size=(75, 1)):
    return gui.Text(char * width, size=size)


class GUI:
    def __init__(self):
        """GUI window for inputing Watermark parameters"""
        self.title = 'PDF Watermarker'
        self.params = {}

    def __iter__(self):
        return iter(self.params)

    def __str__(self):
        return str(self.params)

    @property
    def settings(self):
        """Parameters for parsing directory trees"""
        label_w = 20
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('HPA Design', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                [gui.Text('PDF Watermark utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                [gui.Text('version: ' + __version__, size=(30, 1), font=("Helvetica", 16), text_color='blue')],

                [_line()],

                # Source
                [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                [gui.Text('Source PDF file', size=(label_w, 1), auto_size_text=False), gui.InputText('Source'),
                 gui.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],

                [_line()],

                # Files and non-empty-folders
                [gui.Text('Project address', font=('Helvetica', 15), justification='left')],
                [gui.Text('Address', size=(label_w, 1), auto_size_text=False), gui.InputText()],
                [gui.Text('Town', size=(label_w, 1), auto_size_text=False), gui.InputText()],
                [gui.Text('State', size=(label_w, 1), auto_size_text=False), gui.InputText()],

                [_line()],

                [gui.Text('Watermark Settings', font=('Helvetica', 15), justification='left')],
                [
                    gui.Text('Logo Image', size=(label_w, 1), auto_size_text=False),
                    gui.InputCombo(values=(available_images()), size=(30, 4))
                ],

                [
                    gui.Text('File Compression', size=(label_w, 1), auto_size_text=False),
                    gui.Radio('Uncompressed', "RADIO1", default=True), gui.Radio('Compressed', "RADIO1")
                ],
                [
                    gui.Text('Watermark Flattening', size=(label_w, 1), auto_size_text=False),
                    gui.Radio('Layered', "RADIO3", default=True), gui.Radio('Flattened', "RADIO3")
                ],
                [
                    gui.Text('Watermark Placement', size=(label_w, 1), auto_size_text=False),
                    gui.Radio('Overlay', "RADIO2", default=True), gui.Radio('Underneath', "RADIO2")
                ],
                [gui.Text('Opacity', size=(label_w, 1), auto_size_text=False),
                 gui.Slider(range=(1, 20), orientation='h', size=(34, 30), default_value=8)],

                [_line()],

                # Encryption
                [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
                [gui.Checkbox('Encrypt', default=True)],
                [gui.Text('User Password', size=(label_w, 1), auto_size_text=False), gui.InputText()],
                [gui.Text('Owner Password', size=(label_w, 1), auto_size_text=False), gui.InputText()],

                [gui.Text('Click Submit to watermark PDF')],

                [gui.Submit(), gui.Cancel()]
            ]

            (button, (values)) = form.LayoutAndShow(layout)

        opacity = float(values[11] * .01)
        user_pw = values[13] if len(values[13]) > 0 else ''
        owner_pw = values[14] if len(values[14]) > 0 else ''
        self.params = {
            'pdf': values[0],
            'address': values[1],
            'town': values[2],
            'state': values[3],
            'image': values[4],
            'compression': {
                'uncompressed': values[5],
                'compressed': values[6]
            },
            'flattening': {
                'layered': values[7],
                'flattened': values[8],
            },
            'placement': {
                'overlay': values[9],
                'underneath': values[10]
            },
            'opacity': opacity,
            'encrypt': values[12],
            'user_pw': user_pw,
            'owner_pw': owner_pw,
        }
        return self.params


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
            [gui.Text('Enter the Source file')],
            [gui.Text('Source File', size=(15, 1), justification='right'), gui.InputText('Src'),
             gui.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
            [gui.Submit(), gui.Cancel()]]

        button, (source) = form.LayoutAndRead(form_rows)
        return source[0]
