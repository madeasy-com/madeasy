from colorama import Fore, Style
import numpy as np, json
from parse import Parser
from instructor import Instructor
from tqdm import tqdm
from collections import defaultdict
from copy import deepcopy

class Extractor(Parser):
    
    def __init__(self, filename, dir: Instructor = None):
        super().__init__(filename)
        self.dir = dir
    
    def generate(self):
        offerings = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        crosslistings = defaultdict(dict)
        decrossed = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        for offering in tqdm(self.data.itertuples(index=False), total=len(self.data.index)):
            # print(offering)
            course = (offering.Dept_Name + "_" + offering.Course)
            # print(course, section)
            instructor = self.dir.get_instructor(
                courseNum = int(offering.Course), 
                sectionNum = str(offering.Section), 
                collegeName = str(offering.Dept_Name),
                collegeNum = str(offering.Dept_Code), 
                collegeTerm = str(self.term),
            )
            if instructor == '': instructor = "UNKNOWN" # Keys cannot be empty strings in Firebase
            # instructor = 'TEST'
            
            dist = {'A': offering.A, 'AB': offering.AB, 'B': offering.B, 'BC': offering.BC, 'C': offering.C, 'D': offering.D, 'F': offering.F, 'GPA': offering.GPA, 'Students': int(offering.Students), 'Sections': 1}
            
            # Find crosslisted courses
            pk = offering.Course+'_'+instructor+'_'+offering.Section
            if (pk not in crosslistings):
                crosslistings[pk][offering.Dept_Name] = (dist)
                decrossed[offering.Dept_Name+'_'+offering.Course][instructor][offering.Section] = (dist)
            else:
                changelog = [False] * (len(crosslistings[pk])+1)
                for i, (k, other) in enumerate(crosslistings[pk].items()): 
                    if k != offering.Dept_Name and other != dist and instructor != 'UNKNOWN': 
                        changelog[i] = True
                        # We know that the same course cannot have been added twice to crosslistings
                        # So this means that the course is crosslisted
                        # pass
                        readj = lambda new, prev, count: (new*(dist['Students']) + prev*(other["Students"])) / (count)
                        # Section Count Remains same, just need to merge both listing's data
                        sum_students = dist['Students']+other["Students"]
                        dist['A'] = readj(dist['A'], other["A"], sum_students)
                        dist['AB'] = readj(dist['AB'], other["AB"], sum_students)
                        dist['B'] = readj(dist['B'], other["B"], sum_students)
                        dist['BC'] = readj(dist['BC'], other["BC"], sum_students)
                        dist['C'] = readj(dist['C'], other["C"], sum_students)
                        dist['D'] = readj(dist['D'], other["D"], sum_students)
                        dist['F'] = readj(dist['F'], other["F"], sum_students)
                        dist['GPA'] = readj(dist['GPA'], other["GPA"], sum_students)
                        dist['Students'] += other["Students"]
                dept = list(crosslistings[pk].keys())
                for i, changed in enumerate(changelog):
                    if not changed: continue
                    crosslistings[pk][dept[i]] = deepcopy(dist)
                    decrossed[dept[i]+'_'+offering.Course][instructor][offering.Section] = (deepcopy(dist))
                crosslistings[pk][offering.Dept_Name] = (dist)
                decrossed[offering.Dept_Name+'_'+offering.Course][instructor][offering.Section] = (deepcopy(dist))
                

            
            
        for (course, offering) in tqdm(decrossed.items()):
            # Merge all sections of a course taught by the same instructor
            for instructor in offering:
                dist = {'A': 0, 'AB': 0, 'B': 0, 'BC': 0, 'C': 0, 'D': 0, 'F': 0, 'GPA': 0, 'Students': 0, 'Sections': 0}
                for section in offering[instructor].values():
                    for k in ['Students', 'Sections']: dist[k] += section[k]
                    for k in ['A', 'AB', 'B', 'BC', 'C', 'D', 'F', 'GPA']: dist[k] += (section[k]*section['Students'])
                for k in ['A', 'AB', 'B', 'BC', 'C', 'D', 'F', 'GPA']: dist[k] /= dist['Students']
                offerings[course][instructor] = dist
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
