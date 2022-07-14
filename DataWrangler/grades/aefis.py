import requests, json
from colorama import Fore, Style
import browser_cookie3 as bc
from math import ceil
from tqdm import tqdm
import time

def search(course):
    '''
    Input: course name e.g. 'E C E 252'
    Output: list of dictionaries containing course information
    '''
    url_bit = requests.utils.quote(course)
    cookies = bc.load()
    response = requests.get(f'https://aefis.wisc.edu/index.cfm/page/AefisService.browse?rf=JSON&entityList=Term,Department,College,Course,User&q={url_bit}&_=1653434599703', cookies=cookies).json()
    return response['DATA']

def id(course):
    '''
    Input: course name e.g. 'E C E 252'
    Output: course id e.g. '406501'
    '''
    return search(course)[0]['Id']

def id_map(id):
    '''
    Converts term id (offical) to term id (aefis internal)
    '''
    id = int(id)
    semester = ((id%10)//2-1)
    x = [122, 123]
    y = [50, 51]
    point_slope = 3*(id//10 - x[0]) + y[0]
    return str(point_slope+semester)
    
def instructors(course, term):
    '''
    Returns dictionary of instructor values mapped to their respective course sections
    Usage: instructors(course, term)['{section}'] -> 'Instructors'
    Example: instructors('E C E 252', '1222')['001'][0]['Name'] -> 'Joseph KRACHEY'
    '''
    cookies = bc.load()
    
    filter = { "TermId" : id_map(term), "course.ConvertToVersionUuid": id(course) }
    filter = json.dumps(filter)
    
    params = {
        'rf': 'JSON',
        'filter': filter,
    }

    response = requests.get('https://aefis.wisc.edu/index.cfm/page/AefisCourseSection.list', params=params, cookies=cookies).json()
    
    def filter(response):
        '''
        Selects only the instructor names and their respective course sections
        '''
        data = {}
        for section in response['DATA']:
            instructor_li = section['InstructorList']
            names = []
            for instructor in instructor_li:
                names.append(instructor['Name'])
                # instructor.pop('Id')
                # instructor.pop('Email')
            # data[section['CourseName'][-3:]] = instructor_li
            data[section['CourseName'][-3:]] = names
        return data
    
    return filter(response)

def instr(term: str, college: str, course: int, section: str, depth: int = 0):
    # Retrieve instructor names
    if depth == 5:
        str(instructors((college).strip()+' '+str(course).strip(), int(term))[str(section)]).replace('[','').replace(']','').replace("'",'')
    if instruct := instructors((college).strip()+' '+str(course).strip(), int(term)):
        return str(instruct[str(section)]).replace('[','').replace(']','').replace("'",'')
    else:
        time.sleep(5)
        instr(term, college, course, section, depth+1)
        


def batch(term):
    '''
    Returns dictionary of instructor values mapped to their respective course sections
    Usage: instructors(course, term)['{course & section}']['Name'] -> 'Instructor Name'
    Example: instructors('E C E 252', '1222')['E C E 252 001']['Name'] -> 'Joseph KRACHEY'
    '''
    cookies = bc.load()
    results, start, total, i  = 100, 0, 100, 0
    
    # Load total number of courses
    filter = { "TermId" : id_map(term) }
    filter = json.dumps(filter)
    
    params = {
        'rf': 'JSON',
        'filter': filter,
        "maxresults": str(0),
        "start": str(0),
    }

    response = requests.get('https://aefis.wisc.edu/index.cfm/page/AefisCourseSection.list', params=params, cookies=cookies).json()
    total = ceil(int(response['recordsFiltered'])//results)
    
    data = {}
    for i in tqdm(range(total)):
        filter = { "TermId" : id_map(term) }
        filter = json.dumps(filter)
        
        params = {
            'rf': 'JSON',
            'filter': filter,
            "maxresults": str(results),
            "start": str(start),
        }

        response = requests.get('https://aefis.wisc.edu/index.cfm/page/AefisCourseSection.list', params=params, cookies=cookies).json()
        
        def filter(response):
            '''
            Selects only the instructor names and their respective course sections
            '''
            data = {}
            for section in response['DATA']:
                instructor_li = section['InstructorList']
                names = []
                for instructor in instructor_li:
                    names.append(instructor['Name'])
                data[section['CourseName']] = names
            return data
        
        data.update(filter(response))
        
        start += results
        i += 1
    
    save(data, f'../data/{term}_key.json')
    return data

def save(data, filename):
    '''
    Saves data to a json file
    '''
    print(Fore.LIGHTCYAN_EX+'Saving database...')
    with open(filename, 'w') as f:
        json.dump(data, f)
        print(Fore.LIGHTGREEN_EX+'Database saved!', Style.RESET_ALL)

def temp(course, term):
    '''
    Test function
    '''
    course_id = f'"{id(course)}"'
    term_id = f'"{id_map(term)}"'
    print(term_id)
    query_li = ['{"course.ConvertToVersionUuid":', course_id, ',"TermId":', term_id, '}']
    query = ''.join(query_li)
    query = requests.utils.quote(query)
    URL = f'https://aefis.wisc.edu/index.cfm/page/AefisCourseSection.list?pdfdelay=0&CoCurricular=false&rf=csv&filter={query}'
    cookies = bc.load()
    res = requests.get(URL, cookies=cookies).text
    print(res)

if __name__ == '__main__':
    # print(batch(1222))
    # temp('e c e 252',1222)
    # test_id_map()
    # print(search('e c e 252'))
    # print(id('e c e 252'))
    # print(instructors('e c e 252',1222))
    # print(instructors('e c e 252',1222)['001'])
    print(instr(1222, 'e c e', 252,'001'))
    # print(instructors('comp sci 300',1222))
    # save(instructors('e c e 252',1222))