import codecs
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup

# check webpage.html file exists
try:
    # Save file first can no longer use requests lib due to ebay bot detection
    file = codecs.open("html/webpage.html", "r", "utf-8")
    html = file.read()
    file.close()
except FileNotFoundError:
    print("File not found - first save webpage.html file as html/webpage.html")
    exit()

# Parse the page
soup = BeautifulSoup(html, 'html.parser')

# Obtain prices
Sale_Price = [(tag.get_text().strip()[1:].replace(',','')) for tag in soup.find_all("span", class_="POSITIVE")]

# Remove strings that share class of POSITIVE
Sale_Price = [price for price in Sale_Price if all(string not in price for string in ["old", "o"])]

# now change to floats
Sale_Price = [float(price) for price in Sale_Price]

plt.hist(Sale_Price, bins=20)

# Average price
print(np.mean(Sale_Price))

# Average price excluding outlier
final_prices = [ price for price in Sale_Price if price > 20]
print(np.mean(final_prices))
plt.hist(final_prices, bins=50)  # arguments are passed to np.histogram
plt.show()
