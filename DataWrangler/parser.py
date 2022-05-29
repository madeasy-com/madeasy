import tabula, pandas as pd, csv
from colorama import Fore, Style

class Parser:
    def __init__(self, filename, pages = 'all'):
        print(f'{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}')
        self.data = tabula.read_pdf(filename, pages=pages, area=[96.525, 71.28, 524.205, 716.76])
        print(f'{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}')

    def __iter__(self):
        for page in self.data: yield page

    def subject(self, page):
        # return self.data
        
        # if 'Summary by College/School' == (string := page.splitlines()[1].split(",")[1]): self.data.remove(page)
        # return string[4:].replace(' Grades', '')
    
    def filter(self):
        for page in self.data: 
            self.subject(page)
    
    def save(self, filename): 
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to CSV...')
        with open(f'{filename}.pra', 'w') as file:
            for page in self.data: file.write(str(page).strip())
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saved to CSV!')
            

if __name__ == '__main__':
    pdf = Parser('test.pdf', '1,2,3')
    # pdf.filter()
    # pdf.save('test')
    for page in pdf:
        # print((page))
        print(pdf.subject(page))