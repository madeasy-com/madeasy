import json, re
from instructor import Instructor

def load(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def enrich(filename):
    raw = load(filename)
    data = {}
    term = re.findall(r'\d{4}', filename)[0]
    for course in raw:
        for section in raw[course]:
            data.update({
                course: {
                    'distribution': raw[course][section]['distribution'],
                    'instructors': instructors(course=course, term=term)[section],
                }
            })
        # for section in course:
            # section.update
        # print(course)
    # save(filename, data)
    print(data)

def save(filename, file):
    with open(filename, 'w') as f:
        json.dump(file, f)
        
if __name__ == "__main__":
    enrich('extracted/1222.json')