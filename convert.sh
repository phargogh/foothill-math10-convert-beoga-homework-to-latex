INPUT_FILE="$1"
VERSION=$(echo $INPUT_FILE | egrep -o '[1-9]\.?[0-9]?')

python convert-to-rst.py "$INPUT_FILE"> $VERSION.ltx && pdflatex $VERSION.ltx && open $VERSION.pdf
