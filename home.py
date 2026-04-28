from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()

""" # 1. Fetch the page
url = "https://books.toscrape.com/"
response = requests.get(url)

# Always check the request succeeded before going further
if response.status_code != 200:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

# 2. Parse the HTML
soup = BeautifulSoup(response.content, "html.parser")

# 3. Find all book containers on the page
books = soup.select("article.product_pod")

# 4. Extract data from each book
results = []

for book in books:
    # Title is stored as an attribute, not visible text
    title = book.select_one("h3 a")["title"]

    # Price is the text inside the price element
    price = book.select_one("p.price_color").get_text(strip=True)

    # Rating is encoded as a word in the CSS class: "star-rating Three"
    # We grab the second class name and map it to a number
    rating_word = book.select_one("p.star-rating")["class"][1]
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = rating_map.get(rating_word, 0)

    results.append({
        "title": title,
        "price": price,
        "rating": rating
    })

# 5. Display results
for book in results:
    print(f"{book['title']} | {book['price']} | {book['rating']} stars") """

base_url = os.getenv("BASE_URL")
start_url = os.getenv("START_URL")

all_books = []
url = start_url

while url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for book in soup.select("article.product_pod"):
        title = book.select_one("h3 a")["title"]
        price = book.select_one("p.price_color").get_text(strip=True)
        rating_word = book.select_one("p.star-rating")["class"][1]
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating = rating_map.get(rating_word, 0)
        all_books.append({"title": title, "price": price, "rating": rating})

    # Check for a "next" button and follow it
    next_btn = soup.select_one("li.next a")
    url = base_url + next_btn["href"] if next_btn else None

print(f"Scraped {len(all_books)} books total.")
""" for book in all_books:
    print(f"{book['title']} | {book['price']} | {book['rating']} stars") """