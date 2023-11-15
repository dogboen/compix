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
import progressbar
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, BooleanOptionalAction
import warnings
warnings.simplefilter("ignore")


# =Folder=
def folder(working_path):

	# Create download folder and subfolder(s)
	if not os.path.exists(working_path):
		os.makedirs(working_path)
	os.chdir(working_path)


# =PageParse=
# Gets the issue links from a series, or image set from issue page
def pageparse(url_whole):

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
		return images[1:len(images)-2] # dodge site garbo


# =Download=
# Gets the images from an issue link
def download(images):
	page_count=0
	progress = progressbar.ProgressBar(maxval=len(images)).start()
	for i, image in enumerate(images):

		# get the image source url (could set up more try-catches if not "src")
		url_image = image["src"]

		# get the image content and save files
		r = requests.get(url_image).content
		with open(f"page{i+1}.jpg", "wb+") as f:
			f.write(r)

		# update progressbar
		progress.update()

	progress.finish()

# =Main=
def main():

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

		# Switch back to parent folder
		os.chdir('../../..')



# Set up variables like directory and link and args like full/singleissue

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("series", help="series title as it appears on viewcomics.me")
parser.add_argument("-i", "--issue", type=int, help="(first) Issue number")
parser.add_argument("-t", "--toissue", default=0,type=int, help="to (last) issue number")
parser.add_argument("-f", "--full", action=BooleanOptionalAction, help="grab full set of issues")

# Assign base vars
args = vars(parser.parse_args())
url_base = 'https://viewcomics.org/'
series = args["series"]
issue = args["issue"]
to_issue = args["toissue"]
fullset = args["full"]

# Optional: bring in a whole text file to loop through 

# Main call
main()