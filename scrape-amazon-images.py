import requests
import os
import bs4
url = 'https://www.amazon.com.au/FX505DT-IPS-Type-R5-3550H-GeForce-FX505DT-AH51/dp/B07VBK4SYS'
os.makedirs('product-images', exist_ok=True)

# Download the Amazon product page
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser')

# TODO: Find the high-res URL of the product page
productImgElem = soup.select('.imgTagWrapper img')
if productImgElem == []:
    print('Could not find product image')
else:
    imgUrl = productImgElem[0].get('data-old-hires')

# TODO: Download the image.
print('Downloading image %s...' % (imgUrl))
res = requests.get(imgUrl)
res.raise_for_status()

# TODO: Save the image to ./product-images
imageFile = open(os.path.join('product-images',
                              os.path.basename(imgUrl)), 'wb')

for chunk in res.iter_content(100000):
    imageFile.write(chunk)
imageFile.close()

# TODO: Get next high res product image.

print('Done.')
