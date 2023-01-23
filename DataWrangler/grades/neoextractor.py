from colorama import Fore, Style
import numpy as np, json
from neoparse import Parser
from instructor import Instructor
from tqdm import tqdm
from collections import defaultdict

class Extractor(Parser):
    
    def __init__(self, filename, dir: Instructor = None):
        super().__init__(filename)
        self.dir = dir
    
    def generate(self):
        offerings = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        for offering in tqdm(self.data.itertuples(index=False), total=len(self.data.index)):
            # print(offering)
            course = (offering.Dept_Name + " " + offering.Course)
            # print(course, section)
            instructor = self.dir.get_instructor(
                courseNum = int(offering.Course), 
                sectionNum = str(offering.Section), 
                collegeName = str(offering.Dept_Name),
                collegeNum = str(offering.Dept_Code), 
                collegeTerm = str(self.term),
            )
            # instructor = 'TEST'
            sections = 1
            readj = lambda new, prev, count: (new*(dist['Students']) + prev*(old["Students"])) / (count)
            dist = {'A': offering.A, 'AB': offering.AB, 'B': offering.B, 'BC': offering.BC, 'C': offering.C, 'D': offering.D, 'F': offering.F, 'GPA': offering.GPA, 'Students': offering.Students, 'Sections': sections}
            if instructor in offerings[course]:
                old = offerings[course][instructor]["distribution"]
                dist['Sections'] = 1+old["Sections"]
                sum_students = dist['Students']+old["Students"]
                dist['A'] = readj(dist['A'], old["A"], sum_students)
                dist['AB'] = readj(dist['AB'], old["AB"], sum_students)
                dist['B'] = readj(dist['B'], old["B"], sum_students)
                dist['BC'] = readj(dist['BC'], old["BC"], sum_students)
                dist['C'] = readj(dist['C'], old["C"], sum_students)
                dist['D'] = readj(dist['D'], old["D"], sum_students)
                dist['F'] = readj(dist['F'], old["F"], sum_students)
                dist['GPA'] = readj(dist['GPA'], old["GPA"], sum_students)
                dist['Students'] += old["Students"]
            offerings[course][instructor] = {
                "distribution": {
                    "GPA": dist['GPA'],
                    "A": dist['A'],
                    "AB": dist['AB'],
                    "B": dist['B'],
                    "BC": dist['BC'],
                    "C": dist['C'],
                    "D": dist['D'],
                    "F": dist['F'],
                    "Students": dist['Students'],
                    "Sections": dist['Sections'],
                    # "Variance": vari(),
                },
            }
        # print(offerings)
        return offerings

    def extract(self):
        print(f'{Fore.LIGHTBLUE_EX}[+]{Style.RESET_ALL} Extracting pages...')
        self.file = self.generate()
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
    # dir = None
    pdf = Extractor(
        "../data/pdfs/1214-grade-report.pdf",
        dir
    )
    pdf.extract()
    # pdf.generate()
    pdf.save(pdf.term, '../data/extracted')
