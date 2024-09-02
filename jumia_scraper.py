from  selenium import webdriver
import sys
from selectolax.parser import HTMLParser
from selectolax.parser import Node
import json


class ProductUrlScraper:
    def __init__(self, url:str, domainName :str, n_products=10) -> None:
        self.url = url
        self.driver = None
        self.domainName = domainName
        self.n_products = n_products
        self.html = None
        self.data = []


    def get_html(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        self.html = self.driver.page_source
        


    def parse_html(self) -> None:


        tree = HTMLParser(self.html)
        products = tree.css("article.prd a.core")[:self.n_products]
        for pr in products:
            self.data.append(self.domainName + pr.attributes['href'])




    def get_data(self) -> dict:
        return self.data



    def __del__(self):
        if self.driver:
            self.driver.quit()




class ProductScraper:

    def __init__(self, product_url) -> None:
        self.url = product_url
        self.html = None
        self.driver = None
        self.data = {}

    def get_html(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        self.html = self.driver.page_source
        


    def parse_html(self) -> None:
        tree = HTMLParser(self.html)
        infos : list[Node] = tree.css(".col10 span")[:3]
        

        self.data['price_now'] = infos[0].text()
        self.data['price_before'] = infos[1].text()
        self.data['discount_percentage'] = infos[2].text()

    




    def get_data(self) -> dict:
        return self.data



    def __del__(self):
        if self.driver:
            self.driver.quit()
    



def main(argv: list[str]) -> int:
    if len(sys.argv) != 2:
        print('Invalid argument')
        return 0
    jumiaScraper = ProductUrlScraper(f"https://www.jumia.ma/catalog/?q={argv[1]}", 'https://www.jumia.ma')
    jumiaScraper.get_html()
    jumiaScraper.parse_html()

    urls = jumiaScraper.get_data()


    res = {}
    for url in urls:   
        productScraper = ProductScraper(url)
        productScraper.get_html()
        productScraper.parse_html()

        res[url] = productScraper.get_data()

        file = open('data.json', 'w')

        file.write(json.dumps(res,indent=4))





if __name__ == '__main__':
    main(sys.argv)
        
