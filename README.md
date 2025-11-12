# 🧱 StrefaKostek – PrestaShop (Docker)

Projekt odwzorowujący funkcjonalność i wygląd sklepu **StrefaKostek.pl**, zbudowany na platformie **PrestaShop** i uruchamiany w kontenerach **Docker**.

## 📦 Opis projektu

Celem projektu jest przygotowanie środowiska deweloperskiego sklepu opartego o **PrestaShop**, inspirowanego stroną [strefakostek.pl](https://strefa-kostek.pl).  
Projekt działa w oparciu o **Docker Compose**, co pozwala łatwo uruchomić kompletne środowisko (aplikacja + baza danych) bez ręcznej konfiguracji.

## ⚙️ Wykorzystane oprogramowanie

- **PrestaShop:** 8.x  
- **PHP:** 8.1+  
- **MySQL:** 8.0  
- **Apache (w kontenerze)**  
- **Docker & Docker Compose**  
- **Composer 2.x**  
- **Node.js / npm** *(opcjonalnie – do kompilacji frontu)*

## 🚀 Uruchomienie projektu (Docker)

### 1️⃣ Klonowanie repozytorium
```bash
git clone https://github.com/<twoj-uzytkownik>/<repozytorium>.git
cd <repozytorium>
```

### 2️⃣ Uruchomienie środowiska
```bash
docker compose up -d
```
Aplikacja będzie dostępna pod adresem:  
👉 [http://localhost:8080](http://localhost:8080)

### 3️⃣ Zarządzanie kontenerami
| Komenda | Opis |
|----------|------|
| `docker compose ps` | lista aktywnych kontenerów |
| `docker compose logs -f` | podgląd logów |
| `docker compose down` | zatrzymanie środowiska |
| `docker compose down -v` | zatrzymanie i usunięcie wolumenów (czyści bazę danych) |

## 🧑‍💻 Deweloperka

### Czyszczenie cache PrestaShop
```bash
docker compose exec prestashop rm -rf var/cache/*
```

### Instalacja zależności
```bash
docker compose exec prestashop composer install
```

## 👥 Zespół projektowy

| Imię i nazwisko | Index |
|-----------------|------|
| Julia Kryszczuk | 197753 |
| Jeremi Nowak | 197611 |
| Michał Mrowicki | 197982 |
| Karol Banach | 197912 |

## 🔐 Licencja

Projekt tworzony **w celach edukacyjnych**.  
Nie jest powiązany z oficjalnym sklepem **StrefaKostek.pl** ani jego właścicielem.
