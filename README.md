# Bitrix24 Mass Updates
 Mass Bitrix24 CRM updates using csv tables and Bitrix24 api

# Requirements
- bitrix24-rest
- nbformat

# How to use
1. Create 'config.py' file and write bitrix24 token from https://example.bitrix24.ru/devops/section/standard/ in it
2. Run main.py script, by default it uses "input.csv" file in the same directory and updates deals in Bitrix24

# Options
- -l - turns on leads updating mode
- -i=filename - input file name, 'input.csv' by default
- -o=filename - output file name for errors, 'output.csv' by default
- -e=encoding - input file encoding, 'utf-8' by default
- -d - delimiter specifying, ';' by default
