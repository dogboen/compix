# Compix
## a script to grab and organize comic pictures

### Requirements

requires the following additional packages to be installed: BeautifulSoup, ProgressBar
```
pip install bs4 progressbar
```

### Usage
```
usage: compix.py [-h] [-t] series issue

positional arguments:
  series                series title as it appears on viewcomics.me
  issue                 (first) Issue number

options:
  -h, --help            show this help message and exit
  -t, --toissue         to (last) issue number 
```

### Examples
Find the series on viewcomics first to ensure you have the right format (include year)

*If using .exe version, just replace "py compix.py" with "compix.exe"*

Example 1: Get Issue 3 of Morbius
```
py compix.py morbius 3 
```

Example 2: Get issues 21-26 of Daredevil (2019)
```
py compix.py daredevil-2019 21 -t 26
```

