# Apply a watermark to a PDF file
import os
import shutil
from datetime import datetime
from pdfwatermarker.watermark.draw import WatermarkDraw
from pdfwatermarker.watermark.add import WatermarkAdd
import warnings
from subprocess import call, Popen
from pathlib import Path


def remove_temp(pdf):
    temp = os.path.join(os.path.dirname(pdf), 'temp')
    shutil.rmtree(temp)


class Watermark:
    def __init__(self, pdf, project, address, town, state):
        text = {
            'address': {
                'font': 40,
                'y': -140,
                'txt': {'address': address,
                        'town': town,
                        'state': state}
            },
            'copyright': {
                'font': 16,
                'y': 10,
                'txt': '© copyright ' + str(datetime.now().year),
            }
        }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            watermark = str(WatermarkDraw(project, text, pdf))
        self.pdf = WatermarkAdd(pdf, watermark)
        remove_temp(pdf)

    def __str__(self):
        return str(self.pdf)


class WatermarkGUI:
    def __init__(self):
        # Import GUI and timeout libraries
        from pdfwatermarker.watermark.lib import GUI
        from interruptingcow import timeout
        pdf, address, town, state = GUI().settings
        project = os.path.basename(pdf)[:8]

        # Print GUI selections to console
        print("PDF Watermarker")
        print("{0:20}--> {1}".format('PDF', pdf))
        print("{0:20}--> {1}".format('Project', project))
        print("{0:20}--> {1}".format('Address', address))
        print("{0:20}--> {1}".format('Town', town))
        print("{0:20}--> {1}".format('State', state))

        # Execute Watermark class
        wm = Watermark(pdf, project, address, town, state)
        print("{0:20}--> {1}".format('Watermarked PDF', wm))
        print('\nSuccess!')

        # Open watermarked PDF in finder or explorer window
        try:
            call(["open", "-R", str(Path(str(wm)))])
        except FileNotFoundError:
            Popen(r'explorer /select,' + str(Path(str(wm))))

        # Timeout process after 10 seconds or exit on keyboard press
        try:
            with timeout(10, exception=RuntimeError):
                print('~~Process terminating in 10 seconds~~')
                input('~~Press Any Key To Exit~~')
                quit()
        except RuntimeError:
            quit()
