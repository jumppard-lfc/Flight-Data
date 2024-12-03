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
    def __init__(self, airports_to_scrape):
        
        print(airports_to_scrape)
        time.sleep(1000)
        self.airports_to_scrape = airports_to_scrape
        
        # Set up Firefox options
        firefox_options = Options()
        # firefox_options.add_argument("--headless")  
        
        # Set up Firefox driver
        self.driver = webdriver.Firefox(options=firefox_options)
        

    def scrape(self):
        try:
            self.driver.get(self.url)
            self.fill_form()
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

        except Exception as e:
            print(f"Exception occurred:  str(e)")



def main():
    
    url_to_scrape = 'https://www.google.com/travel/flights/search'  # Replace with the actual URL
    input_file = 'input_airport.csv'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current working directory: {current_dir}")
    # time.sleep(200)
    full_input_path = os.path.join(current_dir, input_file)
    print(f"Input file will be used as: {full_input_path}")

    airports_to_scrape = "Hi"

    scraper = FlightInfoScraper(airports_to_scrape)
    scraper.scrape()

if __name__ == "__main__":
    main()
