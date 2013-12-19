#! /usr/bin/env python

import sys
import os
import commands

def main(argv):
    f_name =sys.argv[2]+sys.argv[1]
    #f_name = "/tmp/file.org"
    s1='commands.getoutput("emacs --batch '
    s2=" --eval '"
    s3="(org-export-as-html nil)'"
    s4='")'
    out = str(s1)+str(f_name)+str(s2)+str(s3)+str(s4)
    exec out

if __name__ == "__main__":
    main(sys.argv)

