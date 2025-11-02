from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import json
import os
from PIL import Image
from io import BytesIO
import time
import re
import requests

BASE_URL = "https://strefa-kostek.pl"

class Produkt:
    def __init__(self, nazwa, cena, zdjecie, link, driver, czy2zdjecia):
        self.nazwa = nazwa
        self.cena = cena
        self.opis = ''
        self.zdjecie = zdjecie
        self.zdjecie2 = ''
        self.zdjecie3 = ''
        self.link = link
        self.driver = driver
        self.pobierz_szczegolowe_dane(czy2zdjecia)

    def fetch(self):
        self.driver.get(self.link) #html
        return self.driver.page_source


    def pobierz_szczegolowe_dane(self,czy2zdjecia):
        page_source = self.fetch()
        soup = BeautifulSoup(page_source, "html.parser") #analiza html

        if not czy2zdjecia:
            img_tag = (soup.find('img', id='bigpic'))

            if img_tag:
                img_src = img_tag.get('src')
                if img_src:
                    self.zdjecie2 = img_src
        else:
            gallery = soup.find('ul', id='thumbs_list_frame')

            if gallery:
                li_items = gallery.find_all('li')
                for i, li in enumerate(li_items):
                    if i >= 2: #wezmy 2 nie badzmy greedy
                        break
                    a_tag = li.find('a')
                    if a_tag:
                        big_image = a_tag.get('href')  
                        if i == 0:
                            self.zdjecie2 = big_image
                        elif i == 1:
                            self.zdjecie3 = big_image
            else:
                # jak nie ma galerii to big pic
                img_tag = soup.find('img', id='bigpic')
                if img_tag:
                    img_src = img_tag.get('src')
                    if img_src:
                        self.zdjecie2 = img_src



        text = ''

        # try to find pelny opis
        meta_desc = soup.find('meta', itemprop='description')
        if meta_desc and meta_desc.get('content'):
            text = meta_desc.get('content').strip()

        # jak nie ma to short
        elif soup.find('div', id='short_description_content'):
            description_div = soup.find('div', id='short_description_content')
            paragraphs = [p.text.strip() for p in description_div.find_all('p')]
            text = '\n'.join(paragraphs)

        self.opis = text

    def __call__(self, *args, **kwargs): #wyświetlanie produktu essentially, ale to taki hattrick żeby moc zrobic produkt()
        print(self.nazwa + ' ' + self.opis + ' ' + self.cena + ' ' + self.zdjecie + ' ' + self.zdjecie2)

class Podkategoria:
    def __init__(self, nazwa, link):
        self.nazwa = nazwa
        if '/' in nazwa or '+' in nazwa:
            print("znaleziono niedozwolony znak w nazwie. zmiana.")
            self.nazwa=nazwa.replace('/','_')

        self.link = link
        self.produkty: List[Produkt] = []

    def fetch(self,driver):
        driver.get(self.link)
        return driver.page_source


    def scrolluj_strone(self, driver, pauza=2, max_scroll=30): #trzeba przeskrolować stronke bo js ładuje produkty, a nie ma kolejnych stron

        last_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(max_scroll): #raczej watpie ze wiecej niz 20 razy trzeba będzie scrollować a nawet jeśli to trudnoxdd
            # przewiń do końca strony
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # poczekaj, aż nowe produkty się załadują
            time.sleep(pauza)

            # sprawdź nową wysokość strony
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("scrolled.")
                break
            last_height = new_height


    def scrapuj_produkty(self,driver,czy2zdjecia):
        print(f"jedziemy z {self.nazwa}")
        driver.get(self.link) #wiem ze jest wyzej ale idk czy to sie jakos zapisuje or something wiec just to be safe
        self.scrolluj_strone(driver)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    

        product_divs = soup.find_all('li', class_='ajax_block_product')
        if not product_divs:
            print("nie ma produktow, cos jest nie tak. nazwa: {self.nazwa}")
            return

        for product in product_divs:

            nazwa_tag = product.find('span', class_='product-name')
            nazwa = nazwa_tag.text.strip() if nazwa_tag else 'Brak nazwy'
            #print(nazwa)
          
            cena_tag = product.find('span', class_='price', itemprop='price')
            cena = cena_tag.text.strip() if cena_tag else 'Brak ceny'

            
            link_tag = product.find('a', class_='product_img_link')
            produkt_link = link_tag['href'] if link_tag and link_tag.has_attr('href') else 'Brak linku'

            
            img_tag = product.find('img', class_='replace-2x')
            src = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

            
            self.produkty.append(
                Produkt(
                    nazwa,
                    cena,
                    str(src) if src else 'Brak zdjęcia',
                    produkt_link,
                    driver,
                    czy2zdjecia
                )
            )

        print(f"mamy {len(self.produkty)} produktów w podkategorii {self.nazwa}.")

    def scrapuj_czesc_produktow(self,driver,czy2zdjecia):
        print("jedziemy z {self.nazwa}")
        driver.get(self.link) #wiem ze jest wyzej ale idk czy to sie jakos zapisuje or something wiec just to be safe
        self.scrolluj_strone(driver)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    

        product_divs = soup.find_all('li', class_='ajax_block_product')
        if not product_divs:
            print("nie ma produktow, cos jest nie tak. nazwa: {self.nazwa}")
            return

        for i, product in enumerate(product_divs):
            if i>=10:
                break

            nazwa_tag = product.find('span', class_='product-name')
            nazwa = nazwa_tag.text.strip() if nazwa_tag else 'Brak nazwy'

          
            cena_tag = product.find('span', class_='price', itemprop='price')
            cena = cena_tag.text.strip() if cena_tag else 'Brak ceny'

            
            link_tag = product.find('a', class_='product_img_link')
            produkt_link = link_tag['href'] if link_tag and link_tag.has_attr('href') else 'Brak linku'

            
            img_tag = product.find('img', class_='replace-2x')
            src = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

            
            self.produkty.append(
                Produkt(
                    nazwa,
                    cena,
                    str(src) if src else 'Brak zdjęcia',
                    produkt_link,
                    driver,
                    czy2zdjecia
                )
            )

        print(f"mamy {len(self.produkty)} produktów w podkategorii {self.nazwa}.")


    def __call__(self, *args, **kwargs):
        print(self.nazwa)
        for k in self.produkty:
           k()

