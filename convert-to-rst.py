import os
import re
import sys
import html
import urllib.parse
import re

from bs4 import BeautifulSoup


def is_question(paragraph):
    try:
        return 'indent' not in paragraph['class']
    except KeyError:
        return True

def escape(text):
    for specialchar in '$%&#_{}!':
        text = text.replace(specialchar, f'\\{specialchar}')
    return text


def generate_latex(source_html_path):
    soup = BeautifulSoup(open(source_html_path).read(), 'html.parser')
    output_string = ""
    output_string += '\\documentclass[a4paper, twoside, 11pt]{article}\n'
    output_string += '\\usepackage{graphicx}\n'
    output_string += '\\usepackage[space]{grffile}\n'
    output_string += '\\usepackage{enumitem}\n'
    output_string += '\\renewcommand{\\theenumi}{\\alph{enumi}}\n'
    output_string += '\\begin{document}\n'

    title = soup.h1.text.replace(' - ', ' \\textemdash{} ').strip()

    for index, paragraph in enumerate(soup.find_all('p')):
        if is_question(paragraph):
            if index > 0:
                output_string += '\\newpage\n'

            output_string += '\n'
            output_string += f'{{\\scshape {title}}}\n\n'
            output_string += '\\bigskip\n'
            output_string += f'{escape(paragraph.text)}\n'
        elif paragraph.img:  # will be None if not here.
            img_src = (urllib.parse.unquote(
                html.unescape(paragraph.img['src'])))
            file_path, ext = os.path.splitext(img_src)
            output_string += '\\begin{center}\n'
            output_string += (
                f'\\includegraphics[width=10cm]{{./{{{file_path}}}{ext}}}\n')
            output_string += '\\end{center}\n'
        else:
            output_string += '\\bigskip\n\n'
            output_string += '\\begin{enumerate}[itemsep=0em]\n'

            for line in re.split('\([a-z]\)', paragraph.text.strip()):
                line = line.replace('\n', ' ').strip()
                if not line:
                    continue

                #for line in paragraph.text.strip().split('\n'):
                output_string += f'\\item {escape(line.strip())}\n'
            output_string += '\\end{enumerate}\n'
    output_string += '\\end{document}'

    return output_string


if __name__ == '__main__':
    print(generate_latex(sys.argv[1]))
