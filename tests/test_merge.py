from pdfwatermarker import merge
import os
import shutil


def main():
    print('Testing merge function reliability')
    hpa = '/Volumes/Storage/HPA Design/Marketing Library/Floor Plan PDFs'
    desktop = '/Users/Stephen/Desktop'
    pdfs = ['20110167_FP.1.pdf', '20110167_FP.2.pdf', '20110167_FP.3.pdf']

    hpa_paths = [os.path.join(hpa, pdf) for pdf in pdfs]
    pdf_paths = [os.path.join(desktop, pdf) for pdf in pdfs]
    for f in pdf_paths:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

    for f in hpa_paths:
        shutil.copy2(f, desktop)

    # output pdf file name
    output = 'combined_example.pdf'

    # calling pdf merge function
    merge(pdfs=pdf_paths, output_name=output)
    print('Done!')


if __name__ == "__main__":
    # calling the main function
    main()
