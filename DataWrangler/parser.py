from tika import parser
import re

def parse():
    parsed = parser.from_file('test.pdf')
    content = parsed['content']
    term_code = re.findall(r'TERM : .*', content)
    re.findall(r'A AB B BC C D F S U CR N P I NW NR Other', content)
        
if __name__ == '__main__':
    parse()