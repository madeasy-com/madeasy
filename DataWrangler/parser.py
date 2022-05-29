import tabula, pandas as pd, csv
from colorama import Fore, Style

class Parser:
    def __init__(self, filename, pages = 'all'):
        print(f'{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}')
        self.data = tabula.read_pdf(filename, pages=pages, area=[96.525, 71.28, 524.205, 716.76])
        print(f'{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}')

    def __iter__(self):
        for page in self.data: yield page

    def rm_empty(self, page):
        empty_col = [ col for col in page.columns if 'Unnamed:' in col ]
        for col in empty_col: page = page.drop(col, axis=1)
        return page
        # if 'Summary by College/School' == (string := page.splitlines()[1].split(",")[1]): self.data.remove(page)
        # return string[4:].replace(' Grades', '')
    
    def rm_pf(self, page):
        cols = {'S', 'U', 'CR', 'N', 'P', 'I', 'NW', 'NR', 'Other'}.intersection(set(page.columns))
        for col in cols: page = page.drop(col, axis=1)
        return page
    
    def filter(self):
        self.copy = self.data.copy()
        self.data = []
        for page in self.copy: 
            page = self.rm_empty(page)
            page = self.rm_pf(page)
            self.data.append(page)
    
    def save(self, filename): 
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to CSV...')
        with open(f'{filename}.pra', 'w') as file:
            for page in self.data: file.write(str(page).strip())
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saved to CSV!')
            

if __name__ == '__main__':
    pdf = Parser('test.pdf', 'all')
    pdf.filter()
    for page in pdf: print((page))