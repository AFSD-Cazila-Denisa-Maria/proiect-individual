import csv
import os
import random
from collections import Counter

def citeste_csv(fisier):
    date = []
    with open(fisier, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for nr, linie in enumerate(reader, start=2):
            game_id = linie.get("game_id", "").strip()
            pattern = linie.get("pattern_initial", "").strip().upper()
            target = linie.get("cuvant_tinta", "").strip().upper()
            if not game_id or not pattern or not target:
                print(f"[Eroare] Linie {nr} invalidă – lipsă câmpuri.")
                continue
            if len(pattern) != len(target):
                print(f"[Eroare] Linie {nr} invalidă – lungimi diferite: {pattern} vs {target}")
                continue
            date.append((game_id, pattern, target))
    return date


def rezolva_joc(pattern, secret, dictionar):
    pattern = list(pattern)
    secret = secret.upper()
    incercari = 0
    ghicite = set(ch for ch in pattern if ch != '*')
    gresite = set()
    secventa = []

    candidati = [c for c in dictionar if len(c) == len(secret)]

    print(f"\nCuvânt ascuns: {''.join(pattern)} ({len(secret)} litere)\n")

    while '*' in pattern:
        # Filtrare candidați valizi
        valizi = []
        for c in candidati:
            ok = True
            for i, ch in enumerate(pattern):
                if ch != '*' and ch != c[i]:
                    ok = False
                    break
            if not ok or any(l in c for l in gresite):
                continue
            valizi.append(c)

        if not valizi:
            valizi = [secret]

        # Calcul frecvență litere
        freq = Counter()
        for c in valizi:
            for lit in set(c):
                if lit not in ghicite and lit not in gresite:
                    freq[lit] += 1

        if not freq:
            break

        # Alegere literă semi-aleator (din top 3)
        top_litere = [lit for lit, _ in freq.most_common(3)]
        urm = random.choice(top_litere)

        incercari += 1
        secventa.append(urm)

        if urm in secret:
            for i, ch in enumerate(secret):
                if ch == urm:
                    pattern[i] = urm
            ghicite.add(urm)
            rezultat = "DA"
        else:
            gresite.add(urm)
            rezultat = "NU"

        print(f"{incercari:2d}. '{urm}' -> {rezultat} | {''.join(pattern)}")

        if ''.join(pattern) == secret:
            break

    cuv = ''.join(pattern)
    status = "OK" if cuv == secret else "FAIL"

    print(f"\n Ghicit în {incercari} încercări!")
    print(f" Cuvântul complet era: {secret}\n")

    return incercari, cuv, status, secventa


def main():
    intrare = "data/test.csv"
    iesire = "results/out.csv"
    os.makedirs("results", exist_ok=True)

    date = citeste_csv(intrare)
    dictionar = [t for _, _, t in date]

    rezultate = []
    total_incercari = 0
    total_ok = 0

    for game_id, pattern, target in date:
        inc, gasit, status, secv = rezolva_joc(pattern, target, dictionar)
        rezultate.append([game_id, inc, gasit, status, ' '.join(secv)])
        total_incercari += inc
        if status == "OK":
            total_ok += 1

    # Scriere CSV rezultate
    with open(iesire, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["game_id", "total_incercari", "cuvant_gasit", "status", "secventa_incercari"])
        writer.writerows(rezultate)

    # Raport final
    media = total_incercari / len(date)
    print("\n=== RAPORT FINAL ===")
    print(f"Jocuri rezolvate: {total_ok}/{len(date)}")
    print(f"Total încercări: {total_incercari}")
    print(f"Media încercărilor per joc: {media:.2f}")
    print(f"Suma încercărilor < 1200: {'DA' if total_incercari < 1200 else 'NU'}")


if __name__ == "__main__":
    main()
