#!/bin/bash
source generate.sh
open Frontend/html/index.html &
python3 Backend/main.py
