import requests, json, time
from colorama import Fore, Style
from tqdm import tqdm


def terms():
    '''
    Get a dictionary of all the terms available in the database    
    '''
    res = requests.get('https://public.enroll.wisc.edu/api/search/v1/aggregate').json()
    return res['terms']

def course_list(term, query='*'):
    '''
    Generates a list of all the available courses in the database for a given term
    '''
    json_data = {
        'selectedTerm': term,
        'queryString': query,
        'filters': [{'has_child': {'type': 'enrollmentPackage','query': {'bool': {'must': [{'match': {'packageEnrollmentStatus.status': 'OPEN WAITLISTED',},},{'match': {'published': True,},},],},},},},],
        'page': 1,
        'pageSize': 9999,
        'sortOrder': 'SCORE',
    }
    return requests.post('https://public.enroll.wisc.edu/api/search/v1', json=json_data).json()
    
def get(term, subject_id, course_id):
    '''
    Returns a dictionary of information about a course
    Tries 5 times before returning None
    '''
    for i in range(5):
        try:
            return requests.get(f'https://public.enroll.wisc.edu/api/search/v1/enrollmentPackages/{term}/{subject_id}/{course_id}').json()
        except:
            time.sleep(5)
    return None

def generator():
    '''
    Generates a database of all the available courses in the database for all available terms and relevant information
    Format: {term: [courses' information]}
    '''
    database = {}
    terms_info = terms()
    for term in terms_info:
        print(term['longDescription'], 'data downloading...')
        term = term['termCode']
        courses = course_list(term)
        term_courses = []
        for course in tqdm(courses['hits']):
            # Get the course's information
            info = get(term, course['subject']['subjectCode'], course['courseId'])
            # Skip if course information is not available (usually because of server issues)
            if info is None: continue
            # Alternatively, terminate the program if the course information is not available
            # if data is None: raise Exception('Course information not available at this time')
            # Filter the course information (reduces the size of the database)
            term_courses.append(filter(course, info))
            # print(term_courses[-1])
            break
        database[term] = term_courses
    return database

def filter(course, info):
    '''
    TODO: Filters a course's information to only include the relevant information
    '''
    relevant = []
    instructors = set()
    relevant.extend([
        {'generalEd': course['generalEd']},
        {'ethnicStudies': course['ethnicStudies']},
        {'breadths': course['breadths']},
        {'levels': course['levels']}
    ])
    for section in info:
        
        instructor = section['sections'][0]['instructor']
        if instructor is not None: 
            instructor = instructor['personAttributes']['emplid']
            instructors.add(instructor)
            # instructor = instructor['personAttributes']['name']
            # instructors.add((instructor['first'], instructor['middle'], instructor['last'], instructor['legalFirst'], instructor['legalMiddle']))
        relevant.extend([
            section['packageEnrollmentStatus'],
            section['sections'][0]['subject']#.pop('schoolCollegels')#.pop('undergraduateCatalogURI'))#.pop('graduateCatalogURI').pop('departmentURI').pop('uddsFundingSource').pop('schoolCollege').pop('footnotes')
            ])
    relevant.append({
        'instructors': list(instructors),
    })
    return relevant

def save():
    '''
    Saves the database to a JSON file
    '''
    print(Fore.LIGHTCYAN_EX+'Downloading database...')
    database = generator()
    print('Saving database...')
    with open('../data/database.json', 'w') as f:
        json.dump(database, f)
        print(Fore.LIGHTGREEN_EX+'Database saved!', Style.RESET_ALL)

if __name__ == '__main__':
    save()
    # generator()
    # print(get('1232', '185', '021717.79'))
    # print(course_list('1224'))
    # print(course_list('1226')['hits'][123])
    # print(filter(course_list('1226')['hits'][123], get('1232', '266', '024795')))
    # with open('test.json', 'w') as f:
    #     json.dump(get('1232', '266', '024795'), f)
    #     # json.dump(course_list('1226'), f)