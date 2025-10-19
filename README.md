# proiect-individual
# Solver Hangman Automat

## Descriere
Acest proiect implementează un solver automat pentru jocul **Hangman**. Codul ghicește litere și cuvinte țintă până la identificarea completă, rulând offline fără dicționar extern.

## Cerințe
- Python 3.8+  
- Fișier CSV cu jocuri: `game_id, pattern_initial, cuvant_tinta`  
- Nu sunt necesare librării externe

## Structură cod
- `citeste_csv(fisier)` → citește datele din CSV  
- `rezolva_joc(pattern, secret, dictionar)` → simulează ghicirea literelor  
- `main()` → rulează toate jocurile și scrie rezultatele în `results/out.csv`

## Cum se rulează
1. Pune fișierul CSV în folderul `data`  
2. Rulează scriptul:
```bash
python solve_hangman_final.py
