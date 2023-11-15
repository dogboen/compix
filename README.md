# Compix
## a script to grab and organize comic pictures

### Requirements

Using the .py version requires the following additional packages to be installed: BeautifulSoup, ProgressBar
```
pip install bs4 progressbar
```

### Usage
```
usage: compix.py [-h] [-i ISSUE] [-t TOISSUE] [-f | --full] series

positional arguments:
  series                series title as it appears on viewcomics.me

options:
  -h, --help            show this help message and exit
  -i ISSUE, --issue ISSUE
                        (first) Issue number (default: None)
  -t TOISSUE, --toissue TOISSUE
                        to (last) issue number (default: 0)
  -f, --full, --no-full
                        grab full set of issues (default: None)
```

### Examples
Find the series on viewcomics first to ensure you have the right format (include year)

*If using .exe version, just replace "py compix.py" with "compix.exe"*

Example 1: Get Issue 3 of Morbius
```
py compix.py morbius -i 3 
```

Example 2: Get issues 21-26 of Daredevil (2019)
```
py compix.py daredevil-2019 -i 21 -t 26
```

Example 3: Get full set of Monstress
```
py compix.py monstress -f
```

11/2023 changelog:
- updated to new domain
- updates for progressbar
- cleaned up site garbo image handling