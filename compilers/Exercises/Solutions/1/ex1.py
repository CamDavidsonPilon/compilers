# ex1.py
#
# Problem: Tokenize 'a = 3 + (4 * 5)'

import re

ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER>\d+)'
SPACE = r'(?P<SPACE>\s+)'

patterns = [ID, NUMBER, SPACE]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        m = pat.match(text,index)
        if m:
            if m.lastgroup != 'SPACE':
                yield (m.lastgroup, m.group())
            index = m.end()
        else:
            print('Bad character %r' % text[index])
            index += 1

text = 'abc 123 $ cde 456'

for tok in tokenize(text):
    print(tok)

