from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import csv
import os
import time

class FlightInfoScraper:
    def __init__(self, url, output_file='flight_data.csv'):
        self.url = url
        self.output_file = os.path.join(os.getcwd(), output_file)
        
        # Set up Firefox options
        firefox_options = Options()
        # firefox_options.add_argument("--headless")  
        
        # Set up Firefox driver
        self.driver = webdriver.Firefox(options=firefox_options)
        

    def scrape(self):
        try:
            self.driver.get(self.url)
            self.fill_form()
            results = self.extract_results()
            self.save_to_csv(results)
        finally:
            self.driver.quit()

    def fill_form(self):
        try:
            # Wait for the form to load
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]"))
            )
            
            if form:

                from_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Where from?']"))
                )
                from_input.clear()
                from_input.send_keys("Chhatrapati Shivaji Maharaj International Airport Mumbai")
                time.sleep(1)
                from_input.send_keys(Keys.ARROW_DOWN) 
                time.sleep(0.5)   
                from_input.send_keys(Keys.RETURN)

                print("From location entered")




                time.sleep(4)


                to_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Where to?']"))
                )
                to_input.clear()
                to_text = "Goa Dabolim International Airport"
                
                to_input.send_keys(to_text[:-1])
                time.sleep(1)

                new_to_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz[3]/div/div[2]/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/input"))
                )

                new_to_input.send_keys(to_text[-1])
                new_to_input.send_keys(Keys.RETURN)



                time.sleep(2)



                click_flight_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz[1]/div[1]/header/div[2]/div[2]/div[1]/div/nav/div[3]/div/button/div[3]"))
                )
                click_flight_button.click()



                time.sleep(2)


                click_from_date = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz[4]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input"))
                )
                click_from_date.click()
                time.sleep(5)
                click_to_date = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz[4]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/input"))
                )
                click_to_date.click()


                click_from_date_again = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz[4]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/input"))
                )
                click_from_date_again.click()
                







                calendar_cells = self.driver.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")
                price_data = []

                for cell in calendar_cells:
                    try:
                        date = cell.get_attribute('data-iso')
                        price_element = cell.find_element(By.CSS_SELECTOR, "div[data-gs]")
                        price_text = price_element.get_attribute('aria-label')
                        if price_text and ',' in price_text:
                            price = price_text.split(',')[1].strip()
                            price_data.append({
                                'date': date,
                                'price': price
                            })
                    except Exception as e:
                        continue




                print(price_data)
                time.sleep (40000)

                # calendar_cells = self.driver.find_elements(By.XPATH, "/html/body/c-wiz[4]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]")

                # # Create a list to store date-price pairs
                # price_data = []

                # for cell in calendar_cells:
                #     try:
                #         print(cell.get_attribute('outerHTML'))

                #         time.sleep(20000)
                #         # Get the date from data-iso attribute
                #         date = cell.get_attribute('data-iso')
                        
                #         # Get the price element - it's in a div with class 'CylAxb n3qw7 UNMzKf julK3b'
                #         price_element = cell.find_element(By.CSS_SELECTOR, "div[data-gs] div.julK3b")
                #         #price_element = cell.find_element(By.CSS_SELECTOR, "div.CylAxb.n3qw7.UNMzKf.julK3b")
                #         price_text = price_element.text  # This will give you something like "₹5,393"
                #         # print(price_text)
                #         # time.sleep(2)
                #         # Clean the price text (remove ₹ and commas)
                #         price = price_text.replace('₹','').replace(',','')
                        
                #         # Add to our data list
                #         price_data.append({
                #             'date': date,
                #             'price': price
                #         })
                #     except Exception as e:
                #         # Skip cells that don't have prices
                #         continue


                # print(price_data)

                # time.sleep(2000)
                # # to_input.send_keys(Keys.TAB)
                # to_input.send_keys(Keys.RETURN)
                # #to_input.click()
                # #to_input.submit()
                # # new_to_input.click()
                # #to_input.clear()
                
                # time.sleep(2000)
                # to_input.send_keys(Keys.ARROW_DOWN)
                # time.sleep(0.2)
                # to_input.send_keys(Keys.RETURN)

                # print("To location entered")
                # # to_input.click()
                # # to_input.send_keys(Keys.RETURN)
                # # to_input.send_keys(Keys.ENTER)
                # # # Enter the last character
                # # to_input.send_keys(to_text[-1])
                # # time.sleep(0.5)
                # # # Hit enter
                # # to_input.send_keys(Keys.ENTER)

                # # # to_input.send_keys("Goa Dabolim International Airport")
                # # # to_input.click()
                # # to_input.send_keys(Keys.RETURN)
                # # to_input.send_keys(Keys.ENTER)
                # time.sleep(500)

                
                # # Wait for the dropdown to appear
                # dropdown = WebDriverWait(self.driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, "//ul[@role='listbox']"))
                # )

                # # Find and click the first item in the dropdown
                # first_item = dropdown.find_element(By.XPATH, ".//li[1]")
                # first_item.click()
                # print("First dropdown item selected")
                # # # Fill in the form
                # # from_input = self.driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input")
                # # to_input = self.driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input")
                # # search_button = self.driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button/div[1]")
                
                # # from_input.send_keys("New York")  # Replace with your 'from' location
                # # to_input.send_keys("Los Angeles")  # Replace with your 'to' location
                # # search_button.click()
                
                # # Wait for results to load
                # WebDriverWait(self.driver, 10).until(
                #     EC.presence_of_element_located((By.CLASS_NAME, "flight-result"))
                # )
        except Exception as e:
            print(f"Exception occurred:  str(e)")

    # def extract_results(self):
    #     results = []
    #     flight_elements = self.driver.find_elements(By.CLASS_NAME, "flight-result")
        
    #     for element in flight_elements:
    #         result = {
    #             'Airline': element.find_element(By.CLASS_NAME, "airline").text,
    #             'Departure': element.find_element(By.CLASS_NAME, "departure").text,
    #             'Arrival': element.find_element(By.CLASS_NAME, "arrival").text,
    #             'Price': element.find_element(By.CLASS_NAME, "price").text,
    #             # Add more fields as needed
    #         }
    #         results.append(result)
    #         print(f"Extracted flight: {result}")
        
    #     return results

    # def save_to_csv(self, rows_data):
    #     if not rows_data:
    #         print("No data to save.")
    #         return
        
    #     keys = rows_data[0].keys()
    #     with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
    #         dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
    #         dict_writer.writeheader()
    #         dict_writer.writerows(rows_data)
    #     print(f"Data saved to {self.output_file} successfully.")

