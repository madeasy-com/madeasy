import requests, box_downloader as box
from bs4 import BeautifulSoup
from boxsdk import DevelopmentClient

def links():
    '''
    Get the links to the distribution PDFs from the registrar's website
    '''
    res = requests.get('https://registrar.wisc.edu/grade-reports/')
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.find_all('tbody')
    links = [ linker['href'] for linker in tables[1].find_all('a') ]
    return links
    
def download():
    '''
    I am using selenium to download from box, hopefully there is a better way to get the PDF downloads from box than this that we can shift to in the future.
    '''
    box.download(links())
    
if __name__ == '__main__':
    print(links())
    download()