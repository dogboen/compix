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

	print(f"Grabbing images from: {url_whole}...")
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

	# Set up the download area 
	folder(working_path)

	# Process site data for image links
	images = pageparse(url_whole)

	print(f"Issue {str(issue)} found, Pages: {str(len(images))}")
	sleep (1)

	# Download the goods
	download(images)



# Set up variables like directory and link and args like full/singleissue

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--series", default="the-amazing-spider-man-1963", help="Series title as it appears on viewcomics.me")
parser.add_argument("-i", "--issue", default=1, type=int, help="Issue number")

args = vars(parser.parse_args())

url_base = 'https://viewcomics.me/'

# Series name (i.e. the-boys)
comic_series = args["series"]

# Issue number 
issue = args["issue"]

url_whole = f"{url_base}{comic_series}/issue-{str(issue)}/full" 
working_path = f"./download/{comic_series}/issue-{issue}"

# Optional: bring in a whole text file to loop through 

# Main call
main()