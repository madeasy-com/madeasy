from colorama import Fore, Style
import numpy as np, json
from parse import Parser
from instructor import Instructor
from tqdm import tqdm

class Extractor(Parser):
    
    def generate(self, page):
        # print(page)
        courseNumList = page["CourseNum"].tolist()
        sectionList = page["Section"].tolist()
        courseDict = {}
        student = page["Students"].tolist()
        gpa = page["GPA"].tolist()
        A = page["A"].tolist()
        AB = page["AB"].tolist()
        B = page["B"].tolist()
        BC = page["BC"].tolist()
        C = page["C"].tolist()
        D = page["D"].tolist()
        try:
            F = page["F"].tolist()
        except:
            F = ["."]
        for i in range(len(courseNumList)):
            course_num, section = courseNumList[i], sectionList[i]
            if gpa[i] == ".": gpa[i] = "NaN"
            if A[i] == ".": A[i] = 0
            if AB[i] == ".": AB[i] = 0
            if B[i] == ".": B[i] = 0
            if BC[i] == ".": BC[i] = 0
            if C[i] == ".": C[i] = 0
            if D[i] == ".": D[i] = 0
            if F[i] == ".": F[i] = 0
            if gpa[i] != "NaN": mu = float(gpa[i])
            (A[i], AB[i], B[i], BC[i], C[i], D[i], F[i], gpa[i]) = tuple(map(float, (A[i], AB[i], B[i], BC[i], C[i], D[i], F[i], gpa[i])))
            def vari():
                deviation = [
                    (4.0-mu)*(4.0-mu) * A[i] / 100,
                    (3.5-mu)*(3.5-mu) * AB[i] / 100,
                    (3.0-mu)*(3.0-mu) * B[i] / 100,
                    (2.5-mu)*(2.5-mu) * BC[i] / 100,
                    (2.0-mu)*(2.0-mu) * C[i] / 100,
                    (1.0-mu)*(1.0-mu) * D[i] / 100,
                    (0.0-mu)*(0.0-mu) * F[i] / 100,
                ]
                return sum(deviation)
            course = (page.attrs["Subject"] + " " + str(course_num))
            # print(course, section)
            courseDict[course] = courseDict.get(course, {})
            instructor = self.dir.get_instructor(
                    courseNum = int(course_num), 
                    sectionNum = str(section).zfill(3), 
                    collegeName = str(page.attrs["Subject"]),
                    collegeNum = str(page.attrs["SubjectNum"]), 
                    collegeTerm = str(self.term),
                )
            sections = 1
            readj = lambda letter, prev, count: (letter*(count-1) + prev) / (count)
            if instructor in courseDict[course]:
                sections = 1+courseDict[course][instructor]["distribution"]["Sections"]
                A[i] = readj(A[i], courseDict[course][instructor]["distribution"]["A"], sections)
                AB[i] = readj(AB[i], courseDict[course][instructor]["distribution"]["AB"], sections)
                B[i] = readj(B[i], courseDict[course][instructor]["distribution"]["B"], sections)
                BC[i] = readj(BC[i], courseDict[course][instructor]["distribution"]["BC"], sections)
                C[i] = readj(C[i], courseDict[course][instructor]["distribution"]["C"], sections)
                D[i] = readj(D[i], courseDict[course][instructor]["distribution"]["D"], sections)
                F[i] = readj(F[i], courseDict[course][instructor]["distribution"]["F"], sections)
                gpa[i] = readj(gpa[i], courseDict[course][instructor]["distribution"]["GPA"], sections)
            courseDict[course][instructor] = {
                "distribution": {
                    "A": A[i],
                    "AB": AB[i],
                    "B": B[i],
                    "BC": BC[i],
                    "C": C[i],
                    "D": D[i],
                    "F": F[i],
                    "GPA": gpa[i],
                    "Variance": vari(),
                    "Sections": sections,
                },
            }
        return courseDict

    def extract(self):
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Extracting pages...')
        self.filter()
        self.file = {}
        [ self.file.update(self.generate(page)) for page in tqdm(self.data) ]
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Extracted!')

    def save(self, filename, dir='extracted'):
        self.make_dir(dir)
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Saving to {filename}.JSON...')
        with open(f'{dir}/{filename}.json', 'w') as file:
            json.dump(self.file, file)
        print(f'{Fore.GREEN}[+]{Style.RESET_ALL} Saved to {filename}.JSON!')


if __name__ == "__main__":
    dir = Instructor(
        "../data/pdfs/1214-dir.pdf",
        "all",
    )
    pdf = Extractor(
        "../data/pdfs/1214-grade-report.pdf",
        "all",
        dir
    )
    pdf.extract()
    pdf.save(pdf.term, '../data/extracted')
