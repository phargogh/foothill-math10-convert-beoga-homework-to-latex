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
    #output_string += '\\usepackage{float}\n'
    #output_string += '\\restylefloat{table}\n'
    output_string += '\\renewcommand{\\theenumi}{\\alph{enumi}}\n'
    output_string += '\\begin{document}\n'

    title = soup.h1.text.replace(' - ', ' \\textemdash{} ').strip()

    index = -1
    for section in soup.html.body.children:
        if section == '\n':
            continue
        if section.name == 'h1':
            continue
        index += 1

        if re.match('^[1-9][0-9]?\\.', section.text.strip()):  # start of a question
            if index > 0:
                output_string += '\\newpage\n'

            output_string += '\n'
            output_string += f'{{\\scshape {title}}}\n\n'
            output_string += '\\bigskip\n'
            output_string += f'{escape(section.text)}\n'

        elif section.img:
            img_src = (urllib.parse.unquote(
                html.unescape(section.img['src'])))
            file_path, ext = os.path.splitext(img_src)
            output_string += '\\begin{center}\n'
            output_string += (
                f'\\includegraphics[width=10cm]{{./{{{file_path}}}{ext}}}\n')
            output_string += '\\end{center}\n'

        elif section.name == 'table':
            output_string += '\\begin{table}[h]\n'
            output_string += '\\centering\n'
            output_string += f'\\caption{{{section.caption.text.strip()}}}\n'

            # Add one extra column for the label.
            n_cols = '|'.join(['c'] * (
                len(section.tbody.find_all('tr')[0].find_all('td')) + 1))
            n_rows = len(section.tbody.find_all('tr'))
            output_string += f'\\begin{{tabular}}{{{n_cols}}}\n'
            output_string += '\\hline\n'

            for row_index, row in enumerate(section.tbody.find_all('tr')):
                row_string = f'\\textbf{{{escape(row.th.text)}}}'
                for field in row.find_all('td'):
                    row_string += f' & {escape(field.text)}'
                output_string += row_string

                # Can only have tex linebreaks before the end of the last row.
                if row_index < (n_rows - 1):
                    output_string += '\\\\'
                output_string += '\n'

            output_string += '\\end{tabular}\n'
            output_string += '\\end{table}\n'

        elif section.text.strip().startswith('(a)'):
            output_string += '\\bigskip\n\n'
            output_string += '\\begin{enumerate}[itemsep=0em]\n'

            for line in re.split('\([a-z]\)', section.text.strip()):
                line = line.replace('\n', ' ').strip()
                if not line:
                    continue

                output_string += f'\\item {escape(line.strip())}\n'
            output_string += '\\end{enumerate}\n'

        else:
            output_string += '\\bigskip\n\n'
            output_string += escape(section.text.strip())

    output_string += '\\end{document}'

    return output_string


if __name__ == '__main__':
    print(generate_latex(sys.argv[1]))
