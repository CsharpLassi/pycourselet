#!/usr/bin/env bash

rm -r build/
rm -r dist/

#Build
python3 setup.py sdist bdist_wheel