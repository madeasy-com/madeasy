import tabula, pandas as pd, csv, re, numbers
from colorama import Fore, Style
import numpy as np
import course_instructor as ci


class Parser:
    def __init__(self, dist_file, dir_file, pages="all"):
        print(f"{Fore.LIGHTCYAN_EX}Loading {dist_file}...{Style.RESET_ALL}")
        self.term = tabula.read_pdf(
            dist_file, pages="1", area=[41.085, 99.99, 53.955, 123.75]
        )[0].columns[0]
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
        data = tabula.read_pdf(
            dist_file,
            pages=pages,
            area=[119.295, 200, 525.195, 487.08],
            pandas_options={"header": None},
            multiple_tables=True,
        )
        subject = []
        subjectNum = []
        for page, code in zip(
            data,
            tabula.read_pdf(
                dist_file,
                pages=pages,
                area=[105.435, 35.145, 121.275, 246.015],
                pandas_options={"header": None},
            ),
        ):
            # page.attrs['Subject'] = re.sub('[[:alpha:]]', '', code.columns[0])
            page.attrs["SubjectNum"] = code.iloc[0, 0]
            page.attrs["Subject"] = code.iloc[0, 1]
            self.data.append(page)
            subject.append(page.attrs["Subject"])
            subjectNum.append(page.attrs["SubjectNum"])
        # print(len(data), len(subject))
        # print(data[220])
        # print(data[220].attrs['Subject'])
        # print(subject[220])
        self.instructorspdf = ci.Instructor(dir_file, pages)
        print(f"{Fore.LIGHTCYAN_EX}Loaded {dist_file}...{Style.RESET_ALL}")

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        for page in self.data:
            yield page

    def rm_empty(self, page):
        """
        Removes all empty columns
        """
        page.dropna(how="all", axis=1, inplace=True)

    def rm_nan_course(self, page):
        GPA_col = "GPA"
        Section_col = "Section"
        Student_col = "Students"
        self.rm_empty(page)
        self.update_headers(page)
        # page[GPA_col] = pd.to_numeric(page[GPA_col], errors='coerce')
        # page.query(f'{GPA_col}.notna()', inplace=True)
        page[Student_col] = pd.to_numeric(page[Student_col], errors="coerce")
        page.query(f"{Student_col}.notna()", inplace=True)
        page.query(f"{Student_col} > 5", inplace=True)
        page.query(f"{Section_col}.notna()", inplace=True)
        # page[Section_col] = page[Section_col].apply(lambda x: re.match(), axis=1)
        # page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', extend=True)
        try:
            page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', inplace=True)
        except:
            pass
        """
        try: page.query(f'{GPA_col}.notna()', inplace=True) 
        except: pass
        try: page.query(f'{GPA_col}.str.replace(".","").str.isdigit()', inplace=True)
        except: pass
        try: page.query(f'{Section_col}.notna()', inplace=True) 
        except: pass
        try: page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', inplace=True)
        except: pass
        """

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

    def save(self, filename="test"):
        print(f"{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to {filename}.PRA...")
        with open(f"{filename}.pra", "w") as file:
            for page in self.data:
                file.write(page.attrs["Subject"] + "\n")
                file.write(str(page).strip() + "\n")
        print(f"{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saved to {filename}.PRA!")

    def courseStat(self, page):
        classList = page["Section"].tolist()
        sectionList = []
        courseDict = {}
        gpa = page["GPA"].tolist()
        A = page["A"].tolist()
        AB = page["AB"].tolist()
        B = page["B"].tolist()
        BC = page["BC"].tolist()
        C = page["C"].tolist()
        D = page["D"].tolist()
        F = page["F"].tolist()
        for i in range(len(classList)):
            sectionList.append(classList[i][-3:])
            classList[i] = classList[i][:3]
        for i in range(len(classList)):
            if A[i] == ".":
                A[i] = 0
            if AB[i] == ".":
                AB[i] = 0
            if B[i] == ".":
                B[i] = 0
            if BC[i] == ".":
                BC[i] = 0
            if C[i] == ".":
                C[i] = 0
            if D[i] == ".":
                D[i] = 0
            if F[i] == ".":
                F[i] = 0
            SD = np.std(  # this is incorrect
                [
                    float(A[i]) / 100 * 4.0,
                    float(AB[i]) / 100 * 3.5,
                    float(B[i]) / 100 * 3.0,
                    float(BC[i]) / 100 * 2.5,
                    float(C[i]) / 100 * 2.0,
                    float(D[i]) / 100 * 1.0,
                    float(F[i]) / 100 * 0.0,
                ]
            )
            instructor = self.instructorspdf.get_instructor(
                int(classList[i]),
                str(sectionList[i]),
                str(page.attrs["SubjectNum"]),
                str(pdf.term),
            )
            courseDict[page.attrs["Subject"] + " " + classList[i]] = {
                self.term: {
                    sectionList[i]: {
                        instructor: {
                            "Mean": gpa[i],
                            "SD": SD,
                            "A": A[i],
                            "AB": AB[i],
                            "B": B[i],
                            "BC": BC[i],
                            "C": C[i],
                            "D": D[i],
                            "F": F[i],
                        }
                    }
                }
            }
        return courseDict


if __name__ == "__main__":
    pdf = Parser(
        "./DataWrangler/report-gradedistribution-2020-2021spring.pdf",
        './DataWrangler/1214Spring_Final_DIR.pdf',
        "1,2,3,4,5",
    )
    pdf.filter()
    # print(pdf)
    # pdf.save(pdf.term)
    for page in pdf:
        print(pdf.courseStat(page))
