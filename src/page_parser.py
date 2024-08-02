from bs4 import BeautifulSoup
import requests


class PageParser(BeautifulSoup):

    BASE_URL = 'https://azcomix.me/'

    def __init__(self, url):
        self.url = url
        if self.BASE_URL not in self.url:
            raise SyntaxError("This is not a comic link as expected")
        else:
            self.reqs = requests.get(self.url)
            super().__init__(self.reqs.text, 'html.parser')

    def page_parse(self, url_whole):
        """Gets the issue links from a series"""

        if '/comic/' in url_whole:
            links = []
            data = self.findAll('a', {"class": "ch-name"})
            for i, a in enumerate(data):
                testlink = data[i].get("href")
                links.insert(0, testlink)

            ans = ('y' in input(f"\nSeries summary: {len(links)} issues found! Proceed to download? (y/n): "))
            if ans:
                return links
            else:
                print("\n=== Download canceled! ===")
                return []
        else:
            return [url_whole]

    def issue_parse(self, url_issue):
        """Pick out the image data from issue page"""
        self.__init__(f"{url_issue}/full")
        images = self.findAll('img')
        return images[1:len(images) - 2]  # skip site garbage images
