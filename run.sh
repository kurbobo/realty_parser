#!/bin/sh
cd search
for i in $(seq 1 80)
do
   python3 search_cian.py
done
