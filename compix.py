# dogeth 03/2022
#
# Compix - a script to grab and organize comic pictures 
#

# Includes

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import warnings
warnings.simplefilter("ignore")
import wget
import os 
from bs4 import *
import requests
import progressbar
from time import sleep


# Set up variables like directory and link and args like full/singleissue
	# update for arguments
url_base = 'https://viewcomics.me/'
comic_series = 'the-boys'
issue = 64

url_whole = f"{url_base}{comic_series}/issue-{str(issue)}/full" 
working_path = f"./download/{comic_series}/issue-{issue}"

# Optional: bring in a whole text file to loop through 


# Create download folder and subfolder(s)
if not os.path.exists(working_path):
	os.makedirs(working_path)
os.chdir(working_path)


# Parse the page for the image sources

print(f"Grabbing images from: {url_whole}")

reqs = requests.get(url_whole)
soup = BeautifulSoup(reqs.text, 'html.parser')
images = soup.findAll('img')

print(f"Issue {str(issue)} found, Pages: {str(len(images))}")
sleep (2)

# COMMENCE DOWNLOAD :clap:
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