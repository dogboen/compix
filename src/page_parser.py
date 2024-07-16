from bs4 import BeautifulSoup
import requests


def pageparse(url_whole):
    """Gets the issue links from a series, or image set from issue page"""

    # Get and parse whole page
    print(f"\nGrabbing data from: {url_whole}...")
    reqs = requests.get(url_whole)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    # For fullset, we're on series page, so get all available issue links
    if '/comic/' in url_whole:
        links =[]
        data =soup.findAll('a', {"class": "ch-name"})
        for i, a in enumerate(data):
            testlink =data[i].get("href")

            links.insert(0, testlink)

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
        return images[1:len(images ) -1] # dodge site garbo