from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    value = request.form['search_value']

    # Amazon scraping
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.in/")
    search_bar_amazon = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "field-keywords"))
    )
    search_bar_amazon.send_keys(value)
    search_bar_amazon.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    html_source = driver.page_source
    soup_amazon = BeautifulSoup(html_source, "html.parser")
    amazon_product_name = [name.text for name in soup_amazon.find_all(class_="a-size-base-plus a-color-base a-text-normal")]

    amazon_product_price = soup_amazon.find_all(class_="a-price-whole")
    all_amazon_prices = [price.getText() for price in amazon_product_price]
    driver.quit()

    # Flipkart scraping
    driver = webdriver.Chrome()
    driver.get("https://www.flipkart.com/")
    search_bar_flipkart = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "q"))
    )
    search_bar_flipkart.send_keys(value)
    search_bar_flipkart.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    html_source = driver.page_source
    soup_flipkart = BeautifulSoup(html_source, "html.parser")
    if soup_flipkart.find_all(class_="s1Q9rs")==[]:
        flipkart_product_name = [name.text for name in soup_flipkart.find_all(class_="IRpwTa")]

    else:
        flipkart_product_name = [name.text for name in soup_flipkart.find_all(class_="IRpwTa")]

    flipkart_product_price = soup_flipkart.find_all(class_="_30jeq3")
    all_flipkart_prices = [price.getText().replace('₹', '') for price in flipkart_product_price]
    driver.quit()

    # Snapdeal scraping
    driver = webdriver.Chrome()
    driver.get("https://www.snapdeal.com/")
    search_bar_snapdeal = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "keyword"))
    )
    search_bar_snapdeal.send_keys(value)
    search_bar_snapdeal.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    html_source = driver.page_source
    soup_snapdeal = BeautifulSoup(html_source, "html.parser")
    snapdeal_product_name = [name.text for name in soup_snapdeal.find_all(class_="product-title")]

    snapdeal_product_price = soup_snapdeal.find_all(class_="lfloat product-price")
    all_snapdeal_prices = [price.getText().replace('Rs.  ', '') for price in snapdeal_product_price]
    driver.quit()

    # Convert the prices to float for comparison
    amazon_prices_float = [float(price.replace(',', '')) for price in all_amazon_prices]
    flipkart_prices_float = [float(price.replace(',', '')) for price in all_flipkart_prices]
    snapdeal_prices_float = [float(price.replace(',', '')) for price in all_snapdeal_prices]

    # Determine the length of the shortest list
    min_length = min(len(amazon_prices_float), len(flipkart_prices_float), len(snapdeal_prices_float), 10)

    # Truncate or pad the lists to the same length
    amazon_prices_float = amazon_prices_float[:min_length]
    flipkart_prices_float = flipkart_prices_float[:min_length]
    snapdeal_prices_float = snapdeal_prices_float[:min_length]

    # Create x-axis values
    x = range(min_length)

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.bar(x, amazon_prices_float, width=0.25, label='Amazon', color='b', align='center')
    plt.bar([i + 0.25 for i in x], flipkart_prices_float, width=0.25, label='Flipkart', color='r', align='center')
    plt.bar([i + 0.5 for i in x], snapdeal_prices_float, width=0.25, label='Snapdeal', color='g', align='center')
    plt.xlabel('Product Index')
    plt.ylabel('Price (₹)')
    plt.title(f'Comparison of {value} Prices on Amazon, Flipkart, and Snapdeal')
    plt.xticks([i + 0.25 for i in x], x)
    plt.legend()
    plt.tight_layout()

    plt.savefig('static/price_comparison.png')
    # ...

# Prepare product data for result.html
    # ...

# Prepare product data for result.html
    amazon_data = list(zip(amazon_product_name, all_amazon_prices))
    flipkart_data = list(zip(flipkart_product_name, all_flipkart_prices))
    snapdeal_data = list(zip(snapdeal_product_name, all_snapdeal_prices))

# Combine data into a single list
    combined_data = list(zip(amazon_data, flipkart_data, snapdeal_data))

# ...

    return render_template('result.html', value=value, combined_data=combined_data)

    # ...

# Prepare product data for result.html
    

# ...

    # return render_template('result.html', value=value, amazon_products=amazon_products, flipkart_products=flipkart_products, snapdeal_products=snapdeal_products)


# ...

    

if __name__ == '__main__':
    app.run(debug=True)
