import tabula, pandas as pd, csv, re
from colorama import Fore, Style

class Parser:
    def __init__(self, filename, pages = 'all'):
        print(f'{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}')
        self.term = tabula.read_pdf(filename, pages='1', area=[41.085, 99.99, 53.955, 123.75])[0].columns[0]
        self.data = tabula.read_pdf(filename, pages=pages, area=[119.295,200,525.195,487.08], pandas_options={'header': None})
        for page, code in zip(self.data, tabula.read_pdf(filename, pages=pages, area=[107.415, 90.09, 121.275, 193.05])):
            page.attrs['Subject'] = re.sub('[[:alpha:]]', '', code.columns[0])
        print(f'{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}')

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        for page in self.data: yield page

    def rm_empty(self, page):
        '''
        Removes all empty columns
        '''
        page.dropna(how='all',axis=1,inplace=True)
    
    def rm_nan_course(self, page):
        GPA =  '***'
        GPA_col = 'GPA'
        Section_col = 'Section'
        # page.query(f'{GPA_col}.notna()', inplace=True) 
        # page.query(f'{GPA_col}.str.replace(".","").str.isdigit()', inplace=True)
        # page.query(f'{Section_col}.notna()', inplace=True) 
        # page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', inplace=True)
        # '''
        try: page.query(f'{GPA_col}.notna()', inplace=True) 
        except: pass
        try: page.query(f'{GPA_col}.str.replace(".","").str.isdigit()', inplace=True)
        except: pass
        try: page.query(f'{Section_col}.notna()', inplace=True) 
        except: pass
        try: page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', inplace=True)
        except: pass
        # '''
    
    def update_headers(self, page):
        headers = ['Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F']
        cols = dict(zip(page.columns, headers))
        page.rename(columns=cols, inplace=True)
    
    def apply_subj(self, page):
        page[['Section']] = page[['Section']].applymap(lambda x: page.attrs['Subject'] + ' ' + x)
    
    def filter(self):
        for page in self.data:
            self.rm_empty(page)
            self.update_headers(page)
            self.rm_nan_course(page)
            self.apply_subj(page)
        self.data = [ page for page in self.data if not page.empty ]
    
    def save(self, filename='test'): 
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to {filename}.PRA...')
        with open(f'{filename}.pra', 'w') as file:
            for page in self.data: file.write(str(page).strip()+'\n')
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saved to {filename}.PRA!')
            

if __name__ == '__main__':
    pdf = Parser('test.pdf', 'all')
    pdf.filter()
    # print(pdf)
    pdf.save(pdf.term)
    # for page in pdf: print((page))