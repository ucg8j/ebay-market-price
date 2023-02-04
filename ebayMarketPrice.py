import codecs

import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup

LOW_OUTLIERS = 20
HIGH_OUTLIERS = 400
ITEM = "bose quietcomfort 35 ii for sale _ eBay"
FIRST_N_PRICES = 60
NOT_THESE_ITEMS = ["earbuds", "replacement"]

try:
    # Save file as f"{ITEM}.html" first can no longer use requests lib due to ebay bot detection
    file = codecs.open(f"html/{ITEM}.html", "r", "utf-8")
    html = file.read()
    file.close()
except FileNotFoundError:
    print(f"File not found - first save {ITEM}.html file as html/{ITEM}.html")
    exit()

# Parse the page
soup = BeautifulSoup(html, "html.parser")

# filter out items that are not bose queitcomfort 35 ii
# for each ebay item (identified by class "s-item__wrapper clearfix"), if the span role=heading contains the word "earbuds" filter it out
soup_items = soup.find_all("div", class_="s-item__wrapper clearfix")

# Remove items identified from NOT_THESE_ITEMS
filtered_prices = [
    (tag.get_text().strip()[1:].replace(",", ""))
    for item in soup_items
    if not any(word in item.find("span", role="heading").get_text().lower() for word in NOT_THESE_ITEMS)
    for tag in item.find_all("span", class_="POSITIVE")
]

# Remove strings that share class of POSITIVE and convert to float
sale_price = [float(price) for price in filtered_prices if all(string not in price for string in ["old", "o"])]

# limit to first x prices
sale_price = sale_price[:FIRST_N_PRICES]

# Average price excluding outliers
final_prices = [price for price in sale_price if price > LOW_OUTLIERS and price < HIGH_OUTLIERS]
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
