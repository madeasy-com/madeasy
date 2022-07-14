import tabula, pandas as pd, csv, re, numbers
from colorama import Fore, Style
import numpy as np


class Instructor:
    def __init__(self, filename, pages="all"):
        print(f"{Fore.LIGHTCYAN_EX}Loading {filename}...{Style.RESET_ALL}")
        self.term = tabula.read_pdf(
            filename,
            area=[66.825, 70.785, 79.695, 101.475],
            pages=1,
        )[0].columns[0]
        self.data = []
        data = tabula.read_pdf(
            filename,
            area=[127.215, 4.455, 561.825, 791.505],
            pandas_options={"header": None},
            pages=pages,
        )
        self.collegeNum = []
        collegeNum = tabula.read_pdf(
            filename,
            area=[89.595, 31.185, 110.385, 681.615],
            pages=pages,
        )
        for page in collegeNum:
            self.collegeNum.append(page.columns[0][-4:-1])
        i = 0
        for page in data:
            page = page.iloc[:, [1, 3, -1]]
            page.columns = ["Course", "Section", "Instructor"]
            page["Section"] = page["Section"].astype(str).str.zfill(3)
            page["Instructor"] = page["Instructor"].str[4:]
            page["CollegeNum"] = self.collegeNum[i]
            page["Term"] = self.term
            i += 1
            self.data.append(page)
        self.data = pd.concat(self.data)
        print(f"{Fore.LIGHTCYAN_EX}Loaded {filename}...{Style.RESET_ALL}")

    def get_instructor(self, courseNum, sectionNum, collegeNum, collegeTerm):
        return self.data.loc[
            (self.data["Course"] == courseNum)
            & (self.data["Section"] == sectionNum)
            & (self.data["CollegeNum"] == collegeNum)
            & (self.data["Term"] == collegeTerm)
        ]["Instructor"].values[0]

    def get_AllInstructors(self, courseNum, collegeNum, collegeTerm):
        listInstructors = self.data.loc[
            (self.data["Course"] == courseNum)
            & (self.data["CollegeNum"] == collegeNum)
            & (self.data["Term"] == collegeTerm)
        ]["Instructor"].values
        setInstructors = set(listInstructors)
        return setInstructors


if __name__ == "__main__":
    pdf = Instructor(
        r"C:\Users\nithi\Downloads\madeasy\Final_DIR_1224.pdf",
        "1,2,3,4,5",
    )
    print(pdf.get_instructor(215, "301", "108", "1224"))
    print(pdf.get_AllInstructors(215, "108", "1224"))
    # print(pdf.data)