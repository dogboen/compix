# Compix
### a script to grab and organize comic pictures

## Requirements

Using the .py version requires the following additional packages to be installed: BeautifulSoup, tqdm
```
pip install bs4 tqdm
```

## Usage
```
py compix.py
```
Compix will display a menu to select between regular link mode and file mode

### Link Mode
Paste in a desired full link (i.e. https://azcomix.net/comic/morbius) when prompted <br> 
For whole comics, issues will be counted and user confirms whether to continue <br>
Issues are downloaded into folders and also zipped into .cbz format alongside

### File/List Mode
Create a file with a list of your links separated by line, .txt file is fine <br>
Whether issue or comic series, it will loop through and download them all

Once desired .cbz's are downloaded, ComicTagger is a very helpful tool to tag-match against databases

## Issues
### CBZBROKEN
If you see a .CBZBROKEN file, that means the issue was found to be suspiciously small <br>
Console log will also report this <br>
The source site has a number of problem issues and can be confirmed in browser

### TBP parts
The source site splits TPBs into parts for unknown reasons, not always size <br>
This only becomes an issue if you want to properly tag and sort .cbz's <br>
In this case, use the source folders to zip {issue-tpb-part1}, {issue-tpb-part2}, etc. together and rename .zip extension to .cbz (safe)

07/2024 changelog:
- divided program into 3 modules
- cleaned up and optimized all modes
- improved error reporting and edge case handling
- added support for file list input
- removed input arguments in favor of interactive menu
- able to handle mixes of issues and whole comic links the same way

11/2023 changelog:
- updated to new domain
- replaced progressbar with tqdm
- cleaned up site garbo image handling
- added exporting to cbz
