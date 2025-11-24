# 🧪 Selenium Tests - PrestaShop

Automatyczne testy Selenium dla PrestaShopa. Kompletny przepływ zakupowy wykonywany w mniej niż 5 minut.

## 📁 Struktura projektu

```
tests/
├── selenium/
│   ├── pages/                          # Page Object Models
│   │   ├── __init__.py
│   │   ├── home_page.py               # Strona główna, kategorie, szukanie
│   │   ├── cart_page.py               # Koszyk, usuwanie produktów
│   │   ├── auth_page.py               # Rejestracja i logowanie
│   │   ├── checkout_page.py           # Kasa (adres, przesyłka, płatność)
│   │   └── order_page.py              # Historia zamówień, faktury
│   ├── conftest.py                    # Konfiguracja pytest i fixtures
│   ├── test_add_to_cart.py            # Test dodawania produktów
│   ├── test_complete_purchase_flow.py # Test kompletny (główny)
│   └── __init__.py
├── requirements.txt                   # Zależności Python
├── run_tests.py                       # Skrypt uruchamiający testy
├── pytest.ini                         # Konfiguracja pytest
└── README.md
```

## 🚀 Instalacja

### 1. Zainstaluj zależności Python

```bash
cd tests
pip install -r requirements.txt
```

### 2. Sprawdź wersję Pythona

```bash
python --version
```

Wymagany: **Python 3.7+**

## 🧬 Wymagania

- **Python 3.7+**
- **Chrome/Chromium** (webdriver-manager będzie pobierać automatycznie)
- **PrestaShop** uruchomiony na `http://localhost`

## 🎯 Uruchomienie testów

### Opcja 1: Uruchom przy pomocy skryptu

```bash
cd tests
python run_tests.py
```

### Opcja 2: Uruchom przy pomocy pytest bezpośrednio

```bash
cd tests/selenium
pytest -v -s
```

### Uruchom konkretny test

```bash
# Test dodawania produktów
pytest -v test_add_to_cart.py

# Test kompletny przepływ zakupowy
pytest -v test_complete_purchase_flow.py
```

### Uruchom z raportem HTML

```bash
pytest -v --html=report.html --self-contained-html
```

### Uruchom w trybie bezgłowy (bez GUI - szybciej!)

Edytuj `conftest.py` i odkomentuj linię:
```python
chrome_options.add_argument("--headless")
```

Wtedy test będzie działać ~2x szybciej!

## 📊 Testy

### Test 1: Dodanie produktów (`test_add_to_cart.py`)

**Czas:** ~2-3 minuty

**Co robi:**
- Dodaje 5 produktów z kategorii 1 (ilości: 1, 2, 1, 3, 2)
- Dodaje 5 produktów z kategorii 2 (ilości: 1, 1, 2, 1, 3)
- Weryfikuje wszystkie produkty w koszyku

### Test 2: Kompletny przepływ zakupowy (`test_complete_purchase_flow.py`) ⭐

**Czas:** <5 minut

**Co robi:**
1. ✅ Dodaje 10 produktów z 2 kategorii
2. ✅ Wyszukuje produkt i dodaje losowy ze znalezionych
3. ✅ Usuwa 3 produkty z koszyka
4. ✅ Rejestruje nowe konto
5. ✅ Wypełnia formularz adresu
6. ✅ Wybiera przewoźnika (z 2 dostępnych)
7. ✅ Wybiera metodę płatności (przy odbiorze)
8. ✅ Potwierdza zamówienie
9. ✅ Sprawdza status zamówienia
10. ✅ Pobiera fakturę VAT

## 🔧 Dostosowanie testów

### Zmiana URL

Edytuj `conftest.py`:
```python
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8080"  # Zmień na swój adres
```

### Zmiana ilości produktów

Edytuj `test_add_to_cart.py`:
```python
quantities_cat1 = [1, 2, 1, 3, 2]  # Dostosuj do swoich potrzeb
quantities_cat2 = [1, 1, 2, 1, 3]
```

### Zmiana metody płatności

W `test_complete_purchase_flow.py` zmień:
```python
payment_method = checkout_page.select_payment_method("cod")   # Przy odbiorze
# lub
payment_method = checkout_page.select_payment_method("bank")  # Przelew
```

## 🐛 Debugowanie

### Wyświetl szczegóły błędów i print statements

```bash
pytest -v -s
```

### Zwiększ timeout (jeśli strona ładuje się wolno)

Edytuj `conftest.py`:
```python
driver.implicitly_wait(5)  # Zmień z 3 na 5 lub więcej
```

### Pokaż zrzuty ekranu przy błędach

Zainstaluj:
```bash
pip install pytest-screenshot
```

Uruchom z flagą:
```bash
pytest --screenshot=on-failure
```

## 📚 Przydatne linki

- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [PrestaShop Documentation](https://devdocs.prestashop.com/)
- [Page Object Model Best Practices](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

## 💡 Tips & Tricks

### Szybciej uruchomić testy:
1. ✅ Używaj `--headless` (bez GUI)
2. ✅ Upewnij się że PrestaShop jest już uruchomiony
3. ✅ Zamknij inne procesy Chrome/Chromium
4. ✅ Wyłącz rozszerzenia przeglądarki w Chrome

### Lepsze testowanie:
- Zawsze używaj Page Objects do wszystkich interakcji z UI
- Stosuj explicit waits zamiast `time.sleep()`
- Pisz czytelne nazwy testów
- Dodawaj assercje dla każdego wariantu sukcesu
- Sprawdzaj logi w konsoli (`-s` flag)

### Jak naprawić powolne testy:
1. Sprawdź czy strona rzeczywiście się ładuje (~1-2 sec)
2. Zmniejsz implicit wait w `conftest.py`
3. Włącz `--headless`
4. Upewnij się że serwer nie ma problów

## 🚨 Troubleshooting

| Problem | Rozwiązanie |
|---------|-----------|
| `ConnectionError: localhost` | Upewnij się że PrestaShop działa na localhost |
| `Element not found` | Sprawdź selektory CSS w dev tools (F12) |
| `Timeout exception` | Zwiększ implicit wait w conftest.py |
| `Headless mode nie działa` | Chrome musi być zainstalowany systemowo |
| `Powolne testy` | Włącz --headless flag |

## 📝 Dodawanie nowych testów

1. Utwórz nowy plik `test_*.py` w `tests/selenium/`
2. Importuj Page Objects z `pages`
3. Używaj fixtures z `conftest.py`
4. Uruchom: `pytest test_moj_test.py`

### Przykład:

```python
def test_my_custom_test(driver, base_url):
    home = HomePage(driver)
    home.navigate(base_url)
    
    products = home.get_products()
    assert len(products) > 0, "Nie znaleziono produktów"
    
    print("✓ Test wykonany pomyślnie!")
```

## 🏆 Best Practices

✅ **DO:**
- Używaj Page Objects dla każdej strony
- Stosuj WebDriverWait dla dynamicznych elementów
- Pisz testy z myślą o selektorach CSS
- Dodawaj descriptive print statements
- Zawsze cleanup po testach (fixture `yield`)

❌ **DON'T:**
- Nie używaj `time.sleep()` - zamiast tego WebDriverWait
- Nie hardcoduj wartości - używaj parametrów
- Nie ignoruj błędów - zawsze loguj
- Nie pisz testów bez assercji
- Nie testuj na produkcji!

---

**Autor:** Automated QA  
**Data:** 2025-11-24  
**Wersja:** 2.0 - Kompletny przepływ zakupowy  
**Status:** ✅ Gotowe do użytku
