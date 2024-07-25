#!/bin/bash

# Config
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

# Html to png
python3.7 html2pdf_web.py

# png to PDF & SEND s3
python3.7 convertpng2pdf.py


