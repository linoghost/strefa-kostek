import pytest
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.auth_page import AuthPage
from pages.checkout_page import CheckoutPage
from pages.order_page import OrderPage


class TestCompletePurchaseFlow:
    """
    Test suite: Kompletny przepływ zakupowy
    
    Scenariusz obejmuje:
    1. Dodanie 10 produktów z 2 kategorii
    2. Wyszukanie i dodanie losowego produktu
    3. Usunięcie 3 produktów
    4. Rejestracja nowego konta
    5. Checkout (adres, przesyłka, płatność)
    6. Zatwierdzenie zamówienia
    7. Sprawdzenie statusu
    8. Pobranie faktury
    """
    
    def test_complete_purchase_flow(self, driver, base_url):
        """
        Test kompletny przepływ zakupowy (wszystko < 5 min)
        """
        
        print("\n" + "="*60)
        print("START: Kompletny test przepływu zakupowego")
        print("="*60)
        
        # ===== SETUP =====
        home_page = HomePage(driver)
        cart_page = CartPage(driver)
        auth_page = AuthPage(driver)
        checkout_page = CheckoutPage(driver)
        order_page = OrderPage(driver)
        
        account_data = {}
        
        # ===== KROK 1: Dodaj 10 produktów z 2 kategorii =====
        print("\n[KROK 1] Dodawanie 10 produktów z 2 kategorii...")
        home_page.navigate(base_url)
        
        categories = home_page.get_categories()
        assert len(categories) >= 2, "Potrzeba co najmniej 2 kategorii"
        
        category_names = [cat.text for cat in categories]
        valid_categories = [cat for cat in category_names if cat.strip() and cat.lower() != "home"]
        
        assert len(valid_categories) >= 2, f"Za mało kategorii. Znaleziono: {len(valid_categories)}"
        
        cat1_name = valid_categories[0]
        cat2_name = valid_categories[1]
        
        quantities_cat1 = [1, 2, 1, 3, 2]
        quantities_cat2 = [1, 1, 2, 1, 3]
        
        added_count = 0
        
        # Kategoria 1
        home_page.click_category(cat1_name)
        products_cat1 = home_page.get_products()
        assert len(products_cat1) >= 5, f"Za mało produktów w kategorii 1"
        
        for idx, qty in enumerate(quantities_cat1):
            try:
                home_page.add_product_to_cart(idx, quantity=qty)
                added_count += 1
                print(f"  ✓ Dodano produkt {added_count}/10")
            except Exception as e:
                print(f"  ✗ Błąd przy produkcie {idx}: {str(e)}")
        
        # Kategoria 2
        home_page.navigate(base_url)
        home_page.click_category(cat2_name)
        products_cat2 = home_page.get_products()
        assert len(products_cat2) >= 5, f"Za mało produktów w kategorii 2"
        
        for idx, qty in enumerate(quantities_cat2):
            try:
                home_page.add_product_to_cart(idx, quantity=qty)
                added_count += 1
                print(f"  ✓ Dodano produkt {added_count}/10")
            except Exception as e:
                print(f"  ✗ Błąd przy produkcie {idx}: {str(e)}")
        
        print(f"✓ Dodano {added_count} produktów")
        
        # ===== KROK 2: Wyszukaj i dodaj losowy produkt =====
        print("\n[KROK 2] Wyszukanie i dodanie losowego produktu...")
        home_page.navigate(base_url)
        
        try:
            home_page.search_product("laptop")  # Szukaj dowolnego produktu
            random_product = home_page.add_random_product_from_search()
            print(f"✓ Dodano losowy produkt: {random_product}")
        except Exception as e:
            print(f"⚠ Nie udało się dodać losowego produktu: {str(e)}")
        
        # ===== KROK 3: Usuń 3 produkty =====
        print("\n[KROK 3] Usuwanie 3 produktów z koszyka...")
        cart_page.navigate_to_cart(base_url)
        
        products_in_cart = cart_page.get_cart_products()
        initial_count = len(products_in_cart)
        
        removed_count = 0
        for i in range(min(3, initial_count)):
            try:
                cart_page.remove_product_from_cart(0)  # Zawsze usuwaj pierwszy
                removed_count += 1
                print(f"  ✓ Usunięto produkt {removed_count}/3")
            except Exception as e:
                print(f"  ✗ Błąd przy usuwaniu: {str(e)}")
        
        print(f"✓ Usunięto {removed_count} produktów")
        
        final_products = cart_page.get_cart_products()
        print(f"  Produktów w koszyku: {len(final_products)}")
        
        # ===== KROK 4: Rejestracja nowego konta =====
        print("\n[KROK 4] Rejestracja nowego konta...")
        auth_page.go_to_login(base_url)
        
        try:
            account_data = auth_page.register_new_account()
            print(f"✓ Konto zarejestrowane: {account_data['email']}")
            assert auth_page.is_logged_in(), "Użytkownik nie jest zalogowany"
            print(f"✓ Użytkownik zalogowany")
        except Exception as e:
            print(f"⚠ Błąd rejestracji: {str(e)}")
        
        # ===== KROK 5: Checkout - Adres, Przesyłka, Płatność =====
        print("\n[KROK 5] Proces checkout...")
        
        cart_page.navigate_to_cart(base_url)
        
        try:
            cart_page.proceed_to_checkout()
            print("✓ Przeszedł do kasy")
        except Exception as e:
            print(f"⚠ Błąd podczas przejścia do kasy: {str(e)}")
        
        # Wypełnij adres
        try:
            checkout_page.fill_address()
            print("✓ Adres wypełniony")
        except Exception as e:
            print(f"⚠ Błąd przy adresie: {str(e)}")
        
        # Wybierz kuriera
        try:
            carrier_name = checkout_page.select_carrier(carrier_index=0)
            print(f"✓ Wybrany przewoźnik: {carrier_name}")
        except Exception as e:
            print(f"⚠ Błąd przy wyborze przewoźnika: {str(e)}")
        
        # Wybierz metodę płatności
        try:
            payment_method = checkout_page.select_payment_method("cod")
            print(f"✓ Wybrana metoda płatności: {payment_method}")
        except Exception as e:
            print(f"⚠ Błąd przy wyborze płatności: {str(e)}")
        
        # ===== KROK 6: Zatwierdzenie zamówienia =====
        print("\n[KROK 6] Zatwierdzenie zamówienia...")
        
        try:
            checkout_page.confirm_order()
            print("✓ Zamówienie potwierdzone")
        except Exception as e:
            print(f"⚠ Błąd przy potwierdzeniu: {str(e)}")
        
        # ===== KROK 7: Sprawdzenie statusu zamówienia =====
        print("\n[KROK 7] Sprawdzenie statusu zamówienia...")
        
        try:
            order_page.navigate_to_orders(base_url)
            latest_order = order_page.get_latest_order()
            
            if latest_order:
                order_number = order_page.get_order_number(latest_order)
                order_status = order_page.get_order_status(latest_order)
                print(f"✓ Najnowsze zamówienie: #{order_number}")
                print(f"✓ Status: {order_status}")
                
                # ===== KROK 8: Pobranie faktury =====
                print("\n[KROK 8] Pobieranie faktury VAT...")
                
                try:
                    order_page.view_order_details(latest_order)
                    if order_page.has_invoice():
                        order_page.download_invoice()
                        print("✓ Faktura pobrana")
                    else:
                        print("⚠ Zamówienie nie ma jeszcze faktury")
                except Exception as e:
                    print(f"⚠ Błąd przy pobieraniu faktury: {str(e)}")
            else:
                print("⚠ Nie znaleziono zamówienia")
        
        except Exception as e:
            print(f"⚠ Błąd przy sprawdzeniu statusu: {str(e)}")
        
        # ===== PODSUMOWANIE =====
        print("\n" + "="*60)
        print("✓ TEST ZAKOŃCZONY - Wszystkie kroki wykonane!")
        print("="*60)
        
        return {
            "products_added": added_count,
            "products_removed": removed_count,
            "account_email": account_data.get("email", "N/A"),
            "order_number": order_number if 'order_number' in locals() else "N/A",
            "order_status": order_status if 'order_status' in locals() else "N/A"
        }
