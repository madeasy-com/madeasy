import pdfplumber, pandas as pd, csv, re, numbers
from colorama import Fore, Style
from tqdm import tqdm
from instructor import Instructor
import numpy as np

'''
Notes:

Area is defined as [y1, x1, y2, x2]
'''

class Parser:
    def __init__(self, filename, pages = 'all', dir:Instructor=None):
        self.dir = dir
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Loading {filename}...{Style.RESET_ALL}')
        pdf = pdfplumber.open(filename)
        TERM, CODE = (70, 44, 125, 55), (75, 110, 150, 120)
        self.term = pdf.pages[0].within_bbox(TERM).extract_text()[-4:]
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Loaded {filename}...{Style.RESET_ALL}')
        
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Packing data...')
        def clean(row):
            code = row[1]
            # Remove non reported grades and blank rows
            whitelist = ['***' in row, ''.join(row) == '']
            # Check code is in correct format
            blacklist = [len(code) >= 7 and code[-7:-4].isnumeric() and code[-3:].isnumeric() and code[-4] == ' ']
            if True in whitelist: return False
            if False in blacklist: return False
            return True
        
        def mapping(row):
            temp = []
            for s in row[2:11]:
                temp += s.split(' ')
            return [row[1], *temp][:10]
        
        self.data = []
        for page in tqdm(pdf.pages[:20]):
            code = page.within_bbox(CODE).extract_text()
            res = page.extract_table(table_settings={"vertical_strategy": "text","horizontal_strategy": "text","keep_blank_chars": True,"text_x_tolerance": 2})
            res = map(mapping, filter(clean, res))
            temp = pd.DataFrame(res, columns=['Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F']) # columns=['Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F', 'S', 'U', 'CR', 'N', 'P', 'I', 'NW', 'NR', 'Other']
            temp.attrs["SubjectNum"] = code[:3]
            temp.attrs["Subject"] = code[4:]
            self.data.append(temp)
            # print(res)
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Packing finished!')
        

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        for page in self.data: yield page

    def rm_empty(self, page):
        # Removes all empty columns
        page.dropna(how='all',axis=1,inplace=True)
    
    def rm_nan_course(self, page):
        GPA_col = 'GPA'
        Section_col = 'Section'
        Student_col = 'Students'
        self.rm_empty(page)
        self.update_headers(page)
        print(page.dtypes)
        # Get only courses that meet the student threashold 
        page[Student_col] = pd.to_numeric(page[Student_col], errors='coerce', downcast='integer')
        page.query(f'{Student_col}.notna()', inplace=True) 
        page.query(f'{Student_col} > 5', inplace=True)
        # Get only courses with GPA
        page[GPA_col] = pd.to_numeric(page[GPA_col], errors='coerce')
        page.query(f'{GPA_col}.notna()', inplace=True)
        # Get only courses with correct Section information
        page.query(f'{Section_col}.notna()', inplace=True)
        page[Section_col] = page[Section_col].astype(str)
        page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', inplace=True)
        page.query(f'{Section_col}.str.len() == 7', inplace=True)
    
    def reset_headers(self, page):
        headers = list(range(len(page.columns)))
        cols = dict(zip(page.columns, headers))
        page.rename(columns=cols, inplace=True)
    
    def update_headers(self, page):
        headers = ['Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F']
        # headers = ['Department', 'Course', 'Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F']
        cols = dict(zip(page.columns, headers))
        page.rename(columns=cols, inplace=True)
    
    def subject_check(self, page):
        if not page.empty:
            try:
                page.attrs['Subject']
            except:
                page
    
    def clean(self):
        self.data = [ page for page in self.data if not page.empty ]
    
    def filter(self):
        for page in self.data:
            self.rm_empty(page)
            self.update_headers(page)
            # self.reset_headers(page)
            # self.rm_nan_course(page)
            self.rm_empty(page)
            # self.apply_subj(page)
            self.update_headers(page)
            self.subject_check(page)
        self.clean()
    
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
        with open(f'{dir}/{filename}.pra', 'w') as file:
            for page in self.data: 
                file.write('\n' + page.attrs['Subject'] + '\n')
                file.write(str(page))#.strip()+'\n')
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Saved to {filename}.PRA!')
    
            

if __name__ == '__main__':
    # p = Parser('../data/pdfs/1224-grade-report.pdf', '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
    p = Parser('../data/pdfs/1214-grade-report.pdf', 'all')
    p.filter()
    # # print(p.data[220], p.data[220].attrs['Subject'])
    # # print(len(p.data))
    p.save(p.term)
    # for page in p: 
    #     print(page.attrs['Subject'])
    #     print((page))