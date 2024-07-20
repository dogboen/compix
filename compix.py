# dogeth 03/2022
#
# Compix - a script to grab and organize comic pictures 
#
# [] Series Link
#  > [] Issue links
#	  > [] Image Links

# Includes
from src.page_parser import PageParser
from src.file_handler import FileHandler
import warnings
warnings.simplefilter("ignore")

logo = [r"                      _     ",
		r" _______  __ _  ___  (_)_ __",
		r"/ __/ _ \/  ' \/ _ \/ /\ \ /",
		r"\__/\___/_/_/_/ .__/_//_\_\ ",
		r"             /_/            "]


def main():
	"""Main Compix loop"""

	user_choice = input("1. Single link mode \n2.File list input mode\nSelect mode: ")
	match int(user_choice):
		case 1:
			print("\n=Link Mode=")
			url = input("Series or Issue link: ")
			parser = PageParser(url)
			issuelinks = parser.page_parse(url)
			download_issues(parser, issuelinks)

		case 2:
			print("\n=File List Mode=")
			list_file = input("List file (full path): ")
			with open(list_file, "r") as f:
				for link in f:
					link = link.rsplit('\n', 1)[0]  # sniff out pesky \n's
					parser = PageParser(link)
					issuelinks = parser.page_parse(link)
					download_issues(parser, issuelinks)

		case _:
			print("\nExiting")
			return


def download_issues(parser, issuelinks):
	"""Process each issue link"""
	filer = FileHandler()
	for i, link in enumerate(issuelinks):

		# Set up the download area and set as working
		series_issue_str = link.rsplit(parser.BASE_URL, 1)[1].rsplit('/issue-')
		filer.create_dl_folder(series_issue_str[0], series_issue_str[1])

		# Download images
		print(f"Downloading {series_issue_str[0]} issue {series_issue_str[1]} ...")
		images = parser.issue_parse(link)
		filer.download(images, zipping=True)


if __name__ == "__main__":
	for line in logo:
		print(line)
	main()
