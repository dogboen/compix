# dogeth 03/2022
#
# Compix - a script to grab and organize comic pictures 
#

# Includes
import os 
from bs4 import *
import requests
import progressbar
from time import sleep
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import warnings
warnings.simplefilter("ignore")


# =Folder=
def folder(working_path):

	# Create download folder and subfolder(s)
	if not os.path.exists(working_path):
		os.makedirs(working_path)
	os.chdir(working_path)


# =PageParse=
def pageparse(url_whole):

	print(f"\nGrabbing images from: {url_whole}...")
	sleep(1)

	# Parse the page for the image sources
	reqs = requests.get(url_whole)
	soup = BeautifulSoup(reqs.text, 'html.parser')
	images = soup.findAll('img')

	return images


# =Download=
def download(images):
	page_count=0
	with progressbar.ProgressBar(max_value=len(images)) as bar:
		for i, image in enumerate(images):

			# skip first, and last two images (site garbo)
			if i==0 or i==len(images)-2 or i==len(images)-1:
				continue

			# get the image source url (could set up more try-catches if not "src")
			url_image = image["src"]

			# get the image content and save files
			r = requests.get(url_image).content
			with open(f"page{page_count}.jpg", "wb+") as f:
				f.write(r)
			page_count+=1
			bar.update(i)


# =Main=
def main():

	# Loop through all the issues
	
	if not to_issue: # Single issue case
		last_issue = issue
	else:
		last_issue = to_issue

	for i in range(issue,last_issue+1):

		# Set up the download area and set as working
		folder(f"./download/{comic_series}/issue-{i}")

		# Process site data for image links
		images = pageparse(f"{url_base}{comic_series}/issue-{str(i)}/full" )

		print(f"\nIssue {str(i)} found, Pages: {str(len(images))}")
		sleep (1)

		# Download the goods
		download(images)

		# Switch back to parent folder
		os.chdir('../../..')

# Set up variables like directory and link and args like full/singleissue

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("series", help="series title as it appears on viewcomics.me")
parser.add_argument("issue", type=int, help="(first) Issue number")
parser.add_argument("-t", "--toissue", default=0,type=int,help="to (last) issue number")

# Assign base vars
args = vars(parser.parse_args())
url_base = 'https://viewcomics.me/'
comic_series = args["series"]
issue = args["issue"]
to_issue = args["toissue"]


# Optional: bring in a whole text file to loop through 

# Note: url format for whole series is url_base + "comic" + series

# Main call
main()