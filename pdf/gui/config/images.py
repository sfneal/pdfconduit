# Add, remove and view images in the GUI library
import os
import shutil
from pathlib import Path
from pdf.conduit.utils.view import open_window
from platform import system

GUI_ROOT = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(GUI_ROOT, 'lib', 'img')
IMAGES = os.listdir(IMG_DIR)


def add(image_path, file_name=None):
    """Add an image to the GUI img library."""
    if file_name is not None:
        dst_path = os.path.join(IMG_DIR, str(Path(file_name).stem + Path(image_path).suffix))
    else:
        dst_path = IMG_DIR

    if os.path.isfile(image_path):
        shutil.copy2(image_path, dst_path)


def remove(image):
    """Remove an image to the GUI img library."""
    path = os.path.join(IMG_DIR, image)
    if os.path.isfile(path):
        os.remove(path)


def view(folder=IMG_DIR):
    """
    Return a list of available images and
    launch GUI window to view images if GUI is true.
    """
    if system() is 'Windows':
        import PySimpleGUI as sg
        # get list of PNG files in folder
        png_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')]

        filenames_only = [f for f in os.listdir(folder) if '.png' in f]

        if len(png_files) == 0:
            sg.MsgBox('No PNG images in folder')
            exit(0)

        # create the form that also returns keyboard events
        form = sg.FlexForm('Image Browser', return_keyboard_events=True, location=(0, 0), use_default_focus=False)

        # make these 2 elements outside the layout because want to "update" them later
        # initialize to the first PNG file in the list
        image_elem = sg.Image(filename=png_files[0])
        filename_display_elem = sg.Text(png_files[0], size=(80, 3))
        file_num_display_elem = sg.Text('File 1 of {}'.format(len(png_files)), size=(15, 1))

        # define layout, show and read the form
        col = [[filename_display_elem],
               [image_elem],
               [sg.ReadFormButton('Next', size=(8, 2)), sg.ReadFormButton('Prev', size=(8, 2)), file_num_display_elem]]

        col_files = [[sg.Listbox(values=filenames_only, size=(60, 30), key='listbox')],
                     [sg.ReadFormButton('Read')]]
        layout = [[sg.Column(col_files), sg.Column(col)]]
        button, values = form.LayoutAndRead(layout)  # Shows form on screen

        # loop reading the user input and displaying image, filename
        i = 0
        while True:

            # perform button and keyboard operations
            if button is None:
                break
            elif button in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34') and i < len(png_files) - 1:
                i += 1
            elif button in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33') and i > 0:
                i -= 1

            if button == 'Read':
                filename = folder + '\\' + values['listbox'][0]
                # print(filename)
            else:
                filename = png_files[i]

            # update window with new image
            image_elem.Update(filename=filename)
            # update window with filename
            filename_display_elem.Update(filename)
            # update page display
            file_num_display_elem.Update('File {} of {}'.format(i + 1, len(png_files)))

            # read the form
            button, values = form.Read()
    else:
        open_window(IMG_DIR)
