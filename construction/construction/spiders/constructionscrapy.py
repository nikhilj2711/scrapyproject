import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scrapy.selector import Selector
import time

class ConstructionscrapySpider(scrapy.Spider):
    name = "constructionscrapy"
    allowed_domains = ["www.bayut.com"]
    start_urls = ["https://www.bayut.com/to-rent/property/dubai/"]

    def __init__(self, *args, **kwargs):
        super(ConstructionscrapySpider, self).__init__(*args, **kwargs)
        
        # Provide the path to ChromeDriver directly
        chrome_driver_path = "/home/hp/scrapyproject/scrapy__project/scrapyproject/construction/construction/chromedriver"  # Replace with the actual path to your ChromeDriver
        self.driver = webdriver.Chrome(service=Service(chrome_driver_path))
        self.driver.implicitly_wait(10)

    def parse(self, response):
        # Open the URL with Selenium
        self.driver.get(self.start_urls[0])

        while True:
            # Create a Scrapy Selector from the Selenium page source
            sel = Selector(text=self.driver.page_source)

            # Extract property information
            properties = sel.css('div._475e888a._5d46b9fb')
            for property in properties:
                item = {
                    # 'title': property.css('h2.card--title a::text').get(),
                    'price': response.css('div._2923a568 span.dc381b54::text').getall(),
                    # 'location': property.css('div.card-location span span::text').get(),
                    # 'bedrooms': property.css('div.card-type span.bedrooms::text').get(),
                    # 'bathrooms': property.css('div.card-type span.bathrooms::text').get(),
                    # 'area': property.css('div.card-type span.size::text').get(),
                    # 'image_url': property.css('img.card--img::attr(src)').get(),
                    # 'url': property.css('a::attr(href)').get(),
                }
                yield item

            # Find the next page URL from the pagination element
            next_page = sel.css('a._95dd93c1::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.driver.get(next_page_url)
                time.sleep(3)  # Wait for the page to load
            else:
                break  # Exit loop if there is no next page

        # Close the Selenium driver after finishing the pagination
        self.driver.quit()
