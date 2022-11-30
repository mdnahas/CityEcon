#!/bin/sh

htlatex annotated_bibliography
bibtex annotated_bibliography
htlatex annotated_bibliography
mv annotated_bibliography.html annotated_bibliography.css ..

