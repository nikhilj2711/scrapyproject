import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scrapy.selector import Selector
import time

class PriceSpider(scrapy.Spider):
    name = "price"
    allowed_domains = ["bayut.com"]
    start_urls = ["https://www.bayut.com/to-rent/property/dubai/"]

    def __init__(self, *args, **kwargs):
        super(PriceSpider, self).__init__(*args, **kwargs)
        
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

            # Extract property information (Price, Type, and Location)
            properties = sel.css('div._475e888a._5d46b9fb')  # Update this selector based on your needs
            for property in properties:
                item = {
                    # Extracting Price
                    'price': property.css('div._2923a568 span.dc381b54::text').get().strip(),  # Price is in the span with class dc381b54

                    # Extracting Property Type (e.g., Villa, Apartment, etc.)
                    'type': property.css('span._19e94678.e0abc2de::text').get(),  # Property type like Villa, Apartment, etc.

                    # Extracting Location
                    'location': property.css('h3._4402bd70::text').get().strip(),  # Location is in the h3 tag with class _4402bd70
                }
                yield item

            # Find the next page URL from the href attribute (for pagination)
            next_page = sel.css('a._95dd93c1::attr(href)').get()  # Ensure correct selector for the next page button
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.driver.get(next_page_url)
                time.sleep(3)  # Wait for the page to load
            else:
                break  # Exit loop if there is no next page

        # Close the Selenium driver after finishing the pagination
        self.driver.quit()
