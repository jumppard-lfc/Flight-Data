from datetime import datetime  
from selenium import webdriver
from supabase import create_client
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pytz
import csv
import os
import time
import pandas as pd

class FlightInfoScraper:
    def __init__(self, route_list, supabase_db, now_timestamp, full_input_path):
        self.url = 'https://www.google.com/travel/flights/search'
        self.route_list = route_list
        self.supabase = supabase_db['supabase']
        self.supabase_table = supabase_db['supabase_table']
        self.now_timestamp = now_timestamp
        self.full_input_path = full_input_path

        # Set up Firefox options
        firefox_options = Options()
        # firefox_options.add_argument("--headless")  
        
        # Set up Firefox driver
        self.driver = webdriver.Firefox(options=firefox_options)


    def extract_price_and_currency(self, price_text):
        numeric_part = ''
        currency_part = ''
        
        for char in price_text:
            if char.isdigit():
                numeric_part += char
            elif char != ',':
                currency_part = price_text[len(numeric_part):].strip()
                break
        
        return int(numeric_part), currency_part
    

    def scrape(self):
        try:
            # Process one route at a time
            # Each route is a tuple: (source_country, source_airport, dest_country, dest_airport)
            for source_country, source_airport, dest_country, dest_airport in self.route_list:
                try:
                    print(f"\nScraping flights:")
                    print(f"From: {source_airport} ({source_country})")
                    print(f"To: {dest_airport} ({dest_country})")
                    
                    self.driver.get(self.url)
                    self.fill_form(source_country, source_airport, dest_country, dest_airport)
                    time.sleep(2)  # Wait between searches
                except Exception as e:
                    print(f"Error processing route: {str(e)}")
                    continue
        finally:
            self.driver.quit()


    def fill_form(self, source_country, source_airport, dest_country, dest_airport):
        try:
            # Wait for the form to load
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]"))
            )
            
            if form:
                # Fill source airport
                from_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Where from?']"))
                )
                from_input.clear()
                from_input.send_keys(source_airport)
                time.sleep(1)
                from_input.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)
                from_input.send_keys(Keys.RETURN)

                print("From location entered")

                time.sleep(4)

                # Fill destination airport
                to_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Where to?']"))
                )
                to_input.clear()
                to_text = dest_airport
                
                # Split input to handle Google Flights' autocomplete behavior
                to_input.send_keys(to_text[:-1])
                time.sleep(1)

                new_to_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz[3]/div/div[2]/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/input"))
                )

                new_to_input.send_keys(to_text[-1])
                new_to_input.send_keys(Keys.RETURN)

                time.sleep(2)

                # Click flight button
                click_flight_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz[1]/div[1]/header/div[2]/div[2]/div[1]/div/nav/div[3]/div/button/div[3]"))
                )
                click_flight_button.click()
                time.sleep(2)

                # Click calendar dates
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

                # Collect price data
                calendar_cells = self.driver.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")
                #print(f"Found {len(calendar_cells)} calendar cells")

                price_data = []

                if len(calendar_cells) == 0:
                    print(f"\nNo calendar data found for route: {source_airport} → {dest_airport}")
                    time.sleep(4000)
                    return False
                

                for cell in calendar_cells:
                    try:
                        date = cell.get_attribute('data-iso')
                        date_obj = datetime.strptime(date, '%Y-%m-%d').date()

                        price_element = cell.find_element(By.CSS_SELECTOR, "div[data-gs]")
                        price_text = price_element.get_attribute('aria-label')
                        if price_text and ',' in price_text:
                            price = price_text.split(',')[1].strip()
                            price_value, currency = self.extract_price_and_currency(price)
                            price_data.append({
                                'scrape_timestamp': self.now_timestamp.isoformat(), 
                                'date': date_obj.isoformat(),
                                'price': price_value,
                                'currency': currency,
                                'source_country': source_country,
                                'source_airport': source_airport,
                                'destination_country': dest_country,
                                'destination_airport': dest_airport
                            })
                            #print(price_data)
                    except Exception:
                        continue
                
                is_inserted = False        
                # Bulk insert after collecting all data
                if price_data:
                    try:
                        self.supabase.table(self.supabase_table).insert(price_data).execute()
                        print(f"Successfully inserted {len(price_data)} records to database")
                        is_inserted = True
                    except Exception as e:
                        time.sleep(5)
                        print("-" * 40)
                        print(f"Bulk insert failed: {str(e)}")
                        print("-" * 40)
                        is_inserted = False

                print(f"Collected {len(price_data)} prices")

                if is_inserted:
                    # Update CSV 
                    df = pd.read_csv(self.full_input_path, dtype={'Scraping Date': str})
                    mask = (df['Source Airport'] == source_airport) & \
                        (df['Destination Airport'] == dest_airport)
                    df.loc[mask, 'Scraping Date'] = datetime.now().date().strftime('%Y-%m-%d')
                    df.to_csv(self.full_input_path, index=False)
                    print(f"CSV updated for route: {source_airport} → {dest_airport}")

                return price_data

        except Exception as e:
            print(f"Exception in fill_form: {str(e)}")
            raise



def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = 'input_airport.csv'
    full_input_path = os.path.join(current_dir, input_file)

    ist_timezone = pytz.timezone('Asia/Kolkata')
    now_timestamp = datetime.now(ist_timezone)
    today_date = now_timestamp.date()

    supabase_url = ""
    supabase_key = ""
    supabase = create_client(supabase_url, supabase_key)
    supabase_table = "google_flights_scrap"

    supabase_db = {
        'supabase' : supabase,
        'supabase_table' : supabase_table
    }
    
    try:
        # Read the CSV file
        df = pd.read_csv(full_input_path)
        
        # Convert the dataframe rows to a list of tuples
        route_list = []
        for index, row in df.iterrows():
            # Check if Scraping Date is empty or not today's date
            scraping_date = row.get('Scraping Date', '')
            
            if pd.isna(scraping_date) or str(scraping_date).strip() == '':
                # If scraping date is empty, add to route list
                route = (
                    row['Source Country'],
                    row['Source Airport'],
                    row['Destination Country'],
                    row['Destination Airport']
                )
                route_list.append(route)
            else:
                # Convert scraping date string to date object
                try:
                    scrape_date = datetime.strptime(str(scraping_date), '%Y-%m-%d').date()
                    if scrape_date != today_date:
                        route = (
                            row['Source Country'],
                            row['Source Airport'],
                            row['Destination Country'],
                            row['Destination Airport']
                        )
                        route_list.append(route)
                except ValueError as e:
                    print(f"Warning: Invalid date format in row {index + 1}: {scraping_date}")
                    continue
            
        if not route_list:
            print("\nNo routes to process - all routes have been scraped today.")
            return
            
        # Print routes to be processed
        print("\nRoutes to be processed:")
        for i, (src_country, src_airport, dst_country, dst_airport) in enumerate(route_list, 1):
            print(f"\nRoute {i}:")
            print(f"From: {src_airport} ({src_country})")
            print(f"To: {dst_airport} ({dst_country})")
        
        # Initialize scraper with route list
        scraper = FlightInfoScraper(route_list, supabase_db, now_timestamp, full_input_path)
        scraper.scrape()
        
        
    except Exception as e:
        print(f"Main execution error: {str(e)}")

if __name__ == "__main__":
    main()