class Kategoria:
    def __init__(self,nazwa, link):
        self.nazwa = nazwa
        self.link = link
        self.podkategorie: List[Podkategoria] = []
    
    def wyswietl_podkategorie(self):
        if len(self.podkategorie)!=0:
                
            for podkategoria in self.podkategorie:
                print(podkategoria.nazwa)
        else:
            print("cos nie pyklo")    


    def fetch(self,driver):
        driver.get(self.link)
        return driver.page_source

    def scrapuj_podkategorie(self, driver):
        page_source = self.fetch(driver)
        soup = BeautifulSoup(page_source, "html.parser")
        print(f"jestem w {self.nazwa}")

        # Znajdź wszystkie główne kategorie
        main_categories = soup.find_all('li', class_='level-1 parent')
        for main_cat in main_categories:
            print("MEOOOOOOOOOOOOOOOOOOW")
            link_a = main_cat.find('a')
            main_cat_name = link_a.find('span').text.strip()

            # Jeśli ta główna kategoria pasuje do naszej instancji
            if main_cat_name == self.nazwa:
                # Szukamy tylko podkategorii w tej kategorii
                sub_ul = main_cat.find('ul', class_='menu-dropdown')
                if sub_ul:
                    sub_li_elements = sub_ul.find_all('li')
                    for sub_li in sub_li_elements:
                        sub_a = sub_li.find('a')
                        sub_name = sub_a.find('span').text.strip()
                        sub_href = sub_a['href']
                        self.podkategorie.append(Podkategoria(sub_name, sub_href))
                break  # nie trzeba szukać dalej
        
        print(f"Znaleziono {len(self.podkategorie)} podkategorii.")

        if len(self.podkategorie)==0:
            self.podkategorie.append(Podkategoria("dummy", self.link))

        


    def __call__(self):
        for k in self.podkategorie:
            print(k.nazwa + 'link: ' + str(k.link))


    def parsuj_liste_podkategorii(self):
        nazwa_pliku = self.nazwa + '_' +'podkategorie.json'
        try:
            nazwy = [pkat.nazwa for pkat in self.podkategorie]

            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(nazwy, plik, ensure_ascii=False, indent=4)

        except Exception as e:
            print("Blad zapisu")


    def JSON_Podkateogria(self, numer_podkategorii,czy2zdjecia):
        nazwa_pliku = self.nazwa + '-' + self.podkategorie[numer_podkategorii].nazwa + '.json'
        if not czy2zdjecia:
            pola = ["nazwa", "cena", "opis", "zdjecie", "zdjecie2" ]
            try:
                dane = [{pole: getattr(produkt, pole, None) for pole in pola} for produkt in self.podkategorie[numer_podkategorii].produkty]

                with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                    json.dump(dane, plik, ensure_ascii=False, indent=4)

            except Exception as e:
                print("Blad zapisu")
        else:
            pola = ["nazwa", "cena", "opis", "zdjecie", "zdjecie2", "zdjecie3"]
            try:
                dane = [{pole: getattr(produkt, pole, None) for pole in pola} for produkt in
                        self.podkategorie[numer_podkategorii].produkty]

                with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                    json.dump(dane, plik, ensure_ascii=False, indent=4)

            except Exception as e:
                print("Blad zapisu")

    def JSON_Kateogria(self, czy2zdjecia):
        nazwa_pliku = self.nazwa + '.json'
        if not czy2zdjecia:
            pola = ["nazwa", "cena", "opis", "zdjecie", "zdjecie2" ]
            try:
                dane = [{pole: getattr(produkt, pole, None) for pole in pola} for produkt in self.podkategorie[0].produkty]

                with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                    json.dump(dane, plik, ensure_ascii=False, indent=4)

            except Exception as e:
                print("Blad zapisu")
        else:
            pola = ["nazwa", "cena", "opis", "zdjecie", "zdjecie2", "zdjecie3"]
            try:
                dane = [{pole: getattr(produkt, pole, None) for pole in pola} for produkt in
                        self.podkategorie[0].produkty]

                with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                    json.dump(dane, plik, ensure_ascii=False, indent=4)

            except Exception as e:
                print("Blad zapisu")

    def generuj_jpg(self, nr_podkategorii,czy2zdjecia):
        if self.podkategorie[0].nazwa=="dummy":
            folder = self.nazwa+ '-images'
            json_file = self.nazwa + '.json'
        else:
            folder = self.nazwa+ '_' + self.podkategorie[nr_podkategorii].nazwa + '-images'
            json_file = self.nazwa + '-' + self.podkategorie[nr_podkategorii].nazwa + '.json'
        os.makedirs(folder, exist_ok=True)
        with open(json_file,'r',encoding='utf-8') as f:
            data = json.load(f)
        if czy2zdjecia:
            for i, pr in enumerate(data):
                try:
                    link1 = pr.get('zdjecie')
                    link2 = pr.get('zdjecie2')

                    if link1:
                        rs = requests.get(link1)
                        rs.raise_for_status()
                        img = Image.open(BytesIO(rs.content))
                        img_jpg_path1 = os.path.join(folder, f"image_{i}_1.jpg")
                        img.convert("RGB").save(img_jpg_path1, "JPEG")
                        pr['zdjecie_jpg'] =  img_jpg_path1

                    if link2:
                        rs = requests.get(link2)
                        rs.raise_for_status()
                        img = Image.open(BytesIO(rs.content))
                        img_jpg_path2 = os.path.join(folder, f"image_{i}_2.jpg")
                        img.convert("RGB").save(img_jpg_path2, "JPEG")
                        pr['zdjecie2_jpg'] = img_jpg_path2

                    if pr.get('zdjecie3') != "":
                        link3 = pr.get('zdjecie3')
                        rs = requests.get(link3)
                        rs.raise_for_status()
                        img = Image.open(BytesIO(rs.content))
                        img_jpg_path3 = os.path.join(folder, f"image_{i}_3.jpg")
                        img.convert("RGB").save(img_jpg_path3, "JPEG")
                        pr['zdjecie3_jpg'] = img_jpg_path3

                except Exception as e:
                    print('blad przy konwersji zdjec (czy2)')
        else:
            for i, pr in enumerate(data):
                try:
                    link1 = pr.get('zdjecie')
                    link2 = pr.get('zdjecie2')

                    if link1:
                        rs = requests.get(link1)
                        rs.raise_for_status()
                        img = Image.open(BytesIO(rs.content))
                        img_jpg_path1 = os.path.join(folder, f"image_{i}_1.jpg")
                        img.convert("RGB").save(img_jpg_path1, "JPEG")
                        pr['zdjecie_jpg'] = img_jpg_path1

                    if link2:
                        rs = requests.get(link2)
                        rs.raise_for_status()
                        img = Image.open(BytesIO(rs.content))
                        img_jpg_path2 = os.path.join(folder, f"image_{i}_2.jpg")
                        img.convert("RGB").save(img_jpg_path2, "JPEG")
                        pr['zdjecie2_jpg'] = img_jpg_path2
                except Exception as e:
                    print('blad przy konwersji zdjec')

        with open(json_file,'w', encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False, indent=4)

