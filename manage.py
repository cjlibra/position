#!/usr/bin/env python
import os
import sys
import codecs  
codecs.register(lambda name: name == 'cp65001' and codecs.lookup('utf-8') or None) 

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "position.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
