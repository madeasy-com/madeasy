from os import listdir
from colorama import Fore, Style
from extractor import Extractor
from instructor import Instructor

source = '../data/pdfs/'
destination = '../data/extracted'
dir_ext = '-dir.pdf'
report_ext = '-grade-report.pdf'

def main():
    '''
    Batch process all pdf files in the current directory
    '''
    files = listdir(source)
    terms = []
    [ terms.append(term) for file in files if (term := file.split('-')[0]) not in terms ]
    for term in terms:
        if term+dir_ext in files and term+report_ext in files: # check if both dir and grade report exist
            dir = Instructor(source+term+dir_ext)
            pdf = Extractor(source+term+report_ext,dir=dir)
            pdf.extract()
            pdf.save(pdf.term, dir=destination)

if __name__ == '__main__':
    main()