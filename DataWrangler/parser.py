import tabula, pandas as pd, csv
from colorama import Fore, Style

def load(filename, pages = '1'):
    print(f'{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}')
    df = tabula.read_pdf(filename, pages=pages, area=[96.525, 71.28, 524.205, 716.76])
    print(f'{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}')
    return df

def generator(filename, pages='1,2,3'):
    for page in load(filename,pages): yield page.to_csv()

def subject(page):
    string = page.splitlines()[1].split(",")[1]
    return string[string.find(' ')+1:string.rfind(' ')]

# def save(): 
    # print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to CSV...')
    # for table in parse():

if __name__ == '__main__':
    page = generator('test.pdf')
    print(subject(page.__next__()))
    # print(page.__next__())