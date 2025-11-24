from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import string


class AuthPage:
    """
    Page Object Model dla rejestracji i logowania
    """
    
    # Locators
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login'], a[href*='authentication']")
    SIGN_UP_BUTTON = (By.CSS_SELECTOR, "button[name='create-account'], a[href*='registration']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email'], input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password_confirm'], input[id*='confirm']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[name='firstname'], input[id*='firstname']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[name='lastname'], input[id*='lastname']")
    AGREE_TERMS = (By.CSS_SELECTOR, "input[name='customer_privacy'], input[id*='terms']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'][name*='save'], button[type='submit'][name*='register'], button:contains('Register')")
    ACCOUNT_BUTTON = (By.CSS_SELECTOR, "a[href*='my-account'], .account, a.account-link")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.actions = ActionChains(self.driver)
    
    def go_to_login(self, base_url):
        """Przejdź na stronę logowania"""
        self.driver.get(f"{base_url}/index.php?controller=authentication")
    
    def register_new_account(self, email=None, password=None, first_name=None, last_name=None):
        """Zarejestruj nowe konto"""
        
        # Generuj dane jeśli nie podane
        if not email:
            email = f"test_{self._random_string(8)}@example.com"
        if not password:
            password = "TestPass123!"
        if not first_name:
            first_name = "Test"
        if not last_name:
            last_name = f"User{self._random_string(5)}"
        
        # Kliknij przycisk sign up
        try:
            sign_up_btn = self.wait.until(EC.element_to_be_clickable(self.SIGN_UP_BUTTON))
            sign_up_btn.click()
        except:
            pass
        
        # Wypełnij email
        email_input = self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        
        # Wypełnij hasło
        try:
            pwd_input = self.driver.find_element(*self.PASSWORD_INPUT)
            pwd_input.clear()
            pwd_input.send_keys(password)
        except:
            pass
        
        # Wypełnij potwierdzenie hasła
        try:
            confirm_pwd = self.driver.find_element(*self.CONFIRM_PASSWORD_INPUT)
            confirm_pwd.clear()
            confirm_pwd.send_keys(password)
        except:
            pass
        
        # Wypełnij imię
        try:
            fname = self.driver.find_element(*self.FIRST_NAME_INPUT)
            fname.clear()
            fname.send_keys(first_name)
        except:
            pass
        
        # Wypełnij nazwisko
        try:
            lname = self.driver.find_element(*self.LAST_NAME_INPUT)
            lname.clear()
            lname.send_keys(last_name)
        except:
            pass
        
        # Zaakceptuj regulamin
        try:
            agree_checkbox = self.driver.find_element(*self.AGREE_TERMS)
            if not agree_checkbox.is_selected():
                agree_checkbox.click()
        except:
            pass
        
        # Kliknij submit
        try:
            submit_btn = self.driver.find_element(*self.SUBMIT_BUTTON)
            submit_btn.click()
            self.wait.until(EC.url_changes(self.driver.current_url))
        except Exception as e:
            raise Exception(f"Błąd podczas rejestracji: {str(e)}")
        
        return {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
    
    def _random_string(self, length=8):
        """Generuj losowy ciąg znaków"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def is_logged_in(self):
        """Sprawdź czy użytkownik jest zalogowany"""
        try:
            self.driver.find_element(*self.ACCOUNT_BUTTON)
            return True
        except:
            return False
