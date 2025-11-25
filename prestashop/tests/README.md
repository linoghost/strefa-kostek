# 🧪 Selenium Tests - PrestaShop

Automatyczne testy Selenium dla PrestaShopa.

## 📁 Struktura projektu

```
tests/
├── selenium/
│   ├── pages/              # Page Object Models
│   │   ├── __init__.py
│   │   ├── home_page.py    # Strona główna
│   │   └── cart_page.py    # Strona koszyka
│   ├── conftest.py         # Konfiguracja pytest i fixtures
│   ├── test_add_to_cart.py # Główny test
│   └── __init__.py
├── requirements.txt        # Zależności Python
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

Wymagany: Python 3.7+

## 🧬 Wymagania

- **Python 3.7+**
- **Chrome/Chromium** (webdriver-manager będzie pobierać automatycznie)
- **PrestaShop** uruchomiony na `http://localhost`

## 🎯 Uruchomienie testów

### Uruchom wszystkie testy
```bash
cd tests/selenium
pytest -v
```

### Uruchom konkretny test
```bash
pytest -v test_add_to_cart.py::TestAddProductsToCart::test_add_10_products_from_two_categories
```

### Uruchom z raportem HTML
```bash
pytest -v --html=report.html --self-contained-html
```

### Uruchom w trybie bezgłowy (bez GUI)
Odkomentuj linię w `conftest.py`:
```python
chrome_options.add_argument("--headless")
```

## 📊 Test: Dodanie 10 produktów

**Plik:** `test_add_to_cart.py`

**Co robi test:**
1. ✅ Nawiguje na stronę główną
2. ✅ Wchodzi do pierwszej kategorii
3. ✅ Dodaje 5 produktów w ilościach: 1, 2, 1, 3, 2
4. ✅ Wchodzi do drugiej kategorii
5. ✅ Dodaje 5 produktów w ilościach: 1, 1, 2, 1, 3
6. ✅ Sprawdza koszyk
7. ✅ Weryfikuje obecność wszystkich produktów

**Oczekiwany wynik:** Wszystkie 10 produktów w koszyku

## 🔧 Dostosowanie testów

### Zmiana URL
Edytuj `conftest.py`:
```python
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8080"  # Zmień port jeśli potrzeba
```

### Zmiana ilości produktów
Edytuj `test_add_to_cart.py`:
```python
quantities_cat1 = [1, 2, 1, 3, 2]  # Zmień na swoje wartości
quantities_cat2 = [1, 1, 2, 1, 3]
```

### Włączenie trybu headless
W `conftest.py` odkomentuj:
```python
chrome_options.add_argument("--headless")
```

## 📝 Dodawanie nowych testów

1. Utwórz nowy plik `test_*.py` w `tests/selenium/`
2. Użyj dostępnych Page Objects: `HomePage`, `CartPage`
3. Uruchom: `pytest test_moj_test.py`

### Przykład:
```python
def test_search_product(driver, base_url):
    home = HomePage(driver)
    home.navigate(base_url)
    home.search_product("laptop")
    products = home.get_products()
    assert len(products) > 0
```

## 🐛 Debugowanie

### Wyświetl szczegóły błędów
```bash
pytest -v -s  # -s pokazuje print() statements
```

### Zwiększ timeout
Edytuj `conftest.py`:
```python
driver.implicitly_wait(20)  # 20 sekund zamiast 10
```

## 📚 Przydatne linki

- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Best Practices](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

## 💡 Tips

- Używaj Page Objects do wszystkich interakcji z UI
- Zawsze stosuj explicit waits zamiast time.sleep()
- Pisz czytelne nazwy testów
- Dodawaj assercje dla każdego wariantu sukcesu

---

**Autor:** Automated QA
**Ostatnia aktualizacja:** 2025-11-23
