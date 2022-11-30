# Generate Documentation

pdoc -o documentation -f --html .

pdoc -f --pdf . > documentation/documentation.md
pandoc --metadata=title:"PhoneBook Documentation"               \
       --from=markdown+abbreviations+tex_math_single_backslash  \
       --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans"   \
       --toc --toc-depth=4 --output=documentation/documentation.pdf  documentation/documentation.md
