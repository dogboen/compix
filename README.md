# Compix
## a script to grab and organize comic pictures

### Requirements

requires the following additional packages to be installed: BeautifulSoup, ProgressBar
```
pip install bs4 progressbar
```

### Usage
```
usage: compix.py [-h] [-s SERIES] [-i ISSUE]

options:
  -h, --help            show this help message and exit
  -s SERIES, --series SERIES
                        Series title as it appears on viewcomics.me (default: the-amazing-spider-man-1963)
  -i ISSUE, --issue ISSUE
                        Issue number (default: 1)
```

### Grabbing multiple at once (Windows)

The following example will download the first 3 issues of Morbius. 
Define a range where (1,1,3) = (first, increment, last)
```
for /l %c in (1,1,3); do py compix.py -s "morbius" -i %c
```