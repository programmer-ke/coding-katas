#!/bin/bash

echo "This is a long line that needs to be wrapped at 80 characters.
This is another long line that needs to be wrapped at 80 characters.
This is a short line." | python py/line_length_adjustment.py
