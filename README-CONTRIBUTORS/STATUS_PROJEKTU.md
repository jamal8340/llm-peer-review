# LLM Peer Review POC – status prac

## Cel projektu

Rozwijam prototyp wieloagentowego systemu symulującego recenzowanie artykułów naukowych. Docelowo projekt obejmuje optymalizację strategii autora (E1), redakcji (E2) oraz ich współdziałania (E3). Obecne prace koncentrują się na podstawach eksperymentu E2.

## Co przejąłem z poprzedniego projektu

Punktem wyjścia był **LLM Society Simulator** – symulator społeczności agentów. Zachowałem istniejące repozytorium jako bazę technologiczną, w szczególności:

- backend w **Pythonie i FastAPI** oraz strukturę API;
- integrację z **Groq** i konfigurację modelu LLM;
- frontend w **React/Vite** i istniejącą nawigację;
- mechanizmy uruchamiania aplikacji i organizację projektu.

Stary system obsługiwał posty, komentarze i interakcje społeczne. Proces recenzowania artykułów wymaga odrębnych modeli danych, ról i zasad decyzyjnych, dlatego nową logikę implementuję w osobnym module `backend/peer_review/`, bez przepisywania całego starego symulatora.

## Co zrealizowałem

1. **Przygotowałem środowisko i repozytorium** – osobny projekt Git, gałąź `feature/peer-review-poc`, działające środowiska backendu i frontendu.
2. **Zaimplementowałem modele danych** (`backend/peer_review/models.py`) dla artykułu, recenzenta, problemów w recenzji, recenzji, decyzji redakcyjnej i przypadku testowego, wraz z walidacją.
3. **Dodałem strategie E2:** R1 (*Majority-Based*) i R2 (*Expertise-Weighted*) w `backend/peer_review/strategies/editorial.py`.
4. **Przygotowałem pierwszy przypadek kontrolowany** (`backend/data/cases/case_001.json`) oraz silnik porównujący strategie (`backend/peer_review/engine.py`).
5. **Dodałem testy automatyczne** – 6 testów modeli i strategii zakończonych wynikiem `OK`.
6. **Udostępniłem eksperyment przez FastAPI** oraz dodałem ekran **Peer Review POC** w React, umożliwiający uruchomienie porównania R1/R2 i eksport wyniku JSON. Nowe API działało w środowisku lokalnym na porcie `8001`.
7. **Zaimplementowałem trzech recenzentów LLM** (`backend/peer_review/agents/reviewer.py`, `backend/peer_review/llm_experiment.py`). Każdy otrzymuje ten sam artykuł i własny profil, generuje recenzję przez Groq, a odpowiedź jest walidowana przed przekazaniem do R1/R2.

**Wynik testu integracji LLM:** model `openai/gpt-oss-20b` wygenerował trzy recenzje dla `case_001`; wszyscy recenzenci wskazali `reject`, a obie strategie wydały decyzję `reject`, zgodną z założonym wzorcem tego przypadku. Potwierdziłem działanie tego przepływu z terminala. Nie stanowi to jeszcze oceny skuteczności strategii na większym zbiorze.

## Co pozostało do wykonania

### Najbliższe zadania

- [ ] Podłączyć tryb generowania recenzji LLM do **API i widoku React** oraz przetestować pełny przepływ z interfejsu.
- [ ] Zapisywać pełne wyniki uruchomień: recenzje, decyzje, model, konfigurację i błędy.
- [ ] Rozszerzyć zestaw artykułów o przypadki o różnej jakości, z niezależną oceną referencyjną.
- [ ] Dodać testy API, generowania i walidacji odpowiedzi LLM (również przypadków błędnych).
- [ ] Uporządkować konfigurację adresu API oraz rozbieżność między portami `8000` i `8001`.

### Dalszy rozwój

- [ ] Rozbudować E2 o strategię R3 (dyskusja recenzentów), role AE/EiC i R4 (adaptacyjne zarządzanie).
- [ ] Zrealizować E1: odpowiedzi autora na uwagi, rewizje artykułu i strategie A1–A4.
- [ ] Zrealizować E3: porównanie kombinacji strategii autora i redakcji oraz analizę stabilności.
- [ ] Dodać metryki, powtórzenia eksperymentów, analizę kosztów i ewentualnie atrybucję Shapleya.

## Aktualny zakres POC

**Działa:** podstawowe modele i strategie R1/R2, porównanie na kontrolowanym przypadku, widok wyników oraz osobne uruchomienie trzech agentów LLM z przetworzeniem ich recenzji.

**Jeszcze niepotwierdzone:** uruchamianie trybu LLM bezpośrednio z Reacta i pełne testy integracyjne tego wariantu. Na razie recenzenci korzystają z tego samego modelu LLM, różnicowanego profilami w promptach; wpływ tych profili na jakość ocen wymaga osobnej walidacji.
