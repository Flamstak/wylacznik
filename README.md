# Zaawansowany Planer Systemu

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![UI](https://img.shields.io/badge/UI-sv_ttk-orange.svg)

Prosta, ale potężna aplikacja okienkowa (GUI) dla systemu Windows do planowania zamknięcia lub ponownego uruchomienia komputera. Zbudowana przy użyciu `Tkinter` i stylizowana za pomocą `sv-ttk` dla nowoczesnego wyglądu.

## 🚀 Kluczowe Funkcje

* **Dwie Akcje:** Wybierz między zaplanowaniem **zamknięcia** lub **ponownego uruchomienia** systemu.
* **Dwa Tryby Czasu:**
    * **Odliczanie:** Ustaw konkretny czas (godziny, minuty, sekundy), po którym nastąpi akcja.
    * **Konkretna Godzina:** Wybierz dokładną godzinę (np. 23:00), o której system ma wykonać zadanie.
* **Wymuszenie Akcji:** Opcja wymuszenia zamknięcia aplikacji, ignorując niezapisane zmiany w programach.
* **Szybkie Presety:** Przyciski do szybkiego ustawiania odliczania (30 min, 1 godz., 2 godz.).
* **Licznik na Żywo:** Po zaplanowaniu, aplikacja wyświetla licznik czasu pozostałego do wykonania akcji.
* **Anulowanie Zadania:** Możliwość anulowania zaplanowanego zadania w dowolnym momencie.
* **Nowoczesny Interfejs:** Czysty, ciemny motyw dzięki bibliotece `sv-ttk`.

## 🖼️ Podgląd Interfejsu



[Image of the application's user interface]


*Główny interfejs aplikacji z wybranym trybem "Odliczanie".*

## 🛠️ Wymagania

* **System Operacyjny:** Windows (ze względu na użycie poleceń `shutdown /s`, `/r`, `/a`).
* **Python:** Wersja 3.6 lub nowsza.
* **Biblioteki Python:** `sv-ttk`

## ⚙️ Instalacja i Uruchomienie

1.  **Sklonuj repozytorium (lub pobierz plik `.py`):**
    ```bash
    git clone github.com/Flamstak/wylacznik.git(https://github.com/Flamstak/wylacznik.git)
    cd nazwa-folderu
    ```

2.  **Zainstaluj wymaganą bibliotekę:**
    Aplikacja używa `sv-ttk` do nadania nowoczesnego wyglądu.
    ```bash
    pip install sv-ttk
    ```

3.  **Uruchom aplikację:**
    ```bash
    python twoja_nazwa_pliku.py
    ```

4.  **🚨 WAŻNE:**
    Do wykonania poleceń `shutdown` aplikacja **musi być uruchomiona z uprawnieniami administratora**. Kliknij prawym przyciskiem myszy na plik `.py` i wybierz "Uruchom jako administrator" lub uruchom swoje terminal/CMD jako administrator przed wywołaniem skryptu.

## 🕹️ Jak Używać

1.  **Wybierz Akcję:** Z listy rozwijanej wybierz "Zamknij" lub "Uruchom Ponownie".
2.  **Ustaw Czas:**
    * Wybierz "Odliczanie" i wpisz liczbę godzin, minut i sekund.
    * LUB wybierz "Konkretna Godzina" i ustaw godzinę docelową (w formacie 24-godzinnym).
3.  **(Opcjonalnie)** Zaznacz "Wymuś zamknięcie", jeśli chcesz, aby system zignorował niezapisane dane.
4.  Kliknij **"✅ Zaplanuj"**. Na dole pojawi się licznik.
5.  Aby anulować, kliknij **"❌ Anuluj"** w dowolnym momencie.

## 📄 Licencja

Ten projekt jest udostępniany na licencji MIT. Zobacz plik `LICENSE`, aby uzyskać więcej informacji.