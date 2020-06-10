import requests
import os
import bs4
import re
import json
import sys
from lxml import html
user_agent = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
url = 'https://www.amazon.com.au/FX505DT-IPS-Type-R5-3550H-GeForce-FX505DT-AH51/dp/B07VBK4SYS'
os.makedirs('product-images', exist_ok=True)

# Download the Amazon product page
print('Downloading page %s...' % url)
page = requests.get(url, headers=user_agent)

tree = html.fromstring(page.content)


# TODO: Find the script with data containing image URLs
hiRes = str(tree.xpath('//script[contains(., "ImageBlockATF")]/text()'))
if hiRes == []:
    print('Could not find script data containing hires image urls')
else:
    hiResImages = re.findall('\"hiRes\":\"(https.*?\.jpg)\"', hiRes)

for imgUrl in hiResImages:
    # Download the image.
    print('Downloading image %s...' % (imgUrl))
    res = requests.get(imgUrl)
    res.raise_for_status()

    # Save the image to ./product-images
    imageFile = open(os.path.join('product-images',
                                  os.path.basename(imgUrl)), 'wb')

    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

print('Done.')
