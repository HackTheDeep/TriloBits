#!/anaconda3/bin/python

import requests
import bs4
import re
import urllib.request
import os

def download_images(img_urls, dest_dir):
  """Given the urls, downloads
  each image into the destination directory.
  Gives the images local filenames img0, img1, and so on.
  Creates the directory if necessary.
  """
  amnh = 'https://www.amnh.org/'
  abs_dest = os.path.abspath(dest_dir)

  if not os.path.exists(abs_dest):
    os.makedirs(abs_dest)

  for i in range(len(img_urls)):
    print('Retrieving...', img_urls[i])

    item =  img_urls[i].split('/')[-1]
    urllib.request.urlretrieve(amnh + img_urls[i], abs_dest + '/' + item)

def scraper(num_pages, dest_dir):
    url = 'https://www.amnh.org/our-research/paleontology/paleontology-faq/trilobite-website/trilobites-dl/trilobite-images-folder'
    page_count = 10

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for page in range(num_pages):
        print('-' * 20, '\nFetching Page', page, 'imgs\n' + '-' * 20, '\n')

        # Setups URL for each of the 88 pages
        a = url.split('/')

        if page == 1:
            a.append('(offset)')
            a.append(str(page_count))

        elif page >= 2:
            page_count += 10
            a.pop()
            a.append(str(page_count))

        # New page_url
        url = '/'.join(a)

        html_doc = requests.get(url).text
        soup = bs4.BeautifulSoup(html_doc, 'html.parser')

        img_urls = re.findall(r' in-standard-src="/(\S*jpg)', html_doc)

        # remove '_small.jpg' for full-scale imgs
        for i in range(len(img_urls)):
            img_urls[i] = img_urls[i][:-10] + '.jpg'

        download_images(img_urls, dest_dir)

def main():
    scraper(88, 'trilobite')

if __name__ == '__main__':
    main()
