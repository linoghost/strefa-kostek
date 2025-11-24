from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """
    Page Object Model dla strony koszyka PrestaShopa
    """
    
    # Locators
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon, .shopping-cart")
    CART_PRODUCTS = (By.CSS_SELECTOR, "tr[id*='product']")
    PRODUCT_ROWS = (By.CSS_SELECTOR, ".product-line-box, .cart_item")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-name, .product_name")
    PRODUCT_QUANTITY = (By.CSS_SELECTOR, "input[name*='qty'], input[name*='quantity']")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-price, .price")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".standard-checkout, a[href*='checkout'], a[href*='order']")
    CART_TOTAL = (By.CSS_SELECTOR, ".total-price, .cart-total")
    REMOVE_PRODUCT = (By.CSS_SELECTOR, "a[data-id-product], .remove-btn")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
    
    def navigate_to_cart(self, base_url):
        """Przejdź na stronę koszyka"""
        self.driver.get(f"{base_url}/index.php?controller=cart")
    
    def click_cart_icon(self):
        """Kliknij ikonę koszyka"""
        cart_icon = self.wait.until(
            EC.element_to_be_clickable(self.CART_ICON)
        )
        cart_icon.click()
    
    def get_cart_products(self):
        """Pobierz liczbę produktów w koszyku"""
        try:
            products = self.driver.find_elements(*self.PRODUCT_ROWS)
            return products
        except:
            return []
    
    def get_products_count(self):
        """Pobierz liczbę pozycji w koszyku"""
        products = self.get_cart_products()
        return len(products)
    
    def get_product_details(self, product_index):
        """Pobierz szczegóły produktu z koszyka"""
        products = self.get_cart_products()
        if product_index >= len(products):
            raise Exception(f"Produkt z indeksem {product_index} nie istnieje w koszyku")
        
        product = products[product_index]
        
        try:
            name = product.find_element(*self.PRODUCT_NAME).text
        except:
            name = "Unknown"
        
        try:
            quantity_input = product.find_element(*self.PRODUCT_QUANTITY)
            quantity = int(quantity_input.get_attribute("value"))
        except:
            quantity = 0
        
        try:
            price = product.find_element(*self.PRODUCT_PRICE).text
        except:
            price = "N/A"
        
        return {
            "name": name,
            "quantity": quantity,
            "price": price
        }
    
    def get_all_products_details(self):
        """Pobierz szczegóły wszystkich produktów w koszyku"""
        products = self.get_cart_products()
        details = []
        for i in range(len(products)):
            details.append(self.get_product_details(i))
        return details
    
    def verify_product_in_cart(self, product_name):
        """Sprawdź czy produkt jest w koszyku"""
        products = self.get_all_products_details()
        for product in products:
            if product_name.lower() in product["name"].lower():
                return True
        return False
    
    def get_cart_total(self):
        """Pobierz sumę koszyka"""
        try:
            total = self.driver.find_element(*self.CART_TOTAL).text
            return total
        except:
            return "N/A"
    
    def remove_product_from_cart(self, product_index):
        """Usuń produkt z koszyka"""
        products = self.get_cart_products()
        if product_index >= len(products):
            raise Exception(f"Produkt z indeksem {product_index} nie istnieje w koszyku")
        
        product = products[product_index]
        try:
            remove_btn = product.find_element(By.CSS_SELECTOR, "a[data-id-product], .remove, .delete")
            remove_btn.click()
            self.wait.until(EC.staleness_of(product))
        except Exception as e:
            raise Exception(f"Nie udało się usunąć produktu: {str(e)}")
    
    def proceed_to_checkout(self):
        """Przejdź do kasy"""
        try:
            checkout_btn = self.wait.until(
                EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
            )
            checkout_btn.click()
        except Exception as e:
            raise Exception(f"Nie znaleziono przycisku checkout: {str(e)}")
