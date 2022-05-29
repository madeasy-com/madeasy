import tabula, pandas as pd, csv, re
from colorama import Fore, Style


class Parser:
    def __init__(self, filename, pages="all"):
        print(f"{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}")
        self.term = tabula.read_pdf(
            filename, pages="1", area=[41.085, 99.99, 53.955, 123.75]
        )[0].columns[0]
        self.data = tabula.read_pdf(
            filename,
            pages=pages,
            area=[119.295, 200, 525.195, 487.08],
            pandas_options={"header": None},
        )
        for page, code in zip(
            self.data,
            tabula.read_pdf(
                filename, pages=pages, area=[107.415, 90.09, 121.275, 193.05]
            ),
        ):
            # page.attrs['Subject'] = re.sub('[[:alpha:]]', '', code.columns[0])
            if len(code.columns) > 0:
                page.attrs["Subject"] = code.columns[0]
                # print(page.attrs['Subject'])
            else:
                self.data.remove(page)
        print(f"{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}")

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
        GPA = "***"
        GPA_col = "GPA"
        Section_col = "Section"
        page.query(f"{GPA_col}.notna()", inplace=True)
        page.query(f'{GPA_col}.str.replace(".","").str.isdigit()', inplace=True)
        page.query(f"{Section_col}.notna()", inplace=True)
        page.query(f'{Section_col}.str.replace(" ","").str.isdigit()', inplace=True)
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

    def filter(self):
        for page in self.data:
            self.rm_empty(page)
            self.update_headers(page)
            # self.reset_headers(page)
            self.rm_nan_course(page)
            # self.apply_subj(page)
            self.update_headers(page)
        self.data = [page for page in self.data if not page.empty]

    def save(self, filename="test"):
        print(f"{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to {filename}.PRA...")
        with open(f"{filename}.pra", "w") as file:
            for page in self.data:
                file.write(str(page).strip() + "\n")
        print(f"{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saved to {filename}.PRA!")

    def courseStat(pdf, page):
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
            courseDict[page.attrs["Subject"] + " " + classList[i]] = {
                sectionList[i]: {
                    "GPA": gpa[i],
                    "A": A[i],
                    "AB": AB[i],
                    "B": B[i],
                    "BC": BC[i],
                    "C": C[i],
                    "D": D[i],
                    "F": F[i],
                }
            }
        return courseDict


if __name__ == "__main__":
    pdf = Parser(
        r"C:\Users\nithi\Downloads\madeasy\report-gradedistribution-2021-2022fall.pdf",
        "all",
    )
    pdf.filter()
    # print(pdf)
    # pdf.save(pdf.term)
    for page in pdf:
        print(pdf.courseStat(page))
