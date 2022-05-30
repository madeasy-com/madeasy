from os import listdir
from colorama import Fore, Style
from extractor import Extractor

def main():
    '''
    Batch process all pdf files in the current directory
    '''
    source = '../data/pdfs/'
    destination = '../data/extracted'
    for file in listdir(source):
        if file.endswith('.pdf'):
            pdf = Extractor(source+file, 'all')
            pdf.extract()
            pdf.save(pdf.term, dir=destination)

if __name__ == '__main__':
    main()