from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class CheckoutPage:
    """
    Page Object Model dla procesu checkout
    """
    
    # Locators
    ADDRESS_STEP = (By.CSS_SELECTOR, "[data-step='addresses'], .addresses")
    SHIPPING_STEP = (By.CSS_SELECTOR, "[data-step='shipping'], .shipping")
    PAYMENT_STEP = (By.CSS_SELECTOR, "[data-step='payment'], .payment")
    
    # Address form
    ADDRESS_INPUT = (By.CSS_SELECTOR, "input[name='address1']")
    CITY_INPUT = (By.CSS_SELECTOR, "input[name='city']")
    POSTCODE_INPUT = (By.CSS_SELECTOR, "input[name='postcode']")
    COUNTRY_SELECT = (By.CSS_SELECTOR, "select[name='id_country']")
    
    # Shipping (Carrier)
    CARRIER_OPTION = (By.CSS_SELECTOR, "input[name='id_carrier']")
    CARRIER_SELECT = (By.CSS_SELECTOR, ".carrier-item")
    
    # Payment
    PAYMENT_METHOD = (By.CSS_SELECTOR, "input[name='payment-option']")
    COD_PAYMENT = (By.CSS_SELECTOR, "input[value*='cod'], input[id*='cash']")
    BANK_PAYMENT = (By.CSS_SELECTOR, "input[value*='bank'], input[id*='wire']")
    
    # Confirm
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "button[id*='confirm'], button[name*='confirm'], button:contains('Confirm')")
    NEXT_STEP_BUTTON = (By.CSS_SELECTOR, "button[name*='continue'], button:contains('Continue')")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button[id*='payment-confirmation'], button:contains('Place order')")
    
    # Messages
    ORDER_SUCCESS = (By.CSS_SELECTOR, ".alert-success, .success-message")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.actions = ActionChains(self.driver)
    
    def fill_address(self, address="123 Test Street", city="TestCity", postcode="12345"):
        """Wypełnij formularz adresu"""
        try:
            addr_input = self.wait.until(EC.presence_of_element_located(self.ADDRESS_INPUT))
            addr_input.clear()
            addr_input.send_keys(address)
        except:
            pass
        
        try:
            city_input = self.driver.find_element(*self.CITY_INPUT)
            city_input.clear()
            city_input.send_keys(city)
        except:
            pass
        
        try:
            postcode_input = self.driver.find_element(*self.POSTCODE_INPUT)
            postcode_input.clear()
            postcode_input.send_keys(postcode)
        except:
            pass
        
        self.proceed_to_next_step()
    
    def select_carrier(self, carrier_index=0):
        """Wybierz przewoźnika"""
        carriers = self.wait.until(
            EC.presence_of_all_elements_located(self.CARRIER_SELECT)
        )
        
        if carrier_index >= len(carriers):
            carrier_index = 0
        
        carrier = carriers[carrier_index]
        self.actions.move_to_element(carrier).perform()
        carrier.click()
        
        return carrier.text
    
    def select_payment_method(self, method="cod"):
        """Wybierz metodę płatności: 'cod' (przy odbiorze) lub 'bank' (przelew)"""
        if method.lower() == "cod":
            try:
                cod_radio = self.wait.until(EC.element_to_be_clickable(self.COD_PAYMENT))
                cod_radio.click()
                return "Payment on delivery"
            except:
                # Alternatywne szukanie
                payments = self.driver.find_elements(*self.PAYMENT_METHOD)
                if payments:
                    payments[0].click()
                    return "First payment method"
        elif method.lower() == "bank":
            try:
                bank_radio = self.wait.until(EC.element_to_be_clickable(self.BANK_PAYMENT))
                bank_radio.click()
                return "Bank transfer"
            except:
                payments = self.driver.find_elements(*self.PAYMENT_METHOD)
                if len(payments) > 1:
                    payments[1].click()
                    return "Second payment method"
        
        raise Exception(f"Nie znaleziono metody płatności: {method}")
    
    def proceed_to_next_step(self):
        """Przejdź do następnego kroku"""
        try:
            next_btn = self.wait.until(
                EC.element_to_be_clickable(self.NEXT_STEP_BUTTON)
            )
            next_btn.click()
        except:
            pass
    
    def confirm_order(self):
        """Potwierdź zamówienie"""
        try:
            confirm_btn = self.wait.until(
                EC.element_to_be_clickable(self.PLACE_ORDER_BUTTON)
            )
            confirm_btn.click()
            
            # Czekaj na potwierdzenie
            self.wait.until(
                EC.presence_of_element_located(self.ORDER_SUCCESS)
            )
            return True
        except Exception as e:
            raise Exception(f"Nie udało się potwierdzić zamówienia: {str(e)}")
    
    def get_order_confirmation_message(self):
        """Pobierz wiadomość potwierdzenia zamówienia"""
        try:
            msg = self.driver.find_element(*self.ORDER_SUCCESS).text
            return msg
        except:
            return "Unknown"
