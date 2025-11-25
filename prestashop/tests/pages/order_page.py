from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrderPage:
    """
    Page Object Model dla strony historii zamówień
    """
    
    # Locators
    ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href*='my-account']")
    ORDERS_LINK = (By.CSS_SELECTOR, "a[href*='order'], a[href*='history']")
    ORDER_ROW = (By.CSS_SELECTOR, "tr[class*='order'], .order-item")
    ORDER_STATUS = (By.CSS_SELECTOR, ".badge, .status, td.status")
    ORDER_NUMBER = (By.CSS_SELECTOR, "td:first-child, .order-number")
    ORDER_DETAIL_LINK = (By.CSS_SELECTOR, "a[href*='order-detail'], .order-link")
    
    # Invoice
    INVOICE_BUTTON = (By.CSS_SELECTOR, "a[href*='invoice'], button[name*='invoice']")
    INVOICE_LINK = (By.CSS_SELECTOR, "a[class*='invoice'], a[href*='invoice']")
    
    # Order detail page
    ORDER_DETAIL_SECTION = (By.CSS_SELECTOR, ".order-detail, [data-role='tabpanel']")
    INVOICE_SECTION = (By.CSS_SELECTOR, ".invoice-section, .invoices")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
    
    def navigate_to_my_account(self, base_url):
        """Przejdź na moje konto"""
        self.driver.get(f"{base_url}/index.php?controller=my-account")
    
    def navigate_to_orders(self, base_url):
        """Przejdź na historię zamówień"""
        self.driver.get(f"{base_url}/index.php?controller=order-history")
    
    def get_latest_order(self):
        """Pobierz ostatnie zamówienie z listy"""
        try:
            orders = self.wait.until(
                EC.presence_of_all_elements_located(self.ORDER_ROW)
            )
            if orders:
                return orders[0]
            return None
        except:
            return None
    
    def get_order_status(self, order_element=None):
        """Pobierz status zamówienia"""
        if not order_element:
            order_element = self.get_latest_order()
        
        if not order_element:
            return "Unknown"
        
        try:
            status = order_element.find_element(*self.ORDER_STATUS).text
            return status
        except:
            return "Unknown"
    
    def get_order_number(self, order_element=None):
        """Pobierz numer zamówienia"""
        if not order_element:
            order_element = self.get_latest_order()
        
        if not order_element:
            return "Unknown"
        
        try:
            order_num = order_element.find_element(*self.ORDER_NUMBER).text
            return order_num
        except:
            return "Unknown"
    
    def view_order_details(self, order_element=None):
        """Otwórz szczegóły zamówienia"""
        if not order_element:
            order_element = self.get_latest_order()
        
        if not order_element:
            raise Exception("Nie znaleziono zamówienia")
        
        try:
            detail_link = order_element.find_element(*self.ORDER_DETAIL_LINK)
            detail_link.click()
            self.wait.until(
                EC.presence_of_element_located(self.ORDER_DETAIL_SECTION)
            )
        except Exception as e:
            raise Exception(f"Nie udało się otworzyć szczegółów zamówienia: {str(e)}")
    
    def download_invoice(self):
        """Pobierz fakturę VAT"""
        try:
            invoice_btn = self.wait.until(
                EC.element_to_be_clickable(self.INVOICE_BUTTON)
            )
            invoice_btn.click()
            return True
        except:
            try:
                invoice_link = self.wait.until(
                    EC.element_to_be_clickable(self.INVOICE_LINK)
                )
                invoice_link.click()
                return True
            except:
                raise Exception("Nie znaleziono przycisku faktury")
    
    def has_invoice(self):
        """Sprawdź czy zamówienie ma fakturę"""
        try:
            self.driver.find_element(*self.INVOICE_SECTION)
            return True
        except:
            return False
