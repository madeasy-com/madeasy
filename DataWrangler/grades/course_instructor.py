import requests, json
from colorama import Fore, Style
import browser_cookie3 as bc

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

def save(data):
    '''
    Saves data to a json file
    '''
    print(Fore.LIGHTCYAN_EX+'Saving database...')
    with open('../data/t.json', 'w') as f:
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
    # temp('e c e 252',1222)
    # test_id_map()
    # print(search('e c e 252'))
    # print(id('e c e 252'))
    print(instructors('e c e 252',1222))
    print(instructors('e c e 252',1222)['001'])
    # print(instructors('comp sci 300',1222))
    # save(instructors('e c e 252',1222))