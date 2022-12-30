import tabula, pandas as pd, csv, re, numbers
from colorama import Fore, Style
from tqdm import tqdm
from instructor import Instructor


class Parser:
    def __init__(self, filename, pages="all", dir: Instructor = None):
        self.dir = dir
        print(
            f"{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Loading {filename}...{Style.RESET_ALL}"
        )
        self.term = tabula.read_pdf(
            filename, pages="1", area=[41.085, 99.99, 53.955, 123.75]
        )[0].columns[0]
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Loaded {filename}...{Style.RESET_ALL}")
        # # code = tabula.read_pdf(filename, pages, area=)
        # self.data = []
        # data1 = tabula.read_pdf(filename, pages=pages, area=[118.305, 262.68, 525.195, 481.47], pandas_options={'header': None})
        # [ page.rename({0: 10}) for page in data1 ]
        # data2 = tabula.read_pdf(filename, pages=pages, area=[119.3, 200, 524.2, 232], pandas_options={'header': None})
        # for d1, d2 in zip(data1, data2):
        #     self.data.append(d1.merge(d2, how='right'))
        # print(data1)
        # print(data2)
        # self.data = tabula.read_pdf(filename, pages=pages, area=[[118.305, 266.64, 533.115, 482.46,],[119.295,200,525.195,232]], pandas_options={'header': None})
        # # self.data = [ page for i, page in enumerate(self.data) if i % 2 == 1 ]
        # len(self.data)
        self.data = []
        if int(self.term) < 1224:
            data = tabula.read_pdf(
                filename,
                pages=pages,
                area=[119.295, 200, 525.195, 487.08],
                pandas_options={"header": None},
                multiple_tables=True,
            )
        else:
            data = tabula.read_pdf(
                filename,
                pages=pages,
                area=[119.295, 200, 525.195, 487.08],
                pandas_options={"header": None},
                multiple_tables=True,
            )
        # subject = []
        # print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Packing data...')
        # for page, code in zip(data, tabula.read_pdf(filename, pages=pages, area=[107.415, 90.09, 121.275, 193.05], pandas_options={'header': None})):
        #     # page.attrs['Subject'] = re.sub('[[:alpha:]]', '', code.columns[0])
        #     page.attrs['Subject'] = code.iloc[0, 0]
        #     self.data.append(page)
        #     subject.append(page.attrs['Subject'])
        # print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Packing finished!')

        subject = []
        subjectNum = []
        print(f"{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Packing data...")
        for page, code in zip(
            data,
            tabula.read_pdf(
                filename,
                pages=pages,
                area=[105.435, 35.145, 121.275, 246.015],
                pandas_options={"header": None},
            ),
        ):
            try:
                page.attrs["Subject"] = code.iloc[0, 1]
                page.attrs["SubjectNum"] = code.iloc[0, 0]
                self.data.append(page)
                subject.append(page.attrs["Subject"])
                subjectNum.append(page.attrs["SubjectNum"])
            except:
                pass
        # if int(self.term) < 1224:
        #     for page, code in zip(
        #         data,
        #         tabula.read_pdf(
        #             filename,
        #             pages=pages,
        #             area=[105.435, 35.145, 121.275, 246.015],
        #             pandas_options={"header": None},
        #         ),
        #     ):
        #         page.attrs["Subject"] = code.iloc[0, 1]
        #         page.attrs["SubjectNum"] = code.iloc[0, 0]
        #         self.data.append(page)
        #         subject.append(page.attrs["Subject"])
        #         subjectNum.append(page.attrs["SubjectNum"])
        # else:
        #     for page, code in zip(
        #         data,
        #         tabula.read_pdf(
        #             filename,
        #             pages=pages,
        #             area=[101.475, 60.39, 118.305, 169.29],
        #             pandas_options={"header": None},
        #         ),
        #     ):
        #         page.attrs["Subject"] = code.iloc[0, 1]
        #         page.attrs["SubjectNum"] = code.iloc[0, 0]
        #         print(page.attrs["Subject"])
        #         self.data.append(page)
        #         subject.append(page.attrs["Subject"])
        #         subjectNum.append(page.attrs["SubjectNum"])
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Packing finished!")

        # print(len(data), len(subject))
        # print(data[220])
        # print(data[220].attrs['Subject'])
        # print(subject[220])

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        for page in self.data:
            yield page

    def rm_empty(self, page):
        # Removes all empty columns
        page.dropna(how="all", axis=1, inplace=True)

    def rm_nan_course(self, page):
        GPA_col = "GPA"
        Section_col = "Section"
        Student_col = "Students"
        self.rm_empty(page)
        self.update_headers(page)
        # Get only courses that meet the student threashold
        page[Student_col] = pd.to_numeric(page[Student_col], errors="coerce")
        page.query(f"{Student_col}.notna()", inplace=True)
        page.query(f"{Student_col} > 5", inplace=True)
        # Get only courses with GPA
        page[GPA_col] = pd.to_numeric(page[GPA_col], errors="coerce")
        page.query(f"{GPA_col}.notna()", inplace=True)
        # Get only courses with correct Section information
        page.query(f"{Section_col}.notna()", inplace=True)
        page[Section_col] = page[Section_col].astype(str)
        page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', inplace=True)
        page.query(f"{Section_col}.str.len() == 7", inplace=True)

    def reset_headers(self, page):
        headers = list(range(len(page.columns)))
        cols = dict(zip(page.columns, headers))
        page.rename(columns=cols, inplace=True)

    def update_headers(self, page):
        headers = ["Section", "Students", "GPA", "A", "AB", "B", "BC", "C", "D", "F"]
        # headers = ['Department', 'Course', 'Section', 'Students', 'GPA', 'A', 'AB', 'B', 'BC', 'C', 'D', 'F']
        cols = dict(zip(page.columns, headers))
        page.rename(columns=cols, inplace=True)

    def subject_check(self, page):
        if not page.empty:
            try:
                page.attrs["Subject"]
            except:
                page

    def clean(self):
        self.data = [page for page in self.data if not page.empty]

    def filter(self):
        for page in self.data:
            self.rm_empty(page)
            self.update_headers(page)
            # self.reset_headers(page)
            self.rm_nan_course(page)
            self.rm_empty(page)
            # self.apply_subj(page)
            self.update_headers(page)
            self.subject_check(page)
        self.clean()

    def make_dir(self, Folder):
        import os

        if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/{Folder}"):
            pass
        else:
            os.makedirs(f"{os.path.dirname(os.path.abspath(__file__))}/{Folder}")
            print(f"{Folder} Path made!")

    def save(self, filename="test", dir="extracted"):
        self.make_dir(dir)
        print(f"{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to {filename}.PRA...")
        with open(f"{dir}/{filename}.pra", "w") as file:
            for page in self.data:
                file.write("\n" + page.attrs["Subject"] + "\n")
                file.write(str(page))  # .strip()+'\n')
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Saved to {filename}.PRA!")


if __name__ == "__main__":
    pdf = Parser("test.pdf", "all")
    pdf.filter()
    # print(pdf.data[220], pdf.data[220].attrs['Subject'])
    # print(len(pdf.data))
    # pdf.save(pdf.term)
    for page in pdf:
        print(page.attrs["Subject"])
        print((page))
