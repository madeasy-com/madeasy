import pdfplumber, pandas as pd, csv, re, numbers
from colorama import Fore, Style
from tqdm import tqdm

class Parser:
    def __init__(self, filename):
        self.dir = None # Type Instructor
        
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Loading {filename}...{Style.RESET_ALL}')
        pdf = pdfplumber.open(filename)
        TERM, CODE = (70, 44, 125, 55), (75, 110, 150, 120)
        self.term = pdf.pages[0].within_bbox(TERM).extract_text()[-4:]
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Loaded {filename}...{Style.RESET_ALL}')
        
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Packing data...')
        def m(s):
            s = " ".join(s.split())
            n = len(s)
            for i, c in enumerate(s):
                if c.isdigit():
                    if (i+8) < n and s[i:i+3].isnumeric() and s[i+3] == ' ' and s[i+4:i+7].isnumeric() and s[i+7] == ' ':
                        return (DEPT.split(' ', maxsplit=1))+s[i:].split(' ')[:11]
            return ''
        
        with pdfplumber.open(filename) as pdf:
            data = []
            for page in tqdm(pdf.pages):
                DEPT = page.within_bbox(CODE).extract_text()
                res = list(filter(lambda s: s, map(m, filter(lambda s: False if '***' in s else True, page.extract_text().split('\n')))))
                data.extend(res)
            
            self.data = pd.DataFrame(data, columns=['Code', 'Dept', 'Course', 'Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F'])
            self.data.replace('.', '0.0', inplace=True)
            self.data.replace('', '0.0', inplace=True)
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Packing finished!')
        

    def __str__(self):
        return str(self.data)
    
    def make_dir(self, Folder):
        import os
        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/{Folder}'):
            pass
        else:
            os.makedirs(f'{os.path.dirname(os.path.abspath(__file__))}/{Folder}')
            print(f'{Folder} Path made!')
    
    def save(self, filename='test', dir='extracted'):
        self.make_dir(dir)
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to {filename}.PRA...')
        self.data.to_string(f'{dir}/{filename}.pra')
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Saved to {filename}.PRA!')

    
if __name__ == '__main__':
    p = Parser('../data/pdfs/1214-grade-report.pdf')
    p.save('1214')
    print(p)