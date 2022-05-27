import tabula, pandas as pd, csv
from colorama import Fore, Style

def parse(): 
    df = tabula.read_pdf("test.pdf", pages='1,2', area=[96.525, 71.28, 524.205, 716.76])
    # print(df)
    # df[0].to_csv("test.csv", index=True)
    return df[0].to_csv()
    # pages = []
    # for page in df:
    #     pages.append(page.to_csv())
    # return pages

# def save(): 
    # print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to CSV...')
    # for table in parse():
        

def subject(page):
    string = parse().splitlines()[1].split(",")[1]
    return string[string.find(' ')+1:string.rfind(' ')]

if __name__ == '__main__':
    print(subject())