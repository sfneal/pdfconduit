import PySimpleGUI as gui


def _line(char='_', width=100, size=(70, 1)):
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
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('HPA Design PDF Watermark utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                # Source
                [gui.Text('Select a source PDF and input project address information')],
                [gui.Text('Source pdf', size=(15, 1), auto_size_text=False), gui.InputText('Source'),
                 gui.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],

                [_line()],

                # Files and non-empty-folders
                [gui.Text('Project address')],
                [gui.Text('Address', size=(15, 1), auto_size_text=False), gui.InputText()],
                [gui.Text('Town', size=(15, 1), auto_size_text=False), gui.InputText()],
                [gui.Text('State', size=(15, 1), auto_size_text=False), gui.InputText()],

                [_line()],

                [gui.Text('Watermark Opacity', size=(15, 1), auto_size_text=False),
                 gui.Slider(range=(1, 20), orientation='h', size=(34, 30), default_value=8)],
                [_line()],

                # Encryption
                [gui.Checkbox('Encrypt', default=True)],
                [gui.Text('User Password', size=(15, 1), auto_size_text=False), gui.InputText()],
                [gui.Text('Owner Password', size=(15, 1), auto_size_text=False), gui.InputText()],

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
            user_pw = None

        if len(values[7]) > 0:
            owner_pw = values[7]
        else:
            owner_pw = None

        return pdf, address, town, state, encrypt, opacity, user_pw, owner_pw
