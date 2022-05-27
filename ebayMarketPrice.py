import codecs

import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup

LOW_OUTLIERS = 551
HIGH_OUTLIERS = 2500
ITEM = "m1-16gb-pro"
FIRST_N_PRICES = 50

try:
    # Save file as f"{ITEM}.html" first can no longer use requests lib due to ebay bot detection
    file = codecs.open(f"html/{ITEM}.html", "r", "utf-8")
    html = file.read()
    file.close()
except FileNotFoundError:
    print("File not found - first save webpage.html file as html/webpage.html")
    exit()

# Parse the page
soup = BeautifulSoup(html, "html.parser")

# Obtain prices
sale_price = [
    (tag.get_text().strip()[1:].replace(",", ""))
    for tag in soup.find_all("span", class_="POSITIVE")
]

# Remove strings that share class of POSITIVE
sale_price = [
    price for price in sale_price if all(string not in price for string in ["old", "o"])
]

# now change to floats
sale_price = [float(price) for price in sale_price]

# limit to first x prices
sale_price = sale_price[:FIRST_N_PRICES]

# Initial plot to see outliers.
# plt.hist(Sale_Price, bins=20)

# Average price excluding outliers
final_prices = [
    price for price in sale_price if price > LOW_OUTLIERS and price < HIGH_OUTLIERS
]
pct_25, pct_75 = np.percentile(final_prices, [25, 75])

stats = (
    f"mean: {round(np.mean(final_prices), 2)}\n"
    f"median: {round(np.median(final_prices), 2)}\n"
    f"25th %ile: {round(pct_25, 2)}\n"
    f"75th %ile: {round(pct_75, 2)}\n"
)

print(stats)

plt.hist(final_prices, bins=20)
plt.title(f"{ITEM}")
plt.figtext(0.67, 0.7, stats)
plt.show()