def main():
    url_to_scrape = 'https://www.google.com/travel/flights/search'  # Replace with the actual URL
    input_file = 'input_airport.csv'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current working directory: {current_dir}")
    # time.sleep(200)
    full_input_path = os.path.join(current_dir, input_file)
    print(f"Input file will be used as: {full_input_path}")

    scraper = FlightInfoScraper(url_to_scrape, full_input_path)
    scraper.scrape()

if __name__ == "__main__":
    main()


# import scrapy
# from scrapy.crawler import CrawlerProcess
# import time
# import csv
# import random
# import os

# class GenericSpider(scrapy.Spider):
#     name = 'generic_spider'
    
#     def __init__(self, urls=None, output_file='scraped_data.csv', max_pages=10, *args, **kwargs):
#         super(GenericSpider, self).__init__(*args, **kwargs)
#         self.start_urls = urls or []
#         self.output_file = output_file
#         self.max_pages = max_pages
#         self.page_number = 1

#     def save_to_csv(self, rows_data):
#         if not rows_data:
#             return
        
#         keys = rows_data[0].keys()
#         with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
#             dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
#             if csvfile.tell() == 0:
#                 dict_writer.writeheader()
#             dict_writer.writerows(rows_data)
#         print(f"Data appended to {self.output_file} successfully.")

#     def parse(self, response):
#         print(f"Parsing page {self.page_number}: {response.url}")

#         rows_data = []

#         # Extract data from the page
#         title = response.css('title::text').get()
#         print('=' * 120)
#         print(title)

#         items = response.css('div.item')  # Adjust this selector
#         for item in items:
#             row_data = {
#                 'Title': item.css('h2::text').get(default='N/A'),
#                 'URL': item.css('a::attr(href)').get(default='N/A'),
#                 'Description': item.css('p::text').get(default='N/A'),
#                 # Add more fields as needed
#             }
#             rows_data.append(row_data)
#             print('-' * 120)
#             print(f"Extracted item: {row_data}")
#             print('=' * 120)

#         self.save_to_csv(rows_data)

#         # Handle pagination
#         if self.page_number < self.max_pages:
#             time.sleep(500)
#             self.page_number += 1
#             next_page_url = f'{response.url.split("?")[0]}?page={self.page_number}'  # Adjust this pattern
            
#             # Add a random delay between requests
#             time.sleep(random.uniform(1, 3))
            
#             yield scrapy.Request(next_page_url, callback=self.parse)

# def main():

#     # Configure your spider
#     urls_to_scrape = ['https://www.google.com/travel/flights/search'] 
#     output_file = 'scraped_data.csv'
#     max_pages = 10

#     current_dir = os.getcwd()
#     full_output_path = os.path.join(current_dir, output_file)

#     # Create a CrawlerProcess instance
#     process = CrawlerProcess(settings={
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'ROBOTSTXT_OBEY': False,
#         'DOWNLOAD_DELAY': 2,
#     })

#     # Start the spider
#     process.crawl(GenericSpider, urls=urls_to_scrape, output_file=full_output_path, max_pages=max_pages)
#     process.start()

# if __name__ == "__main__":
#     main()