import textwrap
import string

from bs4 import BeautifulSoup


PAGETOP = """
    \documentclass[a4paper, twoside, 11pt]{article}
    \pagestyle{empty}
    \begin{document}
    {\scshape Chapter 1 - Introduction to Statistics}

    \textbf{Homework 1}

    \bigskip
"""

if __name__ == '__main__':
    soup = BeautifulSoup(open('Homework Chapter 1.html').read(), 'html.parser')
    #print(str(soup.h1.text))
    #print('-'*len(str(soup.h1.text)))

    for index, paragraph in enumerate(soup.find_all('p')):
        if index > 1:
            break

        if index % 2 == 0:  # We're on a question:
            print(r'\documentclass[a4paper, twoside, 11pt]{article}' + '\n')
            print(r'\pagestyle{empty}' + '\n')
            print(r'\begin{document}' + '\n')
            print(r'{\scshape ' + soup.h1.text + '}\n\n')
            print(r'\bigskip' + '\n')
            print(f'{paragraph.text}\n')
        else:
            print('\\begin{itemize}')
            for line in paragraph.text.strip().split('\n'):
                line = ' '.join(line.split(' ')[1:])  # Strip leading index
                print(f'  \\item {line}')
            print('\\end{itemize}\n')
            print('\\end{document}')


