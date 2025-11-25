from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class HomePage:
    """
    Page Object Model dla strony głównej PrestaShopa
    """
    
    # Locators
    CATEGORIES_MENU = (By.CSS_SELECTOR, "ul.top-menu li")
    SEARCH_INPUT = (By.ID, "search_query_top")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[name='submit_search']")
    PRODUCT_ITEM = (By.CSS_SELECTOR, ".product-container")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".product-add-to-cart button")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)
    
    def navigate(self, base_url):
        """Przejdź na stronę główną"""
        self.driver.get(base_url)
        time.sleep(2)
    
    #def get_categories(self):
        """Pobierz listę dostępnych kategorii"""
        #categories = self.wait.until(
         #   EC.presence_of_all_elements_located(self.CATEGORIES_MENU)
        #)
        #return categories
    def get_categories(self):
        """
        Pobiera listę kategorii z menu — w tym PODKATEGORIE z popovera PrestaShop.
        """
        # 1. Znajdź główną kategorię (PRODUKTY)
        main_category = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#top-menu > li"))
        )

        # 2. Najechanie myszką aby otworzyć menu
        self.actions.move_to_element(main_category).perform()

        # 3. Czekanie aż rozwinie się popover
        popover_selector = (By.CSS_SELECTOR, "#top-menu .popover ul li a")
        self.wait.until(EC.visibility_of_element_located(popover_selector))

        # 4. Pobranie podkategorii z rozwiniętego menu
        subcategories = self.driver.find_elements(*popover_selector)

        # Jeżeli nie ma podkategorii → zwróć tylko główną
        if not subcategories:
            return [main_category]

        return subcategories

    
    def click_category(self, category_name):
        """Kliknij na wybraną kategorię"""
        categories = self.get_categories()
        for category in categories:
            if category_name.lower() in category.text.lower():
                self.actions.move_to_element(category).perform()
                time.sleep(0.5)
                category.click()
                time.sleep(2)
                return
        raise Exception(f"Kategoria '{category_name}' nie znaleziona")
    
    def search_product(self, product_name):
        """Szukaj produktu"""
        search_input = self.wait.until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(product_name)
        search_button = self.driver.find_element(*self.SEARCH_BUTTON)
        search_button.click()
        time.sleep(2)
    
    def get_products(self):
        """Pobierz listę produktów na stronie"""
        return self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_ITEM)
        )
    
    def get_product_name(self, product_element):
        """Pobierz nazwę produktu z elementu"""
        try:
            name = product_element.find_element(By.CSS_SELECTOR, ".product-name, h5 a").text
            return name
        except:
            return "Unknown"
    
    def add_product_to_cart(self, product_index, quantity=1):
        """
        Dodaj produkt do koszyka
        product_index: indeks produktu z listy (0-based)
        quantity: ilość
        """
        products = self.get_products()
        if product_index >= len(products):
            raise Exception(f"Produkt z indeksem {product_index} nie istnieje")
        
        product = products[product_index]
        product_name = self.get_product_name(product)
        
        # Hover na produkcie żeby pokazać przycisk Add to Cart
        self.actions.move_to_element(product).perform()
        time.sleep(0.5)
        
        # Szukaj przycisku Add to Cart w produkcie
        try:
            add_btn = product.find_element(By.CSS_SELECTOR, ".add-to-cart, .add_to_cart")
            self.actions.move_to_element(add_btn).perform()
            time.sleep(0.3)
            add_btn.click()
        except:
            # Alternatywne szukanie
            add_btn = product.find_element(By.CSS_SELECTOR, "a[data-id-product]")
            add_btn.click()
        
        # Zmodyfikuj ilość jeśli > 1
        if quantity > 1:
            self._set_product_quantity(quantity)
        
        time.sleep(1)
        return product_name
    
    def _set_product_quantity(self, quantity):
        """Ustaw ilość produktu w quickview/modal"""
        try:
            qty_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='qty']")
            qty_input.clear()
            qty_input.send_keys(str(quantity))
        except:
            pass
