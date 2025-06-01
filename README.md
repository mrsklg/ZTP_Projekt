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

## Funkcjonalności

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

Widoki desktopowe

![image](https://github.com/user-attachments/assets/9929e33c-cd13-47bf-8bff-61128c08e5e9)

![image](https://github.com/user-attachments/assets/24633199-a3e3-435d-8264-09f7e5101933)

![image](https://github.com/user-attachments/assets/f7f3eca7-7c33-4958-9404-cabcdfd9624d)

![image](https://github.com/user-attachments/assets/b8b09781-736f-4841-8bd6-2b80c6df5c9e)

![image](https://github.com/user-attachments/assets/439c0eb1-3923-4618-9eaf-41fc7d71e99e)

![image](https://github.com/user-attachments/assets/984acbe0-464b-4046-b739-2323cdab9e09)

![image](https://github.com/user-attachments/assets/21642465-b5cd-4fe1-9341-7d994907c63b)


Widoki mobilne

![image](https://github.com/user-attachments/assets/843163b6-7f31-43e2-9fbd-29b54a852865)

![image](https://github.com/user-attachments/assets/9eb6b8af-9c5c-4de7-99d3-248d958acab0)

![image](https://github.com/user-attachments/assets/da54d934-84a2-4ebd-88a5-bd2c3f2b85a5)

![image](https://github.com/user-attachments/assets/2a48a619-8224-4fda-af3e-022b3e16f360)

![image](https://github.com/user-attachments/assets/9cb5c153-8a48-4d54-82ba-bf7327d78f0f)

![image](https://github.com/user-attachments/assets/a681a59c-6409-4948-8ed1-016acc77e96e)

![image](https://github.com/user-attachments/assets/48753549-b252-4471-8e4b-c712a72d27db)

## ERD
Diagram bazy danych.

![Zrzut ekranu 2025-06-01 190153](https://github.com/user-attachments/assets/44681b34-ce15-4314-83be-cf864b8d0da3)

