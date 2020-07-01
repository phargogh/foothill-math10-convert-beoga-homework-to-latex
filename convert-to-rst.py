import sys

from bs4 import BeautifulSoup


def is_question(paragraph):
    try:
        return 'indent' not in paragraph['class']
    except KeyError:
        return True


def generate_latex(source_html_path):
    soup = BeautifulSoup(open(source_html_path).read(), 'html.parser')
    print(r'\documentclass[a4paper, twoside, 11pt]{article}' + '\n')
    print(r'\begin{document}' + '\n')

    for index, paragraph in enumerate(soup.find_all('p')):

        if is_question(paragraph):
            if index > 0:
                print('\\newpage\n')

            print(r'{\scshape ' + soup.h1.text + '}\n\n')
            print(r'\bigskip' + '\n')
            print(f'{paragraph.text}\n')
        else:
            print('\\bigskip\n')
            print('\\begin{enumerate}')
            print('\\itemsep0em\n')  # limit space between items
            for line in paragraph.text.strip().split('\n'):
                print(f'  \\item {line.strip()}')
            print('\\end{enumerate}\n')
    print('\\end{document}')


if __name__ == '__main__':
    generate_latex(sys.argv[1])
