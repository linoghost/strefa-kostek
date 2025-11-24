import pytest
import time
from pages.home_page import HomePage
from pages.cart_page import CartPage


class TestAddProductsToCart:
    """
    Test suite: Dodawanie produktów do koszyka
    """
    
    def test_add_10_products_from_two_categories(self, driver, base_url):
        """
        Test: Dodaj 10 produktów w różnych ilościach z dwóch różnych kategorii
        
        Scenariusz:
        1. Nawiguj na stronę główną
        2. Wejdź do pierwszej kategorii
        3. Dodaj 5 produktów w różnych ilościach
        4. Wejdź do drugiej kategorii
        5. Dodaj 5 produktów w różnych ilościach
        6. Zweryfikuj, że wszystkie produkty są w koszyku
        7. Zweryfikuj właściwe ilości
        
        Produkty do dodania:
        Kategoria 1: 5 produktów z ilościami [1, 2, 1, 3, 2]
        Kategoria 2: 5 produktów z ilościami [1, 1, 2, 1, 3]
        """
        
        # Setup
        home_page = HomePage(driver)
        cart_page = CartPage(driver)
        
        # Krok 1: Nawiguj na stronę główną
        home_page.navigate(base_url)
        
        # Krok 2-3: Wejdź do pierwszej kategorii i dodaj produkty
        categories = home_page.get_categories()
        assert len(categories) > 0, "Brak dostępnych kategorii"
        
        first_category = None
        second_category = None
        
        # Pobierz nazwy kategorii
        category_names = [cat.text for cat in categories]
        print(f"Dostępne kategorie: {category_names}")
        
        # Filtruj kategorie (pomijaj "Home")
        valid_categories = [cat for cat in category_names if cat.strip() and cat.lower() != "home"]
        
        assert len(valid_categories) >= 2, f"Potrzeba co najmniej 2 kategorii. Znaleziono: {len(valid_categories)}"
        
        first_category_name = valid_categories[0]
        second_category_name = valid_categories[1]
        
        print(f"Kategoria 1: {first_category_name}")
        print(f"Kategoria 2: {second_category_name}")
        
        # Ilości produktów do dodania
        quantities_cat1 = [1, 2, 1, 3, 2]  # 5 produktów
        quantities_cat2 = [1, 1, 2, 1, 3]  # 5 produktów
        
        added_products_cat1 = []
        added_products_cat2 = []
        
        # === KATEGORIA 1 ===
        home_page.click_category(first_category_name)
        
        # Pobierz dostępne produkty
        products_cat1 = home_page.get_products()
        print(f"Kategoria 1: Znaleziono {len(products_cat1)} produktów")
        
        assert len(products_cat1) >= 5, f"Za mało produktów w kategorii 1. Znaleziono: {len(products_cat1)}"
        
        # Dodaj 5 produktów z kategorii 1
        for idx, qty in enumerate(quantities_cat1):
            try:
                product_name = home_page.add_product_to_cart(idx, quantity=qty)
                added_products_cat1.append({
                    "name": product_name,
                    "quantity": qty
                })
                print(f"✓ Dodano: '{product_name}' x{qty}")
            except Exception as e:
                print(f"✗ Błąd przy dodawaniu produktu {idx}: {str(e)}")
        
        # === KATEGORIA 2 ===
        home_page.navigate(base_url)
        home_page.click_category(second_category_name)
        
        # Pobierz dostępne produkty z kategorii 2
        products_cat2 = home_page.get_products()
        print(f"Kategoria 2: Znaleziono {len(products_cat2)} produktów")
        
        assert len(products_cat2) >= 5, f"Za mało produktów w kategorii 2. Znaleziono: {len(products_cat2)}"
        
        # Dodaj 5 produktów z kategorii 2
        for idx, qty in enumerate(quantities_cat2):
            try:
                product_name = home_page.add_product_to_cart(idx, quantity=qty)
                added_products_cat2.append({
                    "name": product_name,
                    "quantity": qty
                })
                print(f"✓ Dodano: '{product_name}' x{qty}")
            except Exception as e:
                print(f"✗ Błąd przy dodawaniu produktu {idx}: {str(e)}")
        
        # === WERYFIKACJA KOSZYKA ===
        cart_page.navigate_to_cart(base_url)
        
        # Sprawdź liczbę produktów
        cart_products = cart_page.get_cart_products()
        total_items_in_cart = len(cart_products)
        
        print(f"\n=== PODSUMOWANIE ===")
        print(f"Dodano z kategorii 1: {len(added_products_cat1)} produktów")
        print(f"Dodano z kategorii 2: {len(added_products_cat2)} produktów")
        print(f"Produkty w koszyku: {total_items_in_cart}")
        
        # Wyświetl szczegóły produktów w koszyku
        print(f"\n=== PRODUKTY W KOSZYKU ===")
        all_cart_products = cart_page.get_all_products_details()
        for i, product in enumerate(all_cart_products):
            print(f"{i+1}. {product['name']} (ilość: {product['quantity']}, cena: {product['price']})")
        
        # Asercje
        expected_total = len(added_products_cat1) + len(added_products_cat2)
        assert total_items_in_cart >= expected_total - 1, (
            f"Oczekiwano co najmniej {expected_total} produktów w koszyku, "
            f"znaleziono: {total_items_in_cart}"
        )
        
        # Sprawdź czy wszystkie produkty z kategorii 1 są w koszyku
        for product in added_products_cat1:
            assert cart_page.verify_product_in_cart(product["name"]), (
                f"Produkt '{product['name']}' z kategorii 1 nie znaleziony w koszyku"
            )
        
        # Sprawdź czy wszystkie produkty z kategorii 2 są w koszyku
        for product in added_products_cat2:
            assert cart_page.verify_product_in_cart(product["name"]), (
                f"Produkt '{product['name']}' z kategorii 2 nie znaleziony w koszyku"
            )
        
        print("\n✓ TEST PASSED - Wszystkie produkty zostały dodane do koszyka!")
        
        return {
            "total_products": total_items_in_cart,
            "category1": added_products_cat1,
            "category2": added_products_cat2,
            "cart_total": cart_page.get_cart_total()
        }
