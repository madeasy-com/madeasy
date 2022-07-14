from colorama import Fore, Style
import numpy as np, json
from parse import Parser
from course_instructor import Instructor
from tqdm import tqdm

class Extractor(Parser):
    
    def generate(self, page):
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
        try:
            F = page["F"].tolist()
        except:
            F = ["."]
        for i in range(len(classList)):
            try:
                sectionList.append(classList[i][-3:])
            except:
                sectionList.append(classList[-3:])
            classList[i] = classList[i][:3]
        for i in range(len(classList)):
            if gpa[i] == ".":
                gpa[i] = "NaN"
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
            course = (page.attrs["Subject"] + " " + classList[i])
            courseDict[course] = {
                sectionList[i]: {
                    "distribution": {
                        "A": A[i],
                        "AB": AB[i],
                        "B": B[i],
                        "BC": BC[i],
                        "C": C[i],
                        "D": D[i],
                        "F": F[i],
                        "Mean": float(gpa[i]),
                        "SD": SD,
                    },
                    "instructors": self.dir.get_instructor(
                        courseNum = int(classList[i]), 
                        sectionNum = str(sectionList[i]), 
                        collegeName = str(page.attrs["Subject"]),
                        collegeNum = str(page.attrs["SubjectNum"]), 
                        collegeTerm = str(pdf.term),
                    ),
                }
            }
        return courseDict

    def extract(self):
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Extracting ...')
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
        "../data/pdfs/1222-dir.pdf",
        "all",
    )
    pdf = Extractor(
        "../data/pdfs/1222-grade-report.pdf",
        "all",
        dir
    )
    pdf.extract()
    pdf.save(pdf.term, '../data/extracted')
