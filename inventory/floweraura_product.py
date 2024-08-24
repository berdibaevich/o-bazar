from bs4 import BeautifulSoup
import requests
import re
from forex_python.converter import CurrencyRates
from django.core.cache import cache

class GiftProduct:
    MENU = "gifts"
    PARSER = "lxml"
    def __init__(self, url) -> None:
        self.url = url
    

    def slugify(self, name: str):
        slug = re.sub(r'\W+', '-', name.lower()).strip("-")
        return slug

    
    def convert_to_int(self, price: str):
        """
        return price of product expected like this "RS 500" => 500
        """
        num = re.search(r"\d+", price)
        if num:
            return int(num.group())
        return None

    

    def convert_to_usd(self, price: str):
        c = CurrencyRates()
        # get the exchange rate for INR to USD
        exchange = c.get_rate("INR", "USD")
        amount = self.convert_to_int(price)
        if amount is None:
            return None
        usd_amount = amount * exchange
        return f"{usd_amount:.2f} USD"




    def get_html(self, tag: str):
        slug = self.slugify(tag)
        full_path = f"{self.url}/{self.MENU}/{slug}"
        html_string = cache.get(full_path)
        if html_string is None:
            r = requests.get(full_path)
            if r.status_code not in range(200, 299):
                return None
            html_string = r.text
            cache.set(full_path, html_string, timeout=60*60)
        html = BeautifulSoup(html_string, self.PARSER)
        return html



    def get_products_box(self, html):
        """
        Return products Box 
        """
        return html.find("div", {'class': "prod-list-cont"})





    def get_product_info(self, product_detail, i):
        data = {}
        product = product_detail.next_sibling
        div_tag = product.find("div", {"class": "block"})
        a_tag = div_tag.a
        data['id'] = i
        data['name'] = a_tag.string
        data['url'] = a_tag.attrs.get("href")
        price = product.find("span", {"class": "flt price"})
        data['price'] = self.convert_to_int(price.text)
        delivery = product.find("span", {"class": "block earliest"})
        data['delivery'] = delivery.text
        return data


    def get_images(self, product):
        images = []
        data_images = product.find_all("div", {"class": "image-gallery-slide"})
        for image in data_images:
            i = image.find("img")
            if i:
                url = i.attrs.get("src")
                images.append(url)
        return images
    


    def convert_to_list(self, html):
        products = []
        products_box = self.get_products_box(html)
        data = products_box.find_all("div", {"class": "list-item dynamo-item"})
        for i, d in enumerate(data):
            product_data = {}
            product = d.find("div", {"class": "react_firstthing1 react_firstthingDesk1"})
            images = self.get_images(product)
            product_info = self.get_product_info(product, i)
            product_data['info'] = product_info
            product_info['images'] = images

            products.append(product_data)
        return products



    
    def get_products(self, name: str):
        """
        Return product data from gift's category
        [Home & Kitchen, Fashion, More Gifts, Gift Hampers]
        """
        html = self.get_html(name)
        if html is None:
            return []

        products = self.convert_to_list(html)
        return products