#!/bin/sh

htlatex annotated_bibliography
bibtex annotated_bibliography
htlatex annotated_bibliography
