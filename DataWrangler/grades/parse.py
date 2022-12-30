import tabula, pandas as pd, csv, re, numbers
from colorama import Fore, Style
from tqdm import tqdm
from instructor import Instructor

'''
Notes:

Area is defined as [y1, x1, y2, x2]
'''

class Parser:
    def __init__(self, filename, pages = 'all', dir:Instructor=None):
        self.dir = dir
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Loading {filename}...{Style.RESET_ALL}')
        self.term = tabula.read_pdf(filename, pages='1', area=[41.085, 99.99, 53.955, 123.75])[0].columns[0]
        # Data area, Subject area
        area = [[119.295,200,525.195,487.08], [105.435, 35.145, 121.275, 246.015]]
        if int(self.term) >= 1224: area[0][0], area[0][2] = area[0][0]-12, area[0][2]+25
        table = tabula.read_pdf(filename, pages=pages, area=area, pandas_options={'header': None})
        self.table = table
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Loaded {filename}...{Style.RESET_ALL}')
        
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Packing data...')
        self.data = []
        n = len(table)
        for i in range(n-1):
            page, code = table[i], table[i+1]
            if len(page) == 1 or len(code) != 1: continue
            page.attrs["SubjectNum"] = code.iloc[0, 0]
            page.attrs["Subject"] = code.iloc[0, 1]
            self.data.append(page)
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Packing finished!')
        

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        for page in self.data: yield page

    def rm_empty(self, page):
        # Removes all empty columns
        page.dropna(how='all',axis=1,inplace=True)
    
    def rm_nan_course(self, index):
        GPA_col = 'GPA'
        CourseNum_col = 'CourseNum'
        Section_col = 'Section'
        Student_col = 'Students'
        page = self.data[index]
        self.rm_empty(page)
        self.update_headers(page)
        if page.shape[1] < 8: 
            # page = pd.DataFrame()
            self.data[index] = pd.DataFrame()
            return
        # Get only courses that meet the student threashold 
        page[Student_col] = pd.to_numeric(page[Student_col], errors='coerce')
        page.query(f'{Student_col}.notna()', inplace=True) 
        # page.query(f'{Student_col} > 5', inplace=True)
        # Get only courses with GPA
        page[GPA_col] = pd.to_numeric(page[GPA_col], errors='coerce')
        page.query(f'{GPA_col}.notna()', inplace=True)
        # Get only courses with correct Section information
        for col in [CourseNum_col, Section_col]:
            # page[col] = pd.to_numeric(page[col], errors='coerce')
            page.query(f'{col}.notna()', inplace=True)
            # page[col] = page[col].astype(str)
            # page.query(f'{col}.str.len() == 3', inplace=True)
            # page.query(f'{col}.str.isdigit()', inplace=True)
        # page[Section_col] = page[Section_col].astype(str)
        # page.query(f'{Section_col}.str.len() == 3', inplace=True)
        # page.query(f'{Section_col}.str.isdigit()', inplace=True)
    
    def reset_headers(self, page):
        headers = list(range(len(page.columns)))
        cols = dict(zip(page.columns, headers))
        page.rename(columns=cols, inplace=True)
    
    def update_headers(self, page):
        if page.shape[1] == 10: 
            temp = page[page.columns[0]].astype('str').str.split(' ', n=1, expand=True)
            if temp.shape[1] == 2: 
                page[page.columns[0]] = temp[0]
                page.insert(1, 'Section', temp[1])
        # if page.shape[1] != 11: return
        headers = ['CourseNum', 'Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F']
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
        for i, page in enumerate(self.data):
            # self.rm_empty(page)
            # self.update_headers(page)
            # self.reset_headers(page)
            self.rm_nan_course(i)
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
    p = Parser('../data/pdfs/1224-grade-report.pdf', '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
    # p.filter()
    # # print(p.data[220], p.data[220].attrs['Subject'])
    # # print(len(p.data))
    # # p.save(p.term)
    # for page in p: 
    #     print(page.attrs['Subject'])
    #     print((page))