import os
import requests
from zipfile import ZipFile
from pathlib import Path
from tqdm import tqdm


class FileHandler:
	def __init__(self):
		self.working_path = None
		self.images = None
		self.series_str = None
		self.issue_str = None

	def create_dl_folder(self, series_str, issue_str):
		"""Create download folder and subfolder(s)"""
		self.series_str = series_str
		self.issue_str = issue_str
		self.working_path = f"./download/{series_str}/{series_str}-issue-{issue_str}"
		if not os.path.exists(self.working_path):
			os.makedirs(self.working_path)
		os.chdir(self.working_path)

	def download(self, images, zipping):
		"""Gets the images from an issue link"""

		for i, image in tqdm(enumerate(images), total=len(images)):
			url_image = image["src"]
			r = requests.get(url_image).content
			with open(f"page{i+1}.jpg", "wb+") as f:
				f.write(r)

		if zipping:
			zipdir = Path(os.getcwd())
			os.chdir('..')
			with ZipFile(f'{self.series_str}-issue-{self.issue_str}.cbz', 'w') as issue_cbz:
				for page_file in zipdir.iterdir():
					issue_cbz.write(page_file, arcname=page_file.name)
			if os.path.getsize(issue_cbz.filename) < 1000000:  # under 1Mb - must be borked images
				print(f"OOF - looks like {self.series_str} issue {self.issue_str} is currently borked on the site...")
				os.rename(issue_cbz.filename, issue_cbz.filename + "BROKEN")
			os.chdir('../..')

		else:
			os.chdir('../../..')
