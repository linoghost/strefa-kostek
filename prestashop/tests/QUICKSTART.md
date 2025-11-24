# 🚀 SZYBKI START

## 1️⃣ Instalacja (2 minuty)

### Windows:
```bash
cd tests
setup.bat
```

### Linux/Mac:
```bash
cd tests
chmod +x setup.sh
./setup.sh
```

### Ręczna instalacja:
```bash
cd tests
pip install -r requirements.txt
```

---

## 2️⃣ Uruchomienie testów

### Opcja A: Skrypt Python (Polecane)
```bash
cd tests
python run_tests.py
```

### Opcja B: Bezpośrednio pytest
```bash
cd tests/selenium
pytest -v -s
```

### Opcja C: Konkretny test
```bash
cd tests/selenium
pytest -v test_complete_purchase_flow.py
```

---

## 3️⃣ Testy do wyboru

| Test | Czas | Opis |
|------|------|------|
| `test_add_to_cart.py` | 2-3 min | Dodaj 10 produktów z 2 kategorii |
| `test_complete_purchase_flow.py` | <5 min | **Główny test** - kompletny przepływ zakupowy |

---

## ⚡ Szybsze testowanie

Włącz **headless mode** (bez GUI = ~2x szybciej):

`conftest.py` → odkomentuj:
```python
chrome_options.add_argument("--headless")
```

---

## 🔍 Debugowanie

### Pokaż szczegóły:
```bash
pytest -v -s
```

### Pokaż błędy:
```bash
pytest -v -s --tb=long
```

### Raport HTML:
```bash
pytest --html=report.html --self-contained-html
```

---

## ❓ FAQ

**P: Jak zmienić URL?**  
O: Edytuj `conftest.py` → `base_url` fixture

**P: Test się wiesza?**  
O: Sprawdź czy PrestaShop działa na localhost:80

**P: Jak dodać nowy test?**  
O: Stwórz `test_*.py` w `tests/selenium/`

**P: Gdzie są raporty?**  
O: W folderze `tests/` po uruchomieniu z `--html` flagą

---

## 📞 Wsparcie

- Sprawdź `README.md` - pełna dokumentacja
- Logi w konsoli (`-s` flag)
- Elementy w dev tools Chromium (F12)

---

**Gotowe? Uruchom:** `python run_tests.py` 🚀
