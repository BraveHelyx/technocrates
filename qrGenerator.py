#!/usr/bin/python

import pyqrcode, sys, re

if sys.argv[1] == '-l': # List Mode
    if len(sys.argv) > 2:
        file_path = './' + sys.argv[2]
        fp = open(file_path, 'r') # Open File
        line_counter = 1

        for line in fp.readlines():
            # Check line matches expected syntax
            match_obj = re.match('^(.*) (.*)$', line)
            if (match_obj):
                text = match_obj.group(1)
                output = match_obj.group(2)

                print "Input: %s / Output: %s" % (text, output)

                # Set up and write the file.
                url = pyqrcode.create(text)
                url.png(output, scale=5, module_color=[34,44,45], background=[255,255,255,0])
            else:
                print "Incorrect Syntax on line %d" % line_counter
            line_counter += 1
    else:
        print "Usage in List Mode: qrGenerator.py -l <input file>"
else:   # Default Mode
    if len(sys.argv) == 4:
        url = pyqrcode.create(sys.argv[1])
        url.png(sys.argv[2], scale=int(sys.argv[3]), module_color=[32,37,38], background=[255,255,255,0])
    else:
        print "Usage: %s <string> <output_file> <image_scale>" %  sys.argv[0]
