# dogeth 03/2022
#
# Compix - a script to grab and organize comic pictures 
#
# [] Series Link
#  > [] Issue links
#	  > [] Image Links

# Includes
import os 
from bs4 import *
import requests
from tqdm import tqdm
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, BooleanOptionalAction
import warnings
import zipfile
import pathlib
warnings.simplefilter("ignore")


def folder(working_path):
	"""Create download folder and subfolder(s)"""

	if not os.path.exists(working_path):
		os.makedirs(working_path)
	os.chdir(working_path)


def pageparse(url_whole):
	"""Gets the issue links from a series, or image set from issue page"""

	# Get and parse whole page
	print(f"\nGrabbing data from: {url_whole}...")
	reqs = requests.get(url_whole)
	soup = BeautifulSoup(reqs.text, 'html.parser')

	# For fullset, we're on series page, so get all available issue links 
	if '/comic/' in url_whole:
		links=[]
		data=soup.findAll('a',{"class":"ch-name"})
		for i, a in enumerate(data):
			testlink=data[i].get("href")
			if 'issue-tpb' in testlink:
				continue # Skip trade paperbacks
			else:
				links.insert(0,testlink)
				
		# Count and confirm w/ user
		ans = input(f"\nSeries summary: {str(len(links))} issues found! Proceed to download? (y/n)")
		if 'y' in ans:
			return links
		else:
			print("\n=====Action canceled!=====\n")
			return
	
	# For issue page, only pick out the image data 
	else:
		images = soup.findAll('img')
		return images[1:len(images)-1] # dodge site garbo


def download(images):
	"""Gets the images from an issue link"""

	# Progress bar
	for i, image in tqdm(enumerate(images), total=len(images)):

		# get the image source url
		url_image = image["src"]

		# get the image content and save files
		r = requests.get(url_image).content
		with open(f"page{i+1}.jpg", "wb+") as f:
			f.write(r)


def main():
	"""Main Compix loop"""

	# Process site data for issue links
	if fullset:
		# Get the full list of issue links
		issuelinks = pageparse(f"{url_base}comic/{series}")
	elif not to_issue: 
		# Single issue link
		issuelinks = [f"{url_base}{series}/issue-{issue}"]
	else:
		# Custom issue range links
		issuelinks = []
		for i in range(issue,to_issue+1):
			issuelinks.append(f"{url_base}{series}/issue-{i}")

	# Process each issue link
	for i, link in enumerate(issuelinks):

		# Set up the download area and set as working
		issue_str = link.rsplit('/',1)[1]
		folder(f"./download/{series}/{issue_str}")
		
		# Parse the issue page for images
		images = pageparse(f"{link}/full")

		# Download the goods
		download(images)

		# Zip to cbz, switch back to parent folder
		if zipping:
			zipdir = pathlib.Path(issue_str)
			os.chdir('..')
			with zipfile.ZipFile(f'{issue_str}.cbz', 'w') as issue_cbz:
				for page_file in zipdir.iterdir():
					issue_cbz.write(page_file, arcname=page_file.name)
			os.chdir('../..')
			# delete images after?
		else:
			os.chdir('../../..')


# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("series", help="series title as it appears on viewcomics.me")
parser.add_argument("-i", "--issue", type=int, help="(first) Issue number")
parser.add_argument("-t", "--toissue", default=0,type=int, help="to (last) issue number")
parser.add_argument("-f", "--full", action=BooleanOptionalAction, help="grab full set of issues")
parser.add_argument("-z", "--zip", action=BooleanOptionalAction, help="zip issue to cbz")

# Assign global vars
args = vars(parser.parse_args())
url_base = 'https://viewcomics.org/'
series = args["series"]
issue = args["issue"]
to_issue = args["toissue"]
fullset = args["full"]
zipping = args["zip"]

# Optional: bring in a whole text file to loop through 

# Main call
if __name__ == "__main__":
	main()