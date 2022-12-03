import requests as rq 
from bs4 import BeautifulSoup 

import csv

class Scrapper:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    soups: list = []

    shoppings_sites = {"Amazon": {"name": "a-size-base-plus a-color-base a-text-normal", "price": "a-price-whole", "rating": "a-icon-alt"}}

    def __init__(self, site_url: str, search_string: str, pages: int):
        if " " in search_string: search_string.replace(" ", "%20")
        for iter in range(pages):
            page = rq.get(f"{site_url}s?k={search_string}&page={iter+1}", headers=self.headers)
            self.soups.append(BeautifulSoup(page.content, "html.parser"))
        return
    
    def find_by_class(self, type: str, class_name: str):
        return_list = []
        for soup in self.soups:
            soup_list = soup.find_all(type, class_ = class_name)
            for item in soup_list:
                return_list.append(item.get_text())
        return return_list

    def search(self, search_list: list, search_name: str):
        out_list = []
        for iter in range(len(search_list)):
            item = search_list[iter]
            for iter_ in item.split(" "):
                if search_name.lower() == iter_.lower():
                    out_list.append(iter)
                    break
                else: pass
        return out_list


if __name__ == "__main__":
    scrapper = Scrapper("https://amazon.in/", "shoes", 4)
    names = scrapper.find_by_class("span", scrapper.shoppings_sites["Amazon"]["name"])
    prices = scrapper.find_by_class("span", scrapper.shoppings_sites["Amazon"]["price"])
    ratings = scrapper.find_by_class("span", scrapper.shoppings_sites["Amazon"]["rating"])
    positions = scrapper.search(names, "sneakers")

    file = open("Sneakers.csv", "w")
    writer = csv.writer(file)
    writer.writerow(["name", "price", "ratings"])

    for position in positions:
        #print(f"{names[position]}  ===  {prices[position]}  ===  {ratings[position]}")
        writer.writerow([names[position], prices[position], ratings[position]])




