import os, zipfile, pathlib
from tqdm import tqdm

def folder(working_path):
	"""Create download folder and subfolder(s)"""

	if not os.path.exists(working_path):
		os.makedirs(working_path)
	os.chdir(working_path)





def download(images, zipping):
	"""Gets the images from an issue link"""

	# Progress bar
	for i, image in tqdm(enumerate(images), total=len(images)):

		# get the image source url
		url_image = image["src"]

		# get the image content and save files
		r = requests.get(url_image).content
		with open(f"page{i+1}.jpg", "wb+") as f:
			f.write(r)

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