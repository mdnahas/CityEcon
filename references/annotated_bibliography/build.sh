#!/bin/sh

htlatex annotated_bibliography
bibtex annotated_bibliography
htlatex annotated_bibliography

# This makes ids match the Bibtex names like "Fischer1995"
sed -i 's/id="X/id="/g' annotated_bibliography.html
# This makes links to those ids work
sed -i 's/href="\#X/href="#/g' annotated_bibliography.html

mv annotated_bibliography.html annotated_bibliography.css ..

