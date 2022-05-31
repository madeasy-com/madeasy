import requests, json

def get(code):
    return requests.get(f'http://data.alext.se/api/course/{code}/').json()

if __name__ == '__main__':
    print(get(1182266300))