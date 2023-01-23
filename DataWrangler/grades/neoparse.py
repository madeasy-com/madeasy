import pdfplumber, pandas as pd, csv, re, numbers
from colorama import Fore, Style
from tqdm import tqdm

class Parser:
    def __init__(self, filename):
        self.dir = None # Type Instructor
        
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Loading {filename}...{Style.RESET_ALL}')
        pdf = pdfplumber.open(filename)
        TERM, CODE = (70, 44, 125, 55), (70, 105, 200, 125)
        self.term = pdf.pages[0].within_bbox(TERM).extract_text()[-4:]
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Loaded {filename}...{Style.RESET_ALL}')
        
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Packing data...')
        def m(s):
            s = " ".join(s.split())
            n = len(s)
            for i, c in enumerate(s):
                if c.isdigit():
                    if (i+8) < n and s[i:i+3].isnumeric() and s[i+3] == ' ' and s[i+4:i+7].isnumeric() and s[i+7] == ' ':
                        code, name = DEPT.split(maxsplit=1)
                        # '\n' replacement done in order to parse an edge case in term 1224
                        if '\n' in name: name = name[:name.find('\n')]
                        return [code, name]+s[i:].split()[:11]
            return ''
        
        with pdfplumber.open(filename) as pdf:
            data = []
            for page in tqdm(pdf.pages):
                DEPT = page.within_bbox(CODE).extract_text()
                '''
                Skip all redacted grade classes '***'
                Squish all multi spaces into single space
                Select strings that exactly match the regex -> '\d{3} \d{3} ' (e.g. '123 001 ') which is basically searching for course and section
                '''
                res = list(filter(lambda s: s, map(m, filter(lambda s: False if '***' in s else True, page.extract_text().split('\n')))))
                data.extend(res)
            
            self.data = pd.DataFrame(data, columns=['Dept_Code', 'Dept_Name', 'Course', 'Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F'])
            self.data.replace('.', '0.0', inplace=True)
            self.data.replace('', '0.0', inplace=True)
            # Edge case for term 1224, later can be solved more generally by replacing dept_name with a mapping such as d[Dept_code] -> Dept_Name
            if 4980 < len(self.data.index):
                if self.data.iloc[4980]['Dept_Code'] == '298': self.data.iloc[4980]['Dept_Name'] = 'EAST ASIAN AREA STUDIES'
            selected = ['Dept_Code', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F']
            for col in selected:
                self.data[col] = pd.to_numeric(self.data[col])
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
    p = Parser('../data/pdfs/1224-grade-report.pdf')
    p.save('1224')
    print(p)