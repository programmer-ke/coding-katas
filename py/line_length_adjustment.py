#!/usr/bin/env python
"""
Adjusts the line length of input text by wrapping long lines at a specified maximum length.
"""

def wrap_line(line, max_length):
    words = line.split()
    wrapped_lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 > max_length:
            wrapped_lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word
    
    if current_line:
        wrapped_lines.append(current_line)
    
    return wrapped_lines

def main():
    max_length = 80
    with open("input.txt", "r") as f_input:
        for line in f_input:
            line = line.strip()
            wrapped_lines = wrap_line(line, max_length)
            for wrapped_line in wrapped_lines:
                print(wrapped_line)

if __name__ == "__main__":
    main()
