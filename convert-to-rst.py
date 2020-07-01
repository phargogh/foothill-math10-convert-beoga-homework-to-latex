import sys

from bs4 import BeautifulSoup


def is_question(paragraph):
    try:
        return 'indent' not in paragraph['class']
    except KeyError:
        return True


def generate_latex(source_html_path):
    soup = BeautifulSoup(open(source_html_path).read(), 'html.parser')
    output_string = ""
    output_string += '\\documentclass[a4paper, twoside, 11pt]{article}\n'
    output_string += '\\begin{document}\n'

    for index, paragraph in enumerate(soup.find_all('p')):
        if is_question(paragraph):
            if index > 0:
                output_string += '\\newpage\n'

            output_string += f'{{\\scshape {soup.h1.text} }}\n\n'
            output_string += '\\bigskip\n'
            output_string += f'{paragraph.text}\n'
        else:
            output_string += '\\bigskip\n'
            output_string += '\\begin{enumerate}'
            output_string += '\\itemsep0em\n'  # limit space between items
            for line in paragraph.text.strip().split('\n'):
                output_string += f'  \\item {line.strip()}\n'
            output_string += '\\end{enumerate}\n'
    output_string += '\\end{document}'

    return output_string


if __name__ == '__main__':
    print(generate_latex(sys.argv[1]))
