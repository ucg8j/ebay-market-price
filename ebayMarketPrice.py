import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

# URL of historical prices of a product
url = "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=magic%20trackpad%202&_sacat=3676&LH_Sold=1&LH_Complete=1&Colour=White&_dcat=23160&rt=nc&_udlo=15"

# Get page
r = requests.get(url) 

# Parse the page
soup = BeautifulSoup(r.content, 'html.parser')

# Obtain prices TODO write fn for the strip/replace for readability
Sale_Price = [ (tag.get_text().strip()[1:].replace(',',''))  for tag in soup.find_all("span", class_="POSITIVE") ]

# Hack FIX: dates are appearing even though they don't have a class of "POSITIVE"
# Remove dates
Sale_Price = [i for i in Sale_Price if "2020" not in i]

# weird string in list
if 'o' in Sale_Price:
  Sale_Price.remove('o')

# now change to floats
Sale_Price = [float(price) for price in Sale_Price]

plt.hist(Sale_Price, bins=20)  # arguments are passed to np.histogram

# Average price
print(np.mean(Sale_Price))

# Average price excluding outlier
final_prices = [ price for price in Sale_Price if price > 20 ]
print(np.mean(final_prices))
plt.hist(final_prices, bins=50)  # arguments are passed to np.histogram
