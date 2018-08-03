import PySimpleGUI as gui
from pdfwatermarker import __version__


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
                    gui.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3', 'Listbox 4'), size=(30, 4))
                ],

                [
                    gui.Text('Page Compression', size=(label_w, 1), auto_size_text=False),
                    gui.Radio('Uncompressed', "RADIO1", default=True), gui.Radio('Compressed', "RADIO1")
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

                [gui.Submit(), gui.Cancel()]]

            (button, (values)) = form.LayoutAndShow(layout)

        self.params = {
            'pdf': values[0],
            'address': values[1],
            'town': values[2],
            'state': values[3],
            'opacity': values[4],
            'encrypt': values[5],
            'user_pw': values[6],
            'owner_pw': values[7],
        }
        pdf = values[0]
        address = values[1]
        town = values[2]
        state = values[3]
        opacity = float(values[4] * .01)
        encrypt = values[5]

        if len(values[6]) > 0:
            user_pw = values[6]
        else:
            user_pw = ''

        if len(values[7]) > 0:
            owner_pw = values[7]
        else:
            owner_pw = None

        return pdf, address, town, state, opacity, encrypt, user_pw, owner_pw
