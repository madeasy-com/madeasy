import tabula, pandas as pd, csv
from colorama import Fore, Style

class Parser:
    def __init__(self, filename, pages = 'all'):
        print(f'{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}')
        self.term = tabula.read_pdf(filename, pages='1', area=[41.085, 99.99, 53.955, 123.75])[0].columns[0]
        self.data = tabula.read_pdf(filename, pages=pages, area=[96.525, 71.28, 524.205, 716.76])
        print(f'{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}')

    def __iter__(self):
        for page in self.data: yield page

    def rm_empty(self, page):
        empty_col = [ col for col in page.columns if 'Unnamed:' in col ]
        for col in empty_col: page.drop(col, axis=1, inplace=True)
        return page
        # if 'Summary by College/School' == (string := page.splitlines()[1].split(",")[1]): self.data.remove(page)
        # return string[4:].replace(' Grades', '')
    
    def rm_pf(self, page):
        cols = {'S', 'U', 'CR', 'N', 'P', 'I', 'NW', 'NR', 'Other'}.intersection(set(page.columns))
        for col in cols: page.drop(col, axis=1, inplace=True)
        return page
    
    def rm_nan_course(self, page):
        GPA =  '***'
        col = 'Ave'
        if col in page.columns:
            page.dropna(subset=[col],inplace=True)
            page.query(f'Ave != "{GPA}"',inplace=True)
        return page
    
    def filter(self):
        for i in range(len(self.data)):
            self.data[i] = self.rm_empty(self.data[i])
            self.data[i] = self.rm_pf(self.data[i])
            self.data[i] = self.rm_nan_course(self.data[i])
            self.data.append(self.data[i])
    
    def save(self, filename='test'): 
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to {filename}.PRA...')
        with open(f'{filename}.pra', 'w') as file:
            for page in self.data: file.write(str(page).strip()+'\n')
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saved to {filename}.PRA!')
            

if __name__ == '__main__':
    pdf = Parser('test.pdf', '1,2,3')
    pdf.filter()
    pdf.save(pdf.term)
    # for page in pdf: print((page))