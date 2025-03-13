#!/bin/bash
source ~/miniforge3/etc/profile.d/conda.sh
conda activate pfnv2
cd '/home/kjb3/D1V1/Documents/!Dell64docs/Programming/py/kjb3_programs_2/pfn_2'
jupyter book build '/home/kjb3/D1V1/Documents/!Dell64docs/Programming/py/kjb3_programs_2/pfn_2' --builder pdflatex

# Note: this file was based on the documentation for Jupyter Book (https://jupyterbook.org/).
# Jupyter Book has been released under the BSD-3-Clause License.
