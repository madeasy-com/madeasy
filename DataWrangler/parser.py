import tabula, pandas as pd, csv
from colorama import Fore, Style

def load(filename, pages = '1'):
    print(f'{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}')
    df = tabula.read_pdf(filename, pages=pages, area=[96.525, 71.28, 524.205, 716.76])
    print(f'{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}')
    return df

df = load('test.pdf', '1,2,3')

def generator():
    for page in df: yield page.to_csv()

def subject(page):
    string = page.splitlines()[1].split(",")[1]
    return string[4:].replace(' Grades', '')

# def save(): 
    # print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to CSV...')
    # for table in parse():

if __name__ == '__main__':
    for page in generator():
        print(subject(page))