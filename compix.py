# dogeth 03/2022
#
# Compix - a script to grab and organize comic pictures 
#
# [] Series Link
#  > [] Issue links
#	  > [] Image Links

# Includes
from src.page_parser import pageparse
from src.file_handler import download, folder
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, BooleanOptionalAction
import warnings
warnings.simplefilter("ignore")


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
		issue_str = link.rsplit('/', 1)[1]
		folder(f"./download/{series}/{issue_str}")
		
		# Parse the issue page for images
		images = pageparse(f"{link}/full")

		# Download the goods
		download(images, zipping)


# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("series", help="series title as it appears on viewcomics.org")
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