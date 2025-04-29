import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import json
import sys

class scraper:
    columns = [
        'abslink', 'title', 'authors', 'abstract', 'doi', 'date', 'section'
        ]

    def rempfix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    def __init__(self, sect):
        self.sect = sect
        self.ahrefs = set()

    def loadcsv(self):
        csvhrefs = set()
        try:
            with open(f'fields{self.sect}.csv', 'r', newline='') as csvf:
                reader = csv.DictReader(csvf, dialect='excel-tab')
                for row in reader:
                    csvhrefs.add(row['abslink'])
        except:
            print('It is likely there is not file to read or the format for the file is bad')

        return csvhrefs

    def getupstlinks(self):
        resp = requests.get(f'https://arxiv.org/list/{self.sect}/recent?show=500')
        soup = BeautifulSoup(resp.content, "html.parser")
        items = soup.select("a[title='Abstract']")
        myhrefs = self.loadcsv()

        for itemlinks in items:
            abslink = f'https://arxiv.org{itemlinks['href']}'

            if not abslink in myhrefs:
                self.ahrefs.add(abslink)

        print(self.ahrefs)

    def scrape(self):
        filename = f'fields{self.sect}.csv'
        datacsv = Path(filename)

        writer = None
        fieldnames = None
        if datacsv.is_file():
            csvfile = open(filename, 'a', newline='');
            writer = csv.DictWriter(csvfile, dialect='excel-tab', fieldnames = self.columns)
        else:
            csvfile = open(filename, 'w', newline='');
            writer = csv.DictWriter(csvfile, dialect='excel-tab', fieldnames = self.columns)
            writer.writeheader()

        for article in self.ahrefs:
            try:
                abssoup = BeautifulSoup(requests.get(article).content, 'html.parser')

                title_elem = abssoup.select_one("h1[class^='title']")
                title = []
                for ti in title_elem.children:
                    if ti.name == None:
                        title.append(ti.text)
                title = " ".join(title)
                print(f'Downloading {title}')

                authors = ",".join([au.text for au in abssoup.select("div[class='authors'] a")])

                abs_elem = abssoup.select_one("blockquote[class^='abstract']")
                abstract = []
                for abst in abs_elem.children:
                    if abst.name == None:
                        abstract.append(abst.text.replace('\n',''))
                abstract = " ".join(abstract)


                doi = scraper.rempfix(abssoup.select_one("a[id='arxiv-doi-link']")['href'], 'https://doi.org/')

                date = re.search(r" *(.+) \(.+ KB\)$", abssoup.select_one("div[class='submission-history'] strong").next_sibling.text).group(1)
                section = re.search(r"(.+) \(.+\..+\)$", abssoup.select_one("span[class='primary-subject']").text).group(1)
                writer.writerow({
                    'abslink' : article,
                    'title' : title,
                    'authors' : authors,
                    'abstract' : abstract,
                    'doi' : doi,
                    'date' : date,
                    'section' : section
                    })
            except KeyboardInterrupt:
                break
            except:
                print("Error al descargar uno de los artículos, en fin...");
                continue


def main():
    section = sys.argv[1]
    #scrapcl = scraper("cs.CL")
    scrapcl = scraper(section)
    scrapcl.getupstlinks()
    scrapcl.scrape()

if __name__ == "__main__":
    main()
