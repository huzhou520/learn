#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
from core import main

print(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
print(sys.path)


if __name__ == '__main__':
    print("Begin")
    agent = main.CommandHandler(sys.argv)