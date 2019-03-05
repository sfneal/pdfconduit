from pdf.conduit import Watermark


def apply_watermark(file_path, params):
    # Execute Watermark class
    wm = Watermark(file_path, progress_bar_enabled=False, use_receipt=False)
    
    wm.draw(text1=params['address'],
            text2=str(params['town'] + ', ' + params['state']))
    return wm.add()
