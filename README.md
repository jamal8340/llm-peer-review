# LLM Peer Review POC

Proof of Concept systemu symulującego proces recenzowania artykułów naukowych z wykorzystaniem agentów LLM.

## Cel projektu

Celem projektu jest badanie i optymalizacja strategii autorów i redakcji czasopism naukowych w środowisku wieloagentowym.

Projekt obejmuje trzy główne eksperymenty:

- **E1 – Author Strategy Optimization:** optymalizacja strategii odpowiadania na recenzje i poprawiania artykułów.
- **E2 – Editorial Strategy Optimization:** optymalizacja strategii podejmowania decyzji redakcyjnych.
- **E3 – Joint Strategy Optimization:** wspólna optymalizacja strategii autora i redakcji.

## Zakres pierwszego POC

Pierwsza wersja będzie koncentrować się na eksperymencie E2, w szczególności na porównaniu:

- R1 – Majority-Based
- R2 – Expertise-Weighted

Minimalny POC będzie wykorzystywał artykuły testowe, trzy recenzje oraz niezależną ocenę poprawności decyzji.

## Technologie

- Python 3.11+
- FastAPI
- Groq API / LLM
- React
- Vite
- Zustand

## Status

Projekt znajduje się na etapie przygotowania architektury i implementacji pierwszego POC.

## Baza projektu

Projekt rozwijany na podstawie wcześniejszego symulatora społeczności agentów LLM (`studioProjektowe2`). Wybrane mechanizmy backendu i frontendu będą adaptowane do symulacji recenzowania naukowego.

## Plan rozwoju

1. Przygotowanie repozytorium i środowiska.
2. Implementacja modeli artykułów, recenzji i decyzji.
3. Implementacja strategii redakcyjnych R1 i R2.
4. Integracja agentów LLM.
5. Opracowanie metryk i porównywanie wyników.
6. Rozszerzenie o eksperymenty E1, E2 i E3.

## Uruchamianie

Instrukcja uruchamiania nowego POC zostanie uzupełniona po implementacji pierwszej wersji. Dotychczasowy kod symulatora jest zachowany jako baza techniczna.

## Licencja

Zgodnie z plikiem LICENSE w repozytorium.