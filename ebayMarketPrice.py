import codecs
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup


LOW_OUTLIERS = 20
HIGH_OUTLIERS = 250

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
soup = BeautifulSoup(html, "html.parser")

# Obtain prices
Sale_Price = [
    (tag.get_text().strip()[1:].replace(",", ""))
    for tag in soup.find_all("span", class_="POSITIVE")
]

# Remove strings that share class of POSITIVE
Sale_Price = [
    price for price in Sale_Price if all(string not in price for string in ["old", "o"])
]

# now change to floats
Sale_Price = [float(price) for price in Sale_Price]

# Initial plot to see outliers.
# plt.hist(Sale_Price, bins=20)

# Average price excluding outliers
final_prices = [
    price for price in Sale_Price if price > LOW_OUTLIERS and price < HIGH_OUTLIERS
]
pct_25, pct_75 = np.percentile(final_prices, [25, 75])

print(
    f"mean: {np.mean(final_prices)}\n"
    f"median: {np.median(final_prices)}\n"
    f"median: {np.median(final_prices)}\n"
    f"25th percentile: {pct_25}\n"
    f"75th percentile: {pct_75}\n"
)
plt.hist(final_prices, bins=20)
plt.show()
