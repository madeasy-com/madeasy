import tabula, pandas as pd, csv
from colorama import Fore, Style

df = tabula.read_pdf("test.pdf", pages='all', area=[96.525, 71.28, 524.205, 716.76])

def parse(): 
    for page in df: yield page.to_csv()

# def save(): 
    # print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to CSV...')
    # for table in parse():
        

def subject(page):
    string = parse().splitlines()[1].split(",")[1]
    return string[string.find(' ')+1:string.rfind(' ')]

if __name__ == '__main__':
    print(subject())