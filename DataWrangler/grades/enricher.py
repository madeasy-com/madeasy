import json, re
from os import listdir
from collections import defaultdict

# def load(filename):
#     with open(filename, 'r') as file:
#         return json.load(file)

source = '../data/extracted/'
ext = '.json'

def enrich(filename):
    files = listdir(source)
    terms = []
    # check if both dir and grade report exist for each term and only add one term to the list
    [ terms.append(term[:-len(ext)]) for file in files if (term := file) and ext in term and term[:-len(ext)].isnumeric() ]

    data = defaultdict(dict)

    for term in terms:
        with open(source+term+ext, 'r') as f:
            d = json.load(f)
            for k, v in d.items():
                # print(k,v)
                data[k][term] = v
                # print(data) 
                # break
            # print(list(d.values())[0])
    
    save(source+filename+ext, data)
    # print(terms)
    # res = {}
    # res.update()
    

def save(filename, file):
    with open(filename, 'w') as f:
        json.dump(file, f)
        
if __name__ == "__main__":
    enrich('all')