class Strefa_Kostek:
    def __init__(self, link):
        self.link = link
        self.kategorie: List[Kategoria] = []

    def __call__(self):
        for k in self.kategorie:
            print(k.nazwa + 'link: ' + str(k.link))

    def fetch_page_source(self, driver):
        driver.get(BASE_URL)
        return driver.page_source

    def scrapuj_kategorie(self, driver):
        page_source = self.fetch_page_source(driver)
        soup = BeautifulSoup(page_source, "html.parser")

        menu = soup.find('div', class_='labvega-menu-active')
        if not menu:
            print("MAMMA MIA NIE MA KATEGORII")
            return

        level1_li = menu.find_all('li', class_='level-1')

        for li in level1_li:
            link_tag = li.find('a')
            if link_tag:
                href = link_tag['href']
                name = link_tag.find('span').text.strip() if link_tag.find('span') else link_tag.text.strip()
                self.kategorie.append(Kategoria(name, href))

        print(f"Znaleziono {len(self.kategorie)} kategorii.")


    def parsuj_liste_kategorii(self):
        nazwa_pliku = 'kategorie.json'
        try:

            nazwy = [kat.nazwa for kat in self.kategorie]

            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(nazwy, plik, ensure_ascii=False, indent=4)

        except Exception as e:
            print("Blad zapisu")
