from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import csv
import os
import scraper


BASE_URL = "https://strefa-kostek.pl"
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GECKODRIVER_PATH = r"A:\studia\biznes\gecko\geckodriver.exe"

firefox_options = Options()
firefox_options.add_argument("--headless")

def initialize_driver():
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def main():
    Strefa_Kostek = scraper.Strefa_Kostek(BASE_URL)

    driver = initialize_driver()

    try:
        Strefa_Kostek.scrapuj_kategorie(driver)
        Strefa_Kostek.parsuj_liste_kategorii()   #lista kategorii
        for i in range(4,7):
            Strefa_Kostek.kategorie[i].scrapuj_podkategorie(driver)
            Strefa_Kostek.kategorie[i].parsuj_liste_podkategorii()    #listy podkategorii

            if Strefa_Kostek.kategorie[i].podkategorie[0].nazwa == "dummy":
                Strefa_Kostek.kategorie[i].podkategorie[0].scrapuj_produkty(driver,True)
                Strefa_Kostek.kategorie[i].JSON_Kateogria(True)
                Strefa_Kostek.kategorie[i].generuj_jpg(0,True)
            else:
                for j in range(len(Strefa_Kostek.kategorie[i].podkategorie)):

                    Strefa_Kostek.kategorie[i].podkategorie[j].scrapuj_produkty(driver,True)
                    Strefa_Kostek.kategorie[i].JSON_Podkateogria(j,True)
                    Strefa_Kostek.kategorie[i].generuj_jpg(j,True)
   
    finally:
        driver.quit()

if __name__ == "__main__":
    main()