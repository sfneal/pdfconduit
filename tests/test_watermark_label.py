from pdfwatermarker.watermark.label import Label


def main():
    print('Testing Watermark class reliability')
    pdf = 'data/charts.pdf'
    label = 'Last updated 7/10/18'
    l = Label(pdf, label).write()
    print(l)


if __name__ == '__main__':
    main()
