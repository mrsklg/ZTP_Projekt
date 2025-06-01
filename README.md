# Watchy
![logo](https://github.com/user-attachments/assets/906c8b93-c478-4fd5-abd7-5c65778526f5)

## Spis treści

- [Opis](#Opis)
- [Funkcjonalności](#Funkcjonalności)
- [Technologie](#Technologie)
- [Sktruktura projektu](#Struktura)
- [Uruchomienie aplikacji lokalnie](#Uruchomienie)
- [Ilustracje](#Ilustracje)
- [ERD](#ERD)

## Opis
Aplikacja pozwala użytkownikom na tworzenie listy filmów do obejrzenia, a także oznaczania filmów jako obejrzanych. Zbudowana z użyciem **React (frontend)**, **Flask (backend)**, **PostgreSQL (baza danych)** i konteneryzowany za pomocą **Dockera**.

## Funkcjonalnośći

- Dodawanie filmów do listy
- Oznaczanie filmów jako obejrzane lub do obejrzenia
- Przeglądanie filmów z podziałem na status
- Przechowywanie danych w relacyjnej bazie PostgreSQL


## Technologie

- Flask (Python)
- React (JavaScript)
- PostgreSQL
- Docker
- Nginx

---

## Struktura projektu

```
ZTP_Projekt/
├── backend/            # Flask backend z kontrolerami, modelami i testami
│   ├── app.py            # Główna aplikacja Flask
│   ├── controllers/      # Logika aplikacji i api
│   ├── models/           # Modele danych 
│   ├── tests/            # Testy jednostkowe
│   └── utils/            # Pomocnicze funkcje 
├── db/                 # Inicjalizacja bazy danych
│   └── init/
│       └── init.sql        # Skrypt SQL tworzący strukturę bazy
├── frontend/           # React frontend z komponentami
│   ├── .env              # Zmienne środowiskowe 
│   ├── Dockerfile        # Budowanie frontendu jako kontener
│   ├── package.json      # Zależności Reacta
│   ├── public/           #Statyczne zasoby i plik HTML główny
│   ├── src/              # Główny kod źródłowy aplikacji React
│   |   ├── index.js        # Punkt wejścia aplikacji React
│   |   ├── App.js          # Główny komponent aplikacji i konfiguracja routingu
│   |   ├── api/            # Funkcje do komunikacji z backendem (fetch/Axios)
|   |   ├── assets/         # Zasoby graficzne (obrazy, loga, wektory)
│   |   ├── components/     # Komponenty wielokrotnego użytku (UI i logika)
│   |   ├── pages/          # Widoki/strony aplikacji
│   |   ├── styles/         # Pliki CSS dla komponentów i stron
|   │   └── test/           # Pliki testów dla frontendu 
├── docker-compose.yml    # Uruchamia wszystkie usługi Dockera
└── README.md             # Dokumentacja projektu
```

### Opis głównych folderów

### `backend/`
- `app.py` – Główna aplikacja Flask z definicją serwera i punktów wejścia.
- `controllers/` – Pliki odpowiadające za obsługę logiki aplikacji:
  - `auth_controller.py`, `movie_controller.py`, `user_controller.py`, `db_controller.py`
- `models/` – Definicje modeli danych
- `utils/db.py` – Konfiguracja i połączenie z bazą danych.
- `tests/` – Struktura testów jednostkowych:
  - `tests/controllers/` – Testy kontrolerów
  - `tests/models/` – Testy modeli

### `db/init/`
- `init.sql` – Skrypt SQL do utworzenia struktury bazy danych PostgreSQL.

### `frontend/`
- `.env` – Zmienne środowiskowe np. URL backendu
- `Dockerfile` – Obraz Dockera do budowy frontendu
- `package.json` – Lista zależności i skryptów
- `components/`  – Komponenty React (przyciski, formularze itp.)
- `public` -  Statyczne zasoby i plik HTML główny
- `src` - Główny kod źródłowy aplikacji React
  - `api` - Funkcje do komunikacji z backendem (fetch/Axios)
  - `assets` - Zasoby graficzne
  - `components` - Komponenty wielokrotnego użytku
  - `pages` - Widoki aplikacji
  - `styles` - Pliki CSS
  - `test` - testy frontendu
- `default.conf` – Potencjalna konfiguracja nginx dla frontendu

### `docker-compose.yml`
- Uruchamia:
  - `backend` – Aplikację Flask
  - `frontend` – Aplikację React
  - `db` – PostgreSQL
  - `nginx` – jako reverse proxy

---

## Uruchomienie aplikacji lokalnie

### 1. Wymagania

- Zainstalowany **Docker** i **Docker Compose**

### 2. Klonowanie repozytorium

```bash
git clone https://github.com/mrsklg/ZTP_Projekt.git
cd ZTP_Projekt
```

### 3. Uruchomienie kontenerów

```bash
docker-compose up --build
```

### 4. Aplikacja będzie dostępna pod:

- [http://localhost:3001](http://localhost:3001)  


---

## Ilustracje

## ERD
Diagram bazy danych.
![erd](https://github.com/user-attachments/assets/b2d73591-8dc6-4fe3-865a-af9d37bdc7a1)
