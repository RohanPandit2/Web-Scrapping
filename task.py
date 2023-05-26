import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_urls = []
    product_names = []
    product_prices = []
    ratings = []
    num_reviews = []
    asins = []
    product_descriptions = []
    manufacturers = []

    # Extracting product details from the page
    product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})
    for card in product_cards:
        # Product URL
        url = card.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        product_urls.append('https://www.amazon.in' + url)

        # Product Name
        product_name = card.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        product_names.append(product_name)

        # Product Price
        try:
            product_price = card.find('span', {'class': 'a-price-whole'}).text.replace(',', '')
            product_prices.append(float(product_price))
        except:
            product_prices.append(None)

        # Rating
        try:
            rating = card.find('span', {'class': 'a-icon-alt'}).text.split(' ')[0]
            ratings.append(float(rating))
        except:
            ratings.append(None)

        # Number of Reviews
        try:
            num_review = card.find('span', {'class': 'a-size-base'}).text.replace(',', '')
            num_reviews.append(int(num_review))
        except:
            num_reviews.append(None)

        # ASIN
        asin = card['data-asin']
        asins.append(asin)

        # Product Description and Manufacturer
        desc_manuf_div = card.find('div', {'class': 'a-section a-size-base-plus a-text-normal'})
        if desc_manuf_div:
            product_desc = desc_manuf_div.text.strip()
            product_descriptions.append(product_desc)

            manufacturer = desc_manuf_div.find('span', {'class': 'a-size-base'}).text.strip()
            manufacturers.append(manufacturer)
        else:
            product_descriptions.append(None)
            manufacturers.append(None)

    return product_urls, product_names, product_prices, ratings, num_reviews, asins, product_descriptions, manufacturers

def scrape_multiple_pages(num_pages, max_products):
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
    all_product_urls = []
    all_product_names = []
    all_product_prices = []
    all_ratings = []
    all_num_reviews = []
    all_asins = []
    all_product_descriptions = []
    all_manufacturers = []

    products_scraped = 0
    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        product_urls, product_names, product_prices, ratings, num_reviews, asins, product_descriptions, manufacturers = scrape_product_details(url)

        num_products = min(max_products - products_scraped, len(product_urls))

        all_product_urls.extend(product_urls[:num_products])
        all_product_names.extend(product_names[:num_products])
        all_product_prices.extend(product_prices[:num_products])
        all_ratings.extend(ratings[:num_products])
        all_num_reviews.extend(num_reviews[:num_products])
        all_asins.extend(asins[:num_products])
        all_product_descriptions.extend(product_descriptions[:num_products])
        all_manufacturers.extend(manufacturers[:num_products])

        products_scraped += num_products
        if products_scraped >= max_products:
            break

    return all_product_urls, all_product_names, all_product_prices, all_ratings, all_num_reviews, all_asins, all_product_descriptions, all_manufacturers

# Specify the number of pages to scrape (at least 20 in your case) and the maximum number of products to fetch (around 200 in your case)
num_pages_to_scrape = 20
max_products_to_fetch = 200

# Scrape the data
product_urls, product_names, product_prices, ratings, num_reviews, asins, product_descriptions, manufacturers = scrape_multiple_pages(num_pages_to_scrape, max_products_to_fetch)

# Save the data to a CSV file
with open('product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'ASIN', 'Product Description', 'Manufacturer'])
    for i in range(len(product_urls)):
        writer.writerow([product_urls[i], product_names[i], product_prices[i], ratings[i], num_reviews[i], asins[i], product_descriptions[i], manufacturers[i]])

print('Scraping completed!')
