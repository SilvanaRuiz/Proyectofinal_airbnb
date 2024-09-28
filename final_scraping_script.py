
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
import logging
import signal
from tqdm import tqdm
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep

# Scraping function

def scraping_urls(city_url):
    # WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)

    # Airbnb Nottingham
    # url = 'https://www.airbnb.com/s/Nottingham--England--United-Kingdom/homes'
    browser.get(city_url)

    all_urls: list = []

    # Scraping para la pagina en la que está
    def scrape_urls():
        sleep(5) # espera a que carge
        listings = browser.find_elements(By.XPATH, '//a[contains(@href, "/rooms/")]')
        urls = [listing.get_attribute('href') for listing in listings]
        return urls

    # Loop para todas las paginas
    while True:
        page_urls = scrape_urls() # Esto funciona porque cada vez que vamos a una pagina nueva la url principal no cambia
        all_urls.extend(page_urls)

        # hacer click en el boton "next"
        try:
            next_button = browser.find_element(By.XPATH, '//a[@aria-label="Next"]')
            next_button.click()
            sleep(5)  # espera a que carge la pagina
        except NoSuchElementException:
            break

    all_urls = set(all_urls)
    all_urls = list(all_urls)
    return all_urls
url_san_francisco = "https://www.airbnb.com/s/San-Francisco--California--United-States/homes"
urls = scraping_urls(url_san_francisco)

print(urls)

def scraping_airbnb(urls):
    df = pd.DataFrame(columns=['guest_favorite', 'rating', 'number_reviews', 'type_host', 'hosting_time', 'price', 'all_reviews'])

    for url in urls:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-search-engine-choice-screen")
        # options.add_argument("--headless")
        options.add_argument('--lang=en')
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Inicializar variables antes del try
        guest_favorite = None
        rating = None
        number_reviews = None
        type_host = None
        hosting_time = None
        price = None
        all_reviews = []

        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='c1lbtiq8 atm_mk_stnw88 atm_9s_1txwivl atm_fq_1tcgj5g atm_wq_kb7nvz atm_tk_1tcgj5g dir dir-ltr']"))
            )
            element.click()
        except:
            pass

        try:
            # Extraer información como guest_favorite, rating, number_reviews, etc.
            data = driver.find_element(By.XPATH, "//a[contains(@href, 'reviews')]")
            sleep(2)

            if data:
                data_list = data.text.split(" ")
                
                # Intentar extraer el número de reviews
                try:
                    number_reviews = data_list[-2].split("\n")[-1]
                except:
                    number_reviews = None  # Si falla, deja en None
                
                all_reviews = []
                try:
                    if int(number_reviews) <= 6:
                        reviews_list = driver.find_elements(By.XPATH, "//div[@class='r1bctolv atm_c8_1sjzizj atm_g3_1dgusqm atm_26_lfmit2_13uojos atm_5j_1y44olf_13uojos atm_l8_1s2714j_13uojos dir dir-ltr']")
                        for review in reviews_list:
                            all_reviews.append(review.text)
                        all_reviews = set(all_reviews)
                        all_reviews = list(all_reviews)
                except:
                    all_reviews = []  # Si no hay reviews o ocurre un error, deja la lista vacía

                # Intentar extraer los datos de Guest Favorite y Rating
                if data_list[0] == "Guest\nfavorite\nRated":
                    guest_favorite = True
                    try:
                        rating = data_list[1]
                    except:
                        rating = None  # Si falla, deja en None
                    
                    try:
                        superhost_list = driver.find_elements(By.XPATH, "//li[@class='l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr']")
                        type_host = superhost_list[-2].text
                        if any(char.isdigit() for char in type_host):
                            type_host = np.nan
                        hosting_time = superhost_list[-1].text
                    except:
                        type_host = None
                        hosting_time = None

                    try:
                        price_primer = driver.find_element(By.XPATH, "//span[@class='a8jt5op atm_3f_idpfg4 atm_7h_hxbz6r atm_7i_ysn8ba atm_e2_t94yts atm_ks_zryt35 atm_l8_idpfg4 atm_vv_1q9ccgz atm_vy_t94yts aze35hn atm_mk_stnw88 atm_tk_idpfg4 dir dir-ltr']")
                        price = price_primer.get_attribute('textContent')
                        sleep(2)
                    except:
                        price = None  # Si falla, deja en None

                else:
                    guest_favorite = False
                    try:
                        rating = driver.find_element(By.XPATH, "//div[@class='r1lutz1s atm_c8_o7aogt atm_c8_l52nlx__oggzyc dir dir-ltr']")
                        #rating = driver.find_element(By.XPATH, "//div[@class='r1lutz1s atm_c8_o7aogt atm_c8_l52nlx__oggzyc dir dir-ltr']")
                        sleep(2)
                    except:
                        rating = None
                    
                    try:
                        superhost_list = driver.find_elements(By.XPATH, "//li[@class='l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr']")
                        type_host = superhost_list[-2].text
                        if any(char.isdigit() for char in type_host):
                            type_host = np.nan
                        hosting_time = superhost_list[-1].text
                    except:
                        type_host = None
                        hosting_time = None

                    try:
                        price_primer = driver.find_element(By.XPATH, "//span[@class='a8jt5op atm_3f_idpfg4 atm_7h_hxbz6r atm_7i_ysn8ba atm_e2_t94yts atm_ks_zryt35 atm_l8_idpfg4 atm_vv_1q9ccgz atm_vy_t94yts aze35hn atm_mk_stnw88 atm_tk_idpfg4 dir dir-ltr']")
                        price = price_primer.get_attribute('textContent')
                    except:
                        price = None

                # Crear un DataFrame temporal con la nueva fila
                new_row = pd.DataFrame({
                    'guest_favorite': [guest_favorite],
                    'rating': [rating],
                    'number_reviews': [number_reviews],
                    'type_host': [type_host],
                    'hosting_time': [hosting_time],
                    'price': [price],
                    'all_reviews': [', '.join(all_reviews)]  # Convertimos la lista en un string separado por comas
                })

                # Concatenar el nuevo DataFrame con el principal
                df = pd.concat([df, new_row], ignore_index=True)

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            driver.quit()

    # Guardar el DataFrame como CSV
    df.to_csv('airbnb_listings.csv', index=False)

    return df


df = scraping_airbnb(urls=urls)
df.head()