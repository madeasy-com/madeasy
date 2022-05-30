from os import listdir
from colorama import Fore, Style
from extractor import Extractor

def main():
    '''
    Batch process all pdf files in the current directory
    '''
    dir = '../data/extracted'
    for file in listdir('../data/pdfs'):
        if file.endswith('.pdf'):
            pdf = Extractor(file, 'all')
            pdf.extract()
            pdf.save(pdf.term, dir=dir)

if __name__ == '__main__':
    